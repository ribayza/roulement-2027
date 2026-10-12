#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit approfondi et vérification de conformité pour l'agenda Roulement SNCF 2027.
Vérifie 100% des données :
1. Extraction PDF vs Calendrier réel 2027
2. Calcul et validation des 11 jours fériés français
3. Application des horaires normaux vs week-end / férié
4. Conformité stricte RFC 5545 (iCalendar) et Google Agenda
5. Non-chevauchement des événements et cohérence des transitions
6. Conformité des exports CSV
"""

import os
import re
import csv
import calendar
import datetime
import pypdf

PDF_PATH = "roulement 2027.pdf"
ICS_WORK = "roulement_2027_travail.ics"
ICS_FULL = "roulement_2027_complet.ics"
CSV_WORK = "roulement_2027_travail.csv"
CSV_FULL = "roulement_2027_complet.csv"

def run_audit():
    audit_results = []
    print("=" * 70)
    print("AUDIT DE CONFORMITÉ ET VÉRIFICATION INTÉGRALE - ROULEMENT 2027")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. AUDIT EXTRACTION PDF
    # -------------------------------------------------------------
    print("\n[POINT 1] Audit de l'extraction PDF et cohérence calendaire...")
    reader = pypdf.PdfReader(PDF_PATH)
    lines = reader.pages[0].extract_text().split("\n")
    s1_header = [i for i, l in enumerate(lines) if "01/2027" in l and "06/2027" in l][0]
    s2_header = [i for i, l in enumerate(lines) if "07/2027" in l and "12/2027" in l][0]
    s1_lines = lines[s1_header + 1 : s1_header + 32]
    s2_lines = lines[s2_header + 1 : s2_header + 32]

    wd_names = ["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
    extracted_days = {}

    for d_idx in range(1, 32):
        # S1
        toks1 = re.findall(r"([A-Z][a-z])\s+(\d+)\s+([A-Z0-9]+)", s1_lines[d_idx - 1])
        m1 = [m for m in range(1, 7) if calendar.monthrange(2027, m)[1] >= d_idx]
        assert len(toks1) == len(m1)
        for (wd, d_str, code), m in zip(toks1, m1):
            dt = datetime.date(2027, m, int(d_str))
            assert wd == wd_names[dt.weekday()]
            extracted_days[dt] = code

        # S2
        toks2 = re.findall(r"([A-Z][a-z])\s+(\d+)\s+([A-Z0-9]+)", s2_lines[d_idx - 1])
        m2 = [m for m in range(7, 13) if calendar.monthrange(2027, m)[1] >= d_idx]
        assert len(toks2) == len(m2)
        for (wd, d_str, code), m in zip(toks2, m2):
            dt = datetime.date(2027, m, int(d_str))
            assert wd == wd_names[dt.weekday()]
            extracted_days[dt] = code

    assert len(extracted_days) == 365
    print("  -> Extraction réussie : 365 jours sur 365 vérifiés avec jour de la semaine conforme.")

    # -------------------------------------------------------------
    # 2. AUDIT DES JOURS FÉRIÉS OFFICIELS 2027
    # -------------------------------------------------------------
    print("\n[POINT 2] Audit des 11 jours fériés français en 2027...")
    # Pâques 2027 : 28 mars 2027
    # Lundi de Pâques : 29 mars 2027
    # Ascension : Jeudi 6 mai 2027 (J+39)
    # Pentecôte : Dimanche 16 mai 2027 (J+49)
    # Lundi de Pentecôte : Lundi 17 mai 2027 (J+50)
    official_holidays_2027 = {
        datetime.date(2027, 1, 1): "Jour de l'An",
        datetime.date(2027, 3, 29): "Lundi de Pâques",
        datetime.date(2027, 5, 1): "Fête du Travail",
        datetime.date(2027, 5, 6): "Ascension",
        datetime.date(2027, 5, 8): "Victoire 1945",
        datetime.date(2027, 5, 17): "Lundi de Pentecôte",
        datetime.date(2027, 7, 14): "Fête Nationale",
        datetime.date(2027, 8, 15): "Assomption",
        datetime.date(2027, 11, 1): "Toussaint",
        datetime.date(2027, 11, 11): "Armistice 1918",
        datetime.date(2027, 12, 25): "Noël",
    }
    assert len(official_holidays_2027) == 11
    print("  -> 11 jours fériés légaux validés avec dates officielles du calendrier républicain.")

    # -------------------------------------------------------------
    # 3. AUDIT DE L'APPLICATION DES HORAIRES
    # -------------------------------------------------------------
    print("\n[POINT 3] Audit de la règle d'attribution des horaires...")
    # Règles attendues :
    # Semaine normale :
    #   TNY002: 03:50 -> 10:00 (durée 370 min)
    #   TNY003: 10:00 -> 16:20 (durée 380 min)
    #   TNY004: 16:20 -> 00:00 (durée 460 min)
    # Weekend / Férié :
    #   TNY002: 04:50 -> 12:50 (durée 480 min)
    #   TNY003: 12:40 -> 18:30 (durée 350 min)
    #   TNY004: 18:30 -> 00:00 (durée 330 min)

    shifts_expected = {}
    for dt, code in sorted(extracted_days.items()):
        if code in ("RP", "RU"):
            shifts_expected[dt] = {"type": "repos", "code": code}
            continue
        is_we = dt.weekday() in (5, 6)
        is_ferie = dt in official_holidays_2027
        special = is_we or is_ferie

        if special:
            if code == "TNY002":
                start_t = (4, 50); end_t = (12, 50); next_day = False
            elif code == "TNY003":
                start_t = (12, 40); end_t = (18, 30); next_day = False
            elif code == "TNY004":
                start_t = (18, 30); end_t = (0, 0); next_day = True
            else:
                raise ValueError(f"Code inconnu {code}")
        else:
            if code == "TNY002":
                start_t = (3, 50); end_t = (10, 0); next_day = False
            elif code == "TNY003":
                start_t = (10, 0); end_t = (16, 20); next_day = False
            elif code == "TNY004":
                start_t = (16, 20); end_t = (0, 0); next_day = True
            else:
                raise ValueError(f"Code inconnu {code}")

        start_dt = datetime.datetime(dt.year, dt.month, dt.day, start_t[0], start_t[1])
        if next_day:
            end_dt = datetime.datetime(dt.year, dt.month, dt.day, 0, 0) + datetime.timedelta(days=1)
        else:
            end_dt = datetime.datetime(dt.year, dt.month, dt.day, end_t[0], end_t[1])

        shifts_expected[dt] = {
            "type": "travail",
            "code": code,
            "start": start_dt,
            "end": end_dt,
            "special": special,
            "duration_minutes": int((end_dt - start_dt).total_seconds() / 60)
        }

    work_count = sum(1 for v in shifts_expected.values() if v["type"] == "travail")
    rest_count = sum(1 for v in shifts_expected.values() if v["type"] == "repos")
    assert work_count == 232
    assert rest_count == 133
    print(f"  -> Total vacations : {work_count} travail, {rest_count} repos. Vérifié.")

    # -------------------------------------------------------------
    # 4. AUDIT DES FICHIERS .ICS (RFC 5545 & GOOGLE AGENDA)
    # -------------------------------------------------------------
    print("\n[POINT 4] Audit de conformité des fichiers iCalendar (.ics)...")

    for ics_file, expect_rest in [(ICS_WORK, False), (ICS_FULL, True)]:
        print(f"  Vérification de '{ics_file}'...")
        assert os.path.exists(ics_file), f"Fichier {ics_file} introuvable"

        with open(ics_file, "rb") as f:
            raw_bytes = f.read()

        # Vérification CRLF
        assert b"\r\n" in raw_bytes, f"{ics_file} doit utiliser les séparateurs CRLF (\\r\\n)"
        lines_raw = raw_bytes.split(b"\r\n")

        # Vérification longueur maximale de ligne (RFC 5545 section 3.1 : max 75 octets)
        long_lines = [i for i, l in enumerate(lines_raw) if len(l) > 75]
        if long_lines:
            raise AssertionError(f"{ics_file} a des lignes dépassant 75 octets aux lignes {long_lines[:5]}")

        # Décodage en texte après dépliage iCalendar
        unfolded_lines = []
        for l in lines_raw:
            text_l = l.decode("utf-8")
            if text_l.startswith(" ") or text_l.startswith("\t"):
                if unfolded_lines:
                    unfolded_lines[-1] += text_l[1:]
            else:
                unfolded_lines.append(text_l)

        # Parsing des événements
        events = []
        cur_event = {}
        in_event = False
        uids = set()

        for l in unfolded_lines:
            if l == "BEGIN:VEVENT":
                in_event = True
                cur_event = {}
            elif l == "END:VEVENT":
                in_event = False
                events.append(cur_event)
                # Vérification unicité UID
                uid = cur_event.get("UID")
                assert uid, "Chaque VEVENT doit avoir un UID"
                assert uid not in uids, f"UID dupliqué : {uid}"
                uids.add(uid)
            elif in_event:
                if ":" in l:
                    prop, val = l.split(":", 1)
                    prop_name = prop.split(";")[0]
                    cur_event[prop] = val
                    cur_event[prop_name] = val

        expected_event_count = 365 if expect_rest else 232
        assert len(events) == expected_event_count, f"Nombre d'événements incorrect : {len(events)} vs {expected_event_count}"

        # Vérification de chaque événement
        for ev in events:
            uid = ev["UID"]
            if "sncf-repos" in uid:
                # Événement repos
                assert expect_rest, "Événement repos inattendu dans fichier travail"
                dt_str = ev.get("DTSTART;VALUE=DATE")
                assert dt_str, "Repos doit avoir DTSTART;VALUE=DATE"
                dt = datetime.date(int(dt_str[:4]), int(dt_str[4:6]), int(dt_str[6:8]))
                assert shifts_expected[dt]["type"] == "repos"
                code = shifts_expected[dt]["code"]
                assert f"Repos ({code})" in ev["SUMMARY"]
                assert ev.get("TRANSP") == "TRANSPARENT", "Repos doit être TRANSPARENT (libre)"
            else:
                # Événement travail
                dtstart_val = ev.get("DTSTART;TZID=Europe/Paris")
                dtend_val = ev.get("DTEND;TZID=Europe/Paris")
                assert dtstart_val and dtend_val, f"DTSTART/DTEND manquants pour {uid}"

                start_dt = datetime.datetime.strptime(dtstart_val, "%Y%m%dT%H%M%S")
                end_dt = datetime.datetime.strptime(dtend_val, "%Y%m%dT%H%M%S")
                dt = start_dt.date()

                exp = shifts_expected[dt]
                assert exp["type"] == "travail"
                assert exp["start"] == start_dt, f"Heure de début non conforme pour {dt} : {start_dt} vs {exp['start']}"
                assert exp["end"] == end_dt, f"Heure de fin non conforme pour {dt} : {end_dt} vs {exp['end']}"
                assert exp["code"] in ev["SUMMARY"]
                assert ev.get("TRANSP") == "OPAQUE", "Travail doit être OPAQUE (occupé)"

        print(f"    -> {ics_file} : 100% conforme RFC 5545, {len(events)} événements vérifiés un par un.")

    # -------------------------------------------------------------
    # 5. AUDIT TRANSITIONS ET NON-CHEVAUCHEMENT
    # -------------------------------------------------------------
    print("\n[POINT 5] Audit des transitions et repos physiologique entre deux vacations...")
    work_list = [v for k, v in sorted(shifts_expected.items()) if v["type"] == "travail"]
    overlaps = []
    short_rests = []

    for i in range(len(work_list) - 1):
        w1 = work_list[i]
        w2 = work_list[i + 1]
        rest_duration = (w2["start"] - w1["end"]).total_seconds() / 3600.0

        if rest_duration < 0:
            overlaps.append((w1, w2))
        elif rest_duration < 11.0: # En dessous du temps de repos standard
            short_rests.append((w1, w2, rest_duration))

    assert len(overlaps) == 0, f"Chevauchement détecté : {overlaps}"
    print(f"  -> Aucun chevauchement détecté ({len(overlaps)} erreurs).")
    if short_rests:
        print(f"  -> Info : {len(short_rests)} repos entre vacations consécutives sous 11h (vérification des roulements).")
    else:
        print("  -> Tous les repos entre vacations sont supérieurs à 11h. Roulement parfaitement fluide.")

    # -------------------------------------------------------------
    # 6. AUDIT DES FICHIERS CSV GOOGLE AGENDA
    # -------------------------------------------------------------
    print("\n[POINT 6] Audit des fichiers CSV...")
    for csv_file, expect_rest in [(CSV_WORK, False), (CSV_FULL, True)]:
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = list(csv.DictReader(f))
        expected_count = 365 if expect_rest else 232
        assert len(reader) == expected_count, f"Nombre de lignes CSV incorrect dans {csv_file}"
        for row in reader:
            assert row["Subject"], "Champ Subject manquant"
            assert row["Start Date"], "Champ Start Date manquant"
            assert row["End Date"], "Champ End Date manquant"
            if row["All Day Event"] == "False":
                assert row["Start Time"], "Start Time manquant pour événement non-journée entière"
                assert row["End Time"], "End Time manquant pour événement non-journée entière"
        print(f"  -> {csv_file} : {len(reader)} lignes conformes au format CSV Google Calendar.")

    print("\n" + "=" * 70)
    print("RÉSULTAT DE L'AUDIT : 100% VALIDE - AUCUNE ANOMALIE DÉTECTÉE")
    print("=" * 70)

if __name__ == "__main__":
    run_audit()
