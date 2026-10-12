#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'agenda Google Calendar pour le roulement SNCF 2027.
Extrait les affectations depuis 'roulement 2027.pdf' et génère les fichiers .ics et .csv.

Règles des tranches horaires :
- Jours normaux (Lundi au Vendredi, hors jours fériés) :
    - TNY002 : 03h50 - 10h00
    - TNY003 : 10h00 - 16h20
    - TNY004 : 16h20 - 00h00 (minuit)
- Samedis, Dimanches et Jours Fériés (France métropolitaine 2027) :
    - TNY002 : 04h50 - 12h50
    - TNY003 : 12h40 - 18h30
    - TNY004 : 18h30 - 00h00 (minuit)
- Repos :
    - RP : Repos Périodique
    - RU : Repos Unique / Supplémentaire
"""

import os
import re
import csv
import calendar
import datetime
from collections import Counter
import pypdf

PDF_PATH = "roulement 2027.pdf"

# --- Calcul des jours fériés 2027 en France métropolitaine ---
def get_french_holidays(year=2027):
    # Algorithme Meeus/Jones/Butcher pour le dimanche de Pâques
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451
    month = (h + L - 7 * m + 114) // 31
    day = ((h + L - 7 * m + 114) % 31) + 1
    easter = datetime.date(year, month, day)

    holidays = {
        datetime.date(year, 1, 1): "Jour de l'An",
        easter + datetime.timedelta(days=1): "Lundi de Pâques",
        datetime.date(year, 5, 1): "Fête du Travail",
        datetime.date(year, 5, 8): "Victoire 1945",
        easter + datetime.timedelta(days=39): "Ascension",
        easter + datetime.timedelta(days=50): "Lundi de Pentecôte",
        datetime.date(year, 7, 14): "Fête Nationale",
        datetime.date(year, 8, 15): "Assomption",
        datetime.date(year, 11, 1): "Toussaint",
        datetime.date(year, 11, 11): "Armistice 1918",
        datetime.date(year, 12, 25): "Noël",
    }
    return holidays


# --- Définition des horaires selon le jour ---
SHIFTS_CONFIG = {
    # Jours normaux de semaine (Lundi à Vendredi non férié)
    "normal": {
        "TNY002": {"start": (3, 50), "end": (10, 0), "label": "03h50 - 10h00"},
        "TNY003": {"start": (10, 0), "end": (16, 20), "label": "10h00 - 16h20"},
        "TNY004": {"start": (16, 20), "end": (0, 0), "ends_next_day": True, "label": "16h20 - 00h00"},
    },
    # Samedis, Dimanches et Jours Fériés
    "weekend_ferie": {
        "TNY002": {"start": (4, 50), "end": (12, 50), "label": "04h50 - 12h50"},
        "TNY003": {"start": (12, 40), "end": (18, 30), "label": "12h40 - 18h30"},
        "TNY004": {"start": (18, 30), "end": (0, 0), "ends_next_day": True, "label": "18h30 - 00h00"},
    }
}


def parse_pdf(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    text = reader.pages[0].extract_text()
    lines = text.split("\n")

    # Recherche des lignes contenant les en-têtes
    s1_header_idx = None
    s2_header_idx = None
    for idx, line in enumerate(lines):
        if "01/2027" in line and "06/2027" in line:
            s1_header_idx = idx
        elif "07/2027" in line and "12/2027" in line:
            s2_header_idx = idx

    if s1_header_idx is None or s2_header_idx is None:
        raise ValueError("Impossible de localiser les tableaux semestriels dans le PDF.")

    s1_lines = lines[s1_header_idx + 1: s1_header_idx + 32]
    s2_lines = lines[s2_header_idx + 1: s2_header_idx + 32]

    all_days = {}

    # Semestre 1 (Janvier à Juin 2027)
    for day_num in range(1, 32):
        line = s1_lines[day_num - 1]
        tokens = re.findall(r"([A-Z][a-z])\s+(\d+)\s+([A-Z0-9]+)", line)
        months = [m for m in range(1, 7) if calendar.monthrange(2027, m)[1] >= day_num]
        for (wd_abbr, d_str, code), m in zip(tokens, months):
            d = int(d_str)
            all_days[datetime.date(2027, m, d)] = code

    # Semestre 2 (Juillet à Décembre 2027)
    for day_num in range(1, 32):
        line = s2_lines[day_num - 1]
        tokens = re.findall(r"([A-Z][a-z])\s+(\d+)\s+([A-Z0-9]+)", line)
        months = [m for m in range(7, 13) if calendar.monthrange(2027, m)[1] >= day_num]
        for (wd_abbr, d_str, code), m in zip(tokens, months):
            d = int(d_str)
            all_days[datetime.date(2027, m, d)] = code

    return all_days


def fold_line(line, limit=75):
    """Plie une ligne iCalendar pour respecter strictement la limite RFC 5545 de 75 octets."""
    encoded = line.encode("utf-8")
    if len(encoded) <= limit:
        return line
    parts = []
    first = True
    while encoded:
        max_len = limit if first else (limit - 1)
        if len(encoded) <= max_len:
            parts.append(encoded.decode("utf-8"))
            break
        cut = max_len
        while cut > 0:
            try:
                part = encoded[:cut].decode("utf-8")
                break
            except UnicodeDecodeError:
                cut -= 1
        parts.append(part)
        encoded = encoded[cut:]
        first = False
    return "\r\n ".join(parts)


def escape_ics_text(text):
    """Échappe les caractères réservés selon RFC 5545."""
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\n", "\\n")
    return text


def generate_ics(days_dict, holidays, output_path, include_rest=False, short_title=False):
    """Génère un fichier .ics (iCalendar) compatible Google Agenda."""
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//SNCF//Roulement 2027 Lannemezan//FR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Roulement SNCF 2027",
        "X-WR-TIMEZONE:Europe/Paris",
        "BEGIN:VTIMEZONE",
        "TZID:Europe/Paris",
        "X-LIC-LOCATION:Europe/Paris",
        "BEGIN:DAYLIGHT",
        "TZOFFSETFROM:+0100",
        "TZOFFSETTO:+0200",
        "TZNAME:CEST",
        "DTSTART:19700329T020000",
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
        "END:DAYLIGHT",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0200",
        "TZOFFSETTO:+0100",
        "TZNAME:CET",
        "DTSTART:19701025T030000",
        "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]

    for dt in sorted(days_dict.keys()):
        code = days_dict[dt]
        is_weekend = dt.weekday() in (5, 6)
        holiday_name = holidays.get(dt, None)
        is_holiday = holiday_name is not None
        regime_label = ""
        if is_holiday:
            regime_label = f"Jour férié ({holiday_name})"
        elif is_weekend:
            regime_label = f"Week-end ({days_fr[dt.weekday()]})"
        else:
            regime_label = f"Semaine ({days_fr[dt.weekday()]})"

        if code in ("RP", "RU"):
            if not include_rest:
                continue
            # Événement journée entière pour le repos
            uid = f"sncf-repos-{dt.strftime('%Y%m%d')}@roulement2027"
            next_day = dt + datetime.timedelta(days=1)
            summary = f"Repos ({code})"
            desc = f"Jour de repos ({'Repos Périodique' if code == 'RP' else 'Repos Unique'})\n{regime_label}"
            event_lines = [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{now_utc}",
                f"DTSTART;VALUE=DATE:{dt.strftime('%Y%m%d')}",
                f"DTEND;VALUE=DATE:{next_day.strftime('%Y%m%d')}",
                f"SUMMARY:{escape_ics_text(summary)}",
                f"DESCRIPTION:{escape_ics_text(desc)}",
                "STATUS:CONFIRMED",
                "TRANSP:TRANSPARENT",
                "END:VEVENT",
            ]
            lines.extend(event_lines)
            continue

        # Tranche de travail
        cfg_category = "weekend_ferie" if (is_weekend or is_holiday) else "normal"
        shift_info = SHIFTS_CONFIG[cfg_category][code]

        start_h, start_m = shift_info["start"]
        end_h, end_m = shift_info["end"]

        start_dt = datetime.datetime(dt.year, dt.month, dt.day, start_h, start_m)
        if shift_info.get("ends_next_day", False):
            end_dt = datetime.datetime(dt.year, dt.month, dt.day, 0, 0) + datetime.timedelta(days=1)
        else:
            end_dt = datetime.datetime(dt.year, dt.month, dt.day, end_h, end_m)

        start_str = start_dt.strftime("%Y%m%dT%H%M%S")
        end_str = end_dt.strftime("%Y%m%dT%H%M%S")

        hours_label = shift_info["label"]
        if short_title:
            summary = code
        else:
            summary = f"{code} ({hours_label})"

        desc = (
            f"Poste : {code}\n"
            f"Horaires : {hours_label}\n"
            f"Régime : {regime_label}\n"
            f"Lieu : 676528 LANNEMEZAN INFRA\n"
            f"Agent : RIADH BIZID 7712336Z\n"
            f"Affectation : 676528-TNY651"
        )
        location = "Lannemezan Infra"
        uid = f"sncf-{dt.strftime('%Y%m%d')}-{code}@roulement2027"

        event_lines = [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{now_utc}",
            f"DTSTART;TZID=Europe/Paris:{start_str}",
            f"DTEND;TZID=Europe/Paris:{end_str}",
            f"SUMMARY:{escape_ics_text(summary)}",
            f"DESCRIPTION:{escape_ics_text(desc)}",
            f"LOCATION:{escape_ics_text(location)}",
            "STATUS:CONFIRMED",
            "TRANSP:OPAQUE",
            "END:VEVENT",
        ]
        lines.extend(event_lines)

    lines.append("END:VCALENDAR")

    # Écriture avec sauts de lignes CRLF et pliage RFC 5545
    with open(output_path, "wb") as f:
        for l in lines:
            folded = fold_line(l)
            f.write((folded + "\r\n").encode("utf-8"))


def generate_csv(days_dict, holidays, output_path, include_rest=False):
    """Génère un fichier CSV au format standard Google Calendar."""
    days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    rows = []
    headers = [
        "Subject",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "All Day Event",
        "Description",
        "Location"
    ]

    for dt in sorted(days_dict.keys()):
        code = days_dict[dt]
        is_weekend = dt.weekday() in (5, 6)
        holiday_name = holidays.get(dt, None)
        is_holiday = holiday_name is not None

        if is_holiday:
            regime_label = f"Jour férié ({holiday_name})"
        elif is_weekend:
            regime_label = f"Week-end ({days_fr[dt.weekday()]})"
        else:
            regime_label = f"Semaine ({days_fr[dt.weekday()]})"

        if code in ("RP", "RU"):
            if not include_rest:
                continue
            rows.append({
                "Subject": f"Repos ({code})",
                "Start Date": dt.strftime("%d/%m/%Y"),
                "Start Time": "",
                "End Date": dt.strftime("%d/%m/%Y"),
                "End Time": "",
                "All Day Event": "True",
                "Description": f"Jour de repos ({'Repos Périodique' if code == 'RP' else 'Repos Unique'}) - {regime_label}",
                "Location": ""
            })
            continue

        cfg_category = "weekend_ferie" if (is_weekend or is_holiday) else "normal"
        shift_info = SHIFTS_CONFIG[cfg_category][code]

        start_h, start_m = shift_info["start"]
        end_h, end_m = shift_info["end"]

        start_time_str = f"{start_h:02d}:{start_m:02d}"
        if shift_info.get("ends_next_day", False):
            end_date_str = (dt + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            end_time_str = "00:00"
        else:
            end_date_str = dt.strftime("%d/%m/%Y")
            end_time_str = f"{end_h:02d}:{end_m:02d}"

        rows.append({
            "Subject": f"{code} ({shift_info['label']})",
            "Start Date": dt.strftime("%d/%m/%Y"),
            "Start Time": start_time_str,
            "End Date": end_date_str,
            "End Time": end_time_str,
            "All Day Event": "False",
            "Description": f"Poste {code} - Horaires {shift_info['label']} - {regime_label} - Lannemezan Infra",
            "Location": "676528 LANNEMEZAN INFRA"
        })

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    print(f"Extraction du fichier PDF '{PDF_PATH}'...")
    days = parse_pdf(PDF_PATH)
    print(f"Total de jours analysés : {len(days)}")
    counts = Counter(days.values())
    for code, count in sorted(counts.items()):
        print(f"  - {code:6s} : {count} jours")

    holidays = get_french_holidays(2027)
    print(f"\nJours fériés 2027 identifiés ({len(holidays)}) :")
    days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    for dt, name in sorted(holidays.items()):
        code = days[dt]
        print(f"  - {dt.strftime('%d/%m/%Y')} ({days_fr[dt.weekday()]:8s}) : {name:20s} -> {code}")

    print("\nGénération des fichiers d'agenda pour Google Agenda...")

    # 1. Fichier ICS principal (Postes de travail avec horaires, sans les jours de repos)
    ics_work = "roulement_2027_travail.ics"
    generate_ics(days, holidays, ics_work, include_rest=False, short_title=False)
    print(f"  [OK] {ics_work} (232 postes de travail)")

    # 2. Fichier ICS complet (Postes de travail + Jours de repos RP/RU)
    ics_full = "roulement_2027_complet.ics"
    generate_ics(days, holidays, ics_full, include_rest=True, short_title=False)
    print(f"  [OK] {ics_full} (365 événements : 232 postes + 133 repos)")

    # 3. Fichier CSV pour Google Calendar
    csv_work = "roulement_2027_travail.csv"
    generate_csv(days, holidays, csv_work, include_rest=False)
    print(f"  [OK] {csv_work}")

    csv_full = "roulement_2027_complet.csv"
    generate_csv(days, holidays, csv_full, include_rest=True)
    print(f"  [OK] {csv_full}")

    print("\nTerminé avec succès !")


if __name__ == "__main__":
    main()
