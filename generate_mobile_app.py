#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de la version ultime de l'application Web :
- Ergonomie Mobile PWA (Bottom Nav Bar, Vue Planning / Liste tactile, Cartes grands formats)
- Synchronisation automatique bidirectionnelle en temps réel (Cloud Puter & Firebase)
  avec écouteurs de visibilité / focus et polling automatique toutes les 10 secondes.
- Intégration QR Code hors-ligne et liens magiques.
- Totalement autonome (1 seul fichier HTML sans dépendance lourde).
"""

import json
import os

JSON_PATH = "roulement_data_2027.json"
QRCODE_PATH = "qrcode.min.js"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    days_data = json.load(f)
days_json_str = json.dumps(days_data, ensure_ascii=False)

with open(QRCODE_PATH, "r", encoding="utf-8") as f:
    qrcode_js = f.read()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Roulement SNCF 2027 - Lannemezan Infra | Planning & Congés</title>
  
  <!-- PWA & Mobile Web App Meta Tags -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Roulement SNCF">
  <meta name="theme-color" content="#1e3a8a">
  
  <script src="https://js.puter.com/v2/"></script>
  
  <style>
    :root {
      --primary: #1e3a8a;
      --primary-light: #3b82f6;
      --primary-dark: #172554;
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      
      --color-tny002: #0284c7;
      --color-tny003: #7c3aed;
      --color-tny004: #d97706;
      --color-rp: #64748b;
      --color-ru: #475569;
      
      --color-vt: #059669;
      --color-vt-light: #d1fae5;
      --color-conge: #2563eb;
      --color-conge-light: #dbeafe;
      --color-pending: #f59e0b;
      --color-pending-light: #fef3c7;
      --color-rejected: #dc2626;
      --color-rejected-light: #fee2e2;
      
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
      --radius: 14px;
      --radius-sm: 10px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: var(--bg-page);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 90px; /* Espace pour la bottom navigation sur mobile */
    }

    header {
      background: linear-gradient(135deg, #1e3a8a 0%, #172554 100%);
      color: white;
      padding: 16px 20px;
      box-shadow: var(--shadow);
      position: sticky;
      top: 0;
      z-index: 40;
    }

    .header-container {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }

    .header-title h1 {
      font-size: 1.25rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .header-title p {
      font-size: 0.8rem;
      color: #cbd5e1;
      margin-top: 2px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.15s ease;
      text-decoration: none;
      min-height: 38px;
    }

    .btn-light {
      background: rgba(255, 255, 255, 0.15);
      color: white;
      backdrop-filter: blur(8px);
    }
    .btn-light:hover { background: rgba(255, 255, 255, 0.25); }

    .btn-sync-badge {
      background: rgba(16, 185, 129, 0.2);
      color: #a7f3d0;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .btn-sync-badge:hover { background: rgba(16, 185, 129, 0.3); color: #ffffff; }

    .btn-primary { background: #2563eb; color: white; }
    .btn-primary:hover { background: #1d4ed8; }
    .btn-success { background: #059669; color: white; }
    .btn-success:hover { background: #047857; }
    .btn-danger { background: #dc2626; color: white; }
    .btn-danger:hover { background: #b91c1c; }

    .main-container {
      max-width: 1440px;
      margin: 16px auto;
      padding: 0 16px;
    }

    /* TOAST NOTIFICATION */
    .toast-notification {
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%) translateY(-30px);
      background: #0f172a;
      color: white;
      padding: 10px 20px;
      border-radius: 9999px;
      box-shadow: var(--shadow-lg);
      font-size: 0.88rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 200;
      opacity: 0;
      transition: all 0.3s ease;
      pointer-events: none;
      white-space: nowrap;
    }
    .toast-notification.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
      pointer-events: auto;
    }

    /* DASHBOARD COUNTERS */
    .counters-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }

    .card {
      background: var(--bg-card);
      border-radius: var(--radius);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 16px 18px;
      position: relative;
    }

    .card-vt { border-top: 4px solid var(--color-vt); }
    .card-conge { border-top: 4px solid var(--color-conge); }
    .card-summary { border-top: 4px solid #6366f1; }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .card-title {
      font-size: 1rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .quota-badge {
      background: #f1f5f9;
      color: var(--text-main);
      padding: 3px 8px;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 700;
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .quota-badge input {
      width: 44px;
      padding: 2px 4px;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: 700;
      text-align: center;
      color: #0f172a;
    }

    .stats-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 8px;
    }

    .stat-box {
      background: #f8fafc;
      padding: 8px 6px;
      border-radius: var(--radius-sm);
      text-align: center;
      border: 1px solid #f1f5f9;
    }

    .stat-label {
      font-size: 0.68rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.3px;
    }

    .stat-value {
      font-size: 1.35rem;
      font-weight: 800;
      margin-top: 2px;
      line-height: 1.1;
    }

    .val-vt { color: var(--color-vt); }
    .val-conge { color: var(--color-conge); }
    .val-pending { color: var(--color-pending); }
    .val-rejected { color: var(--color-rejected); }
    .val-restant { color: #0284c7; }

    .progress-bar-container {
      height: 6px;
      background: #e2e8f0;
      border-radius: 9999px;
      overflow: hidden;
      margin-top: 10px;
      display: flex;
    }

    .progress-accepted { background: var(--color-vt); height: 100%; transition: width 0.3s ease; }
    .progress-pending { background: var(--color-pending); height: 100%; transition: width 0.3s ease; }
    .progress-conge-accepted { background: var(--color-conge); height: 100%; transition: width 0.3s ease; }

    /* CONTROLS BAR (DESKTOP) */
    .controls-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
      background: white;
      padding: 10px 14px;
      border-radius: var(--radius);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
    }

    .month-nav {
      display: flex;
      align-items: center;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 4px;
      max-width: 100%;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .month-nav::-webkit-scrollbar { display: none; }

    .btn-month {
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
      min-height: 36px;
    }
    .btn-month:hover { background: #f1f5f9; color: var(--text-main); }
    .btn-month.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    .view-toggles {
      display: flex;
      align-items: center;
      gap: 4px;
      background: #f1f5f9;
      padding: 4px;
      border-radius: var(--radius-sm);
    }

    .btn-view {
      padding: 6px 12px;
      border-radius: 8px;
      border: none;
      background: transparent;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      min-height: 32px;
    }
    .btn-view.active {
      background: white;
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    /* CALENDAR GRID (GRILLE MOIS) */
    .calendar-grid-header {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
      text-align: center;
      font-weight: 700;
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
    }

    .day-cell {
      background: white;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      min-height: 105px;
      padding: 8px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      cursor: pointer;
      transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    .day-cell:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow);
      border-color: #94a3b8;
    }
    .day-cell.is-empty { background: transparent; border-color: transparent; cursor: default; transform: none; box-shadow: none; }
    .day-cell.is-weekend { background: #fafafa; }
    .day-cell.is-holiday { background: #fffbeb; border-color: #fde68a; }

    .day-cell-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 4px;
    }

    .day-num { font-size: 0.95rem; font-weight: 800; color: var(--text-main); }
    .holiday-badge {
      font-size: 0.65rem;
      background: #fef3c7;
      color: #92400e;
      padding: 1px 4px;
      border-radius: 4px;
      font-weight: 600;
      max-width: 90px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .day-shift-badge {
      display: inline-block;
      padding: 3px 6px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 700;
      text-align: center;
      margin-bottom: 2px;
      color: white;
    }
    .badge-tny002 { background-color: var(--color-tny002); }
    .badge-tny003 { background-color: var(--color-tny003); }
    .badge-tny004 { background-color: var(--color-tny004); }
    .badge-rp { background-color: #e2e8f0; color: #475569; }
    .badge-ru { background-color: #cbd5e1; color: #334155; }

    .day-hours { font-size: 0.72rem; color: var(--text-muted); font-weight: 500; }

    .day-override-badge {
      margin-top: 4px;
      padding: 3px 6px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
    }

    .day-cell.has-vt-pending { border: 2px dashed var(--color-pending); background: #fffdf5; }
    .badge-vt-pending { background: var(--color-pending-light); color: #92400e; border: 1px solid #fcd34d; }
    .day-cell.has-vt-accepted { border: 2px solid var(--color-vt); background: #f0fdf4; }
    .badge-vt-accepted { background: var(--color-vt-light); color: #065f46; border: 1px solid #a7f3d0; }
    .day-cell.has-vt-rejected { border: 1px solid #fca5a5; background: #fef2f2; }
    .badge-vt-rejected { background: var(--color-rejected-light); color: #991b1b; border: 1px solid #fca5a5; }

    .day-cell.has-conge-pending { border: 2px dashed var(--color-pending); background: #fffdf5; }
    .badge-conge-pending { background: var(--color-pending-light); color: #92400e; border: 1px solid #fcd34d; }
    .day-cell.has-conge-accepted { border: 2px solid var(--color-conge); background: #eff6ff; }
    .badge-conge-accepted { background: var(--color-conge-light); color: #1e40af; border: 1px solid #bfdbfe; }
    .day-cell.has-conge-rejected { border: 1px solid #fca5a5; background: #fef2f2; }
    .badge-conge-rejected { background: var(--color-rejected-light); color: #991b1b; border: 1px solid #fca5a5; }

    /* VUE PLANNING / AGENDA MOBILE STREAM */
    .stream-container {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .stream-card {
      background: white;
      border-radius: var(--radius);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.15s ease;
      min-height: 68px;
    }
    .stream-card:active {
      transform: scale(0.98);
      background: #f1f5f9;
    }

    .stream-card.is-weekend { background: #fafafa; }
    .stream-card.is-holiday { background: #fffbeb; border-color: #fde68a; }

    .stream-left {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .stream-date-badge {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #f1f5f9;
      border-radius: 10px;
      width: 48px;
      height: 48px;
      flex-shrink: 0;
    }
    .stream-weekday {
      font-size: 0.68rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
    }
    .stream-daynum {
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1;
    }

    .stream-info {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .stream-shift-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .stream-shift-code {
      font-size: 0.95rem;
      font-weight: 800;
    }
    .stream-hours {
      font-size: 0.85rem;
      font-weight: 600;
      color: #334155;
    }
    .stream-meta {
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    .stream-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .stream-badge-state {
      padding: 6px 12px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      white-space: nowrap;
    }

    /* BARRE TACTILE INFÉRIEURE MOBILE (BOTTOM BAR) */
    .mobile-bottom-bar {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: white;
      border-top: 1px solid var(--border-color);
      box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.05);
      z-index: 50;
      padding: 6px 12px;
      justify-content: space-around;
      align-items: center;
    }

    .bottom-bar-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      padding: 6px 10px;
      border-radius: 8px;
      flex: 1;
      max-width: 80px;
    }
    .bottom-bar-item.active {
      color: var(--primary);
      font-weight: 800;
    }
    .bottom-bar-item svg {
      width: 22px;
      height: 22px;
    }

    /* TABLE VIEW */
    .demandes-table-container {
      background: white;
      border-radius: var(--radius);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      overflow-x: auto;
      padding: 16px;
    }
    .table-toolbar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }
    .filter-pills { display: flex; gap: 6px; flex-wrap: wrap; }
    .pill {
      padding: 6px 12px;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
      background: white;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      color: var(--text-muted);
      min-height: 32px;
    }
    .pill.active { background: var(--primary); color: white; border-color: var(--primary); }

    table.data-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
    table.data-table th, table.data-table td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border-color); }
    table.data-table th { background: #f8fafc; font-weight: 700; color: var(--text-muted); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; }
    table.data-table tr:hover { background: #f8fafc; }

    /* MODALS */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      display: flex;
      justify-content: center;
      align-items: flex-end; /* En bas sur mobile façon bottom sheet */
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }
    .modal-backdrop.open { opacity: 1; pointer-events: auto; }

    .modal-content {
      background: white;
      border-radius: 20px 20px 0 0;
      box-shadow: var(--shadow-lg);
      width: 100%;
      max-width: 540px;
      max-height: 85vh;
      overflow-y: auto;
      padding: 24px 20px;
      transform: translateY(100%);
      transition: transform 0.25s ease-out;
    }
    .modal-backdrop.open .modal-content { transform: translateY(0); }

    @media (min-width: 640px) {
      .modal-backdrop { align-items: center; }
      .modal-content { border-radius: var(--radius); transform: translateY(20px); }
      .modal-backdrop.open .modal-content { transform: translateY(0); }
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
    }
    .modal-title { font-size: 1.25rem; font-weight: 800; }
    .modal-close { background: none; border: none; font-size: 1.6rem; cursor: pointer; color: var(--text-muted); padding: 4px; }

    .form-group { margin-bottom: 16px; }
    .form-label { display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; color: var(--text-main); }

    .choice-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .choice-card {
      border: 2px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 14px 10px;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
      min-height: 75px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .choice-card:hover { border-color: #94a3b8; }
    .choice-card.selected-vt { border-color: var(--color-vt); background: var(--color-vt-light); }
    .choice-card.selected-conge { border-color: var(--color-conge); background: var(--color-conge-light); }
    .choice-card-title { font-weight: 800; font-size: 1rem; }
    .choice-card-desc { font-size: 0.72rem; color: var(--text-muted); margin-top: 2px; }

    .status-select-container { display: flex; gap: 6px; margin-top: 8px; }
    .status-btn {
      flex: 1;
      padding: 10px 6px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: #f8fafc;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      min-height: 42px;
    }
    .status-btn.selected { background: var(--primary); color: white; border-color: var(--primary); }

    .info-box { background: #f1f5f9; border-radius: var(--radius-sm); padding: 12px; margin-bottom: 16px; font-size: 0.85rem; }
    .info-box-row { display: flex; justify-content: space-between; margin-bottom: 4px; }
    .info-box-row:last-child { margin-bottom: 0; }

    /* YEAR VIEW */
    .year-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 14px; }
    .year-month-card { background: white; border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 12px; box-shadow: var(--shadow-sm); }
    .year-month-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; text-align: center; color: var(--primary); }
    .year-month-calendar { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; text-align: center; }
    .year-mini-day {
      aspect-ratio: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.72rem;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
    }

    /* SYNC MODAL */
    .sync-tabs { display: flex; gap: 6px; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
    .sync-tab-btn {
      padding: 8px 12px;
      border: none;
      background: transparent;
      font-weight: 700;
      font-size: 0.85rem;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: 6px;
    }
    .sync-tab-btn.active { background: #eff6ff; color: var(--primary); }
    .qr-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
      background: #f8fafc;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      margin-bottom: 16px;
    }
    #qrcodeBox { background: white; padding: 12px; border-radius: 8px; box-shadow: var(--shadow-sm); }

    /* RESPONSIVE MOBILE TWEAKS */
    @media (max-width: 768px) {
      .mobile-bottom-bar { display: flex; }
      .header-actions .btn-sync-badge, .header-actions .btn-light:last-child { display: none; }
      .controls-bar { margin-bottom: 12px; padding: 8px 10px; }
      .view-toggles { display: none; } /* On utilise la bottom bar sur mobile */
      .stats-row { grid-template-columns: repeat(2, 1fr); gap: 6px; }
      .day-cell { min-height: 82px; padding: 4px 6px; }
      .day-num { font-size: 0.85rem; }
      .day-shift-badge { font-size: 0.68rem; padding: 2px 4px; margin-bottom: 0; }
      .day-hours { display: none; }
      .day-override-badge { font-size: 0.65rem; padding: 2px 4px; }
    }
  </style>
</head>
<body>

  <!-- TOAST NOTIFICATION -->
  <div class="toast-notification" id="toastBox">
    <span id="toastIcon">✅</span>
    <span id="toastMsg">Action effectuée</span>
  </div>

  <!-- HEADER -->
  <header>
    <div class="header-container">
      <div class="header-title">
        <h1>🚆 Roulement SNCF 2027 <span style="font-size: 0.85rem; font-weight: 400; opacity: 0.85;">| Lannemezan</span></h1>
        <p>RIADH BIZID 7712336Z • TNY651 • Soldes & Planning</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-sync-badge" onclick="openSyncModal()">
          ☁️ Sync Cloud <span id="syncIndicator" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; margin-left:4px;"></span>
        </button>
        <button class="btn btn-light" onclick="exportUpdatedICS()">
          📥 Exporter (.ics)
        </button>
        <button class="btn btn-light" onclick="openSettingsModal()">
          ⚙️ Quotas
        </button>
      </div>
    </div>
  </header>

  <div class="main-container">

    <!-- COMPTEURS DE SOLDES VT ET CONGES -->
    <div class="counters-grid" id="countersSection">
      <!-- CARTE VT -->
      <div class="card card-vt">
        <div class="card-header">
          <div class="card-title">
            <span style="color: var(--color-vt);">⏱️</span> Vacations Temps Partiel (VT)
          </div>
          <div class="quota-badge">
            Droit : <input type="number" id="inputQuotaVT" value="44" min="0" max="100" onchange="updateQuotas()"> j
          </div>
        </div>
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-label">Posés (attente)</div>
            <div class="stat-value val-pending" id="statVTPending">0</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Acceptés</div>
            <div class="stat-value val-vt" id="statVTAccepted">0</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Restant à poser</div>
            <div class="stat-value val-restant" id="statVTRemaining">44</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Refusés</div>
            <div class="stat-value val-rejected" id="statVTRejected">0</div>
          </div>
        </div>
        <div class="progress-bar-container">
          <div id="barVTAccepted" class="progress-accepted" style="width: 0%;"></div>
          <div id="barVTPending" class="progress-pending" style="width: 0%;"></div>
        </div>
      </div>

      <!-- CARTE CONGES -->
      <div class="card card-conge">
        <div class="card-header">
          <div class="card-title">
            <span style="color: var(--color-conge);">🏖️</span> Congés Annuels (CA)
          </div>
          <div class="quota-badge">
            Droit : <input type="number" id="inputQuotaConge" value="23" min="0" max="60" onchange="updateQuotas()"> j
          </div>
        </div>
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-label">Posés (attente)</div>
            <div class="stat-value val-pending" id="statCongePending">0</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Acceptés</div>
            <div class="stat-value val-conge" id="statCongeAccepted">0</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Restant à poser</div>
            <div class="stat-value val-restant" id="statCongeRemaining">23</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Refusés</div>
            <div class="stat-value val-rejected" id="statCongeRejected">0</div>
          </div>
        </div>
        <div class="progress-bar-container">
          <div id="barCongeAccepted" class="progress-conge-accepted" style="width: 0%;"></div>
          <div id="barCongePending" class="progress-pending" style="width: 0%;"></div>
        </div>
      </div>

      <!-- CARTE SYNTHESE DU ROULEMENT -->
      <div class="card card-summary">
        <div class="card-header">
          <div class="card-title">
            <span>📅</span> Activité Réelle 2027
          </div>
          <div class="quota-badge">
            Total : 365 j
          </div>
        </div>
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-label">Postes initiaux</div>
            <div class="stat-value" style="color: #475569;">232</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Postes réels</div>
            <div class="stat-value" style="color: var(--primary);" id="statWorkReal">232</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Repos (RP/RU)</div>
            <div class="stat-value" style="color: var(--color-rp);">133</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Fériés</div>
            <div class="stat-value" style="color: #d97706;">11</div>
          </div>
        </div>
      </div>
    </div>

    <!-- BARRE DE CONTROLE & MOIS -->
    <div class="controls-bar">
      <div class="month-nav" id="monthNavButtons"></div>
      <div class="view-toggles">
        <button class="btn-view active" id="btnViewMonth" onclick="setView('month')">📅 Mois</button>
        <button class="btn-view" id="btnViewStream" onclick="setView('stream')">📋 Planning</button>
        <button class="btn-view" id="btnViewYear" onclick="setView('year')">📆 Année</button>
        <button class="btn-view" id="btnViewTable" onclick="setView('table')">📋 Liste</button>
      </div>
    </div>

    <!-- VUE MENSUELLE (GRILLE) -->
    <div id="viewMonthContainer">
      <div class="calendar-grid-header">
        <div>Lun</div>
        <div>Mar</div>
        <div>Mer</div>
        <div>Jeu</div>
        <div>Ven</div>
        <div>Sam</div>
        <div>Dim</div>
      </div>
      <div class="calendar-grid" id="monthGrid"></div>
    </div>

    <!-- VUE PLANNING / AGENDA MOBILE (STREAM TACTILE) -->
    <div id="viewStreamContainer" style="display: none;">
      <div class="stream-container" id="streamList"></div>
    </div>

    <!-- VUE ANNUELLE GLOBALE -->
    <div id="viewYearContainer" style="display: none;">
      <div class="year-grid" id="yearGrid"></div>
    </div>

    <!-- VUE TABLEAU DES DEMANDES -->
    <div id="viewTableContainer" style="display: none;">
      <div class="demandes-table-container">
        <div class="table-toolbar">
          <div class="filter-pills">
            <button class="pill active" onclick="filterTable('all')">Tous (<span id="countTableAll">0</span>)</button>
            <button class="pill" onclick="filterTable('pending')">⏳ En attente (<span id="countTablePending">0</span>)</button>
            <button class="pill" onclick="filterTable('accepted')">✅ Acceptés (<span id="countTableAccepted">0</span>)</button>
            <button class="pill" onclick="filterTable('rejected')">❌ Refusés (<span id="countTableRejected">0</span>)</button>
            <button class="pill" onclick="filterTable('VT')">⏱️ VT</button>
            <button class="pill" onclick="filterTable('CA')">🏖️ Congés</button>
          </div>
          <div>
            <button class="btn btn-primary" onclick="window.print()">🖨️ Imprimer</button>
          </div>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Jour</th>
              <th>Type</th>
              <th>Poste Initial</th>
              <th>Statut</th>
              <th>Note</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="tableDemandesBody"></tbody>
        </table>
      </div>
    </div>

  </div>

  <!-- BARRE DE NAVIGATION INFÉRIEURE MOBILE -->
  <nav class="mobile-bottom-bar">
    <button class="bottom-bar-item active" id="bbarMonth" onclick="setView('month')">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
      <span>Grille</span>
    </button>
    <button class="bottom-bar-item" id="bbarStream" onclick="setView('stream')">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg>
      <span>Planning</span>
    </button>
    <button class="bottom-bar-item" id="bbarTable" onclick="setView('table')">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
      <span>Demandes</span>
    </button>
    <button class="bottom-bar-item" id="bbarSync" onclick="openSyncModal()">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
      <span>Sync Cloud</span>
    </button>
  </nav>

  <!-- MODAL ÉDITION JOUR (POSER VT / CONGÉ) -->
  <div class="modal-backdrop" id="dayModalBackdrop">
    <div class="modal-content">
      <div class="modal-header">
        <div class="modal-title" id="modalDayTitle">Détail du Jour</div>
        <button class="modal-close" onclick="closeDayModal()">&times;</button>
      </div>

      <div class="info-box" id="modalInfoBox"></div>

      <div class="form-group">
        <label class="form-label">Type d'absence souhaité :</label>
        <div class="choice-grid">
          <div class="choice-card" id="choiceVT" onclick="selectAbsenceType('VT')">
            <div class="choice-card-title" style="color: var(--color-vt);">⏱️ VT (Temps Partiel)</div>
            <div class="choice-card-desc">Déduit du quota VT</div>
          </div>
          <div class="choice-card" id="choiceConge" onclick="selectAbsenceType('CA')">
            <div class="choice-card-title" style="color: var(--color-conge);">🏖️ Congé Annuel</div>
            <div class="choice-card-desc">Déduit du quota Congés</div>
          </div>
        </div>
      </div>

      <div class="form-group" id="statusGroup" style="display: none;">
        <label class="form-label">Statut de la demande :</label>
        <div class="status-select-container">
          <button type="button" class="status-btn" id="btnStatusPending" onclick="selectStatus('pending')">
            ⏳ En attente
          </button>
          <button type="button" class="status-btn" id="btnStatusAccepted" onclick="selectStatus('accepted')">
            ✅ Accepté
          </button>
          <button type="button" class="status-btn" id="btnStatusRejected" onclick="selectStatus('rejected')">
            ❌ Refusé
          </button>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Note / Motif (optionnel) :</label>
        <input type="text" id="modalNoteInput" placeholder="Ex: Demande déposée le 10/01..." style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 0.95rem;">
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 14px; border-top: 1px solid var(--border-color);">
        <button class="btn btn-danger" id="btnDeleteAbsence" style="display: none;" onclick="deleteCurrentAbsence()">
          🗑️ Supprimer
        </button>
        <div style="display: flex; gap: 8px; margin-left: auto;">
          <button class="btn" style="background: #e2e8f0; color: #334155;" onclick="closeDayModal()">Fermer</button>
          <button class="btn btn-primary" id="btnSaveAbsence" onclick="saveAbsence()">Enregistrer</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL SYNCHRONISATION MULTI-APPAREILS -->
  <div class="modal-backdrop" id="syncModalBackdrop">
    <div class="modal-content">
      <div class="modal-header">
        <div class="modal-title">☁️ Synchronisation Cloud & Mobile</div>
        <button class="modal-close" onclick="closeSyncModal()">&times;</button>
      </div>

      <div class="sync-tabs">
        <button class="sync-tab-btn active" id="tabBtnPuter" onclick="setSyncTab('puter')">☁️ Cloud Direct (1 Clic)</button>
        <button class="sync-tab-btn" id="tabBtnFirebase" onclick="setSyncTab('firebase')">🔥 Firebase</button>
        <button class="sync-tab-btn" id="tabBtnQR" onclick="setSyncTab('qr')">📲 QR Code</button>
      </div>

      <!-- ONGLET PUTER CLOUD -->
      <div id="syncTabPuter">
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
          Synchronisation <strong>automatique dans les deux sens</strong> : toute modification sur votre smartphone s'affiche en direct sur votre ordinateur, et vice-versa.
        </p>

        <div class="info-box">
          <div class="info-box-row">
            <span>Statut Cloud :</span>
            <span id="puterStatusText" style="font-weight: 700; color: #d97706;">Non connecté</span>
          </div>
          <div class="info-box-row" id="puterUserRow" style="display: none;">
            <span>Connecté en tant que :</span>
            <span id="puterUserName" style="font-weight: 700;">—</span>
          </div>
          <div class="info-box-row">
            <span>Dernière synchro :</span>
            <span id="lastSyncTime" style="font-weight: 600;">—</span>
          </div>
        </div>

        <div style="display: flex; gap: 8px; flex-direction: column;">
          <button class="btn btn-success" id="btnPuterConnect" onclick="connectPuterCloud()" style="min-height: 44px;">
            🚀 Se connecter & Activer la synchro en direct
          </button>
          <button class="btn btn-primary" id="btnPuterManualSync" style="display:none; min-height: 44px;" onclick="syncWithPuter()">
            🔄 Forcer la synchronisation immédiate
          </button>
        </div>
      </div>

      <!-- ONGLET GOOGLE FIREBASE -->
      <div id="syncTabFirebase" style="display: none;">
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
          Utilisez votre propre base de données Google Firebase Realtime Database (100% gratuite).
        </p>
        <div class="form-group">
          <label class="form-label">URL de votre base Firebase :</label>
          <input type="text" id="firebaseDbUrl" placeholder="https://mon-projet-default-rtdb.europe-west1.firebasedatabase.app" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 0.85rem;">
        </div>
        <div class="form-group">
          <label class="form-label">Code secret / PIN (optionnel) :</label>
          <input type="password" id="firebaseSecretPin" placeholder="Ex: 1234" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 0.85rem;">
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-primary" onclick="saveFirebaseConfig()">Enregistrer</button>
          <button class="btn btn-success" onclick="syncWithFirebase()">🔄 Synchroniser</button>
        </div>
      </div>

      <!-- ONGLET QR CODE -->
      <div id="syncTabQR" style="display: none;">
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
          Scannez avec votre téléphone pour transférer toutes vos poses instantanément :
        </p>
        <div class="qr-container">
          <div id="qrcodeBox"></div>
          <div style="margin-top: 10px; font-size: 0.78rem; color: var(--text-muted);">
            Contient vos <span id="qrCountAbsences">0</span> demandes actuelles.
          </div>
        </div>
        <button class="btn btn-primary" style="width: 100%;" onclick="copySyncLink()">
          📋 Copier le lien magique
        </button>
      </div>

      <div style="text-align: right; margin-top: 20px; padding-top: 12px; border-top: 1px solid var(--border-color);">
        <button class="btn" style="background: #e2e8f0; color: #334155;" onclick="closeSyncModal()">Fermer</button>
      </div>
    </div>
  </div>

  <!-- MODAL CONFIGURATION QUOTAS & SAUVEGARDE -->
  <div class="modal-backdrop" id="settingsModalBackdrop">
    <div class="modal-content">
      <div class="modal-header">
        <div class="modal-title">⚙️ Quotas & Sauvegardes</div>
        <button class="modal-close" onclick="closeSettingsModal()">&times;</button>
      </div>

      <div class="form-group">
        <label class="form-label">Quota annuel de VT (Temps partiel) :</label>
        <input type="number" id="settingsQuotaVT" value="44" min="0" max="100" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 1rem; font-weight: 700;">
      </div>

      <div class="form-group">
        <label class="form-label">Quota annuel de Congés Annuels (CA) :</label>
        <input type="number" id="settingsQuotaConge" value="23" min="0" max="60" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 1rem; font-weight: 700;">
      </div>

      <div style="border-top: 1px solid var(--border-color); padding-top: 16px; margin-top: 16px;">
        <label class="form-label">Sauvegarde manuelle JSON :</label>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button class="btn btn-success" onclick="exportBackupJSON()">💾 Télécharger</button>
          <label class="btn btn-primary" style="margin: 0; cursor: pointer;">
            📂 Restaurer <input type="file" id="importFileInput" accept=".json" style="display: none;" onchange="importBackupJSON(event)">
          </label>
          <button class="btn btn-danger" onclick="resetAllData()">⚠️ Réinitialiser</button>
        </div>
      </div>

      <div style="text-align: right; margin-top: 24px;">
        <button class="btn btn-primary" onclick="saveSettings()">Valider</button>
      </div>
    </div>
  </div>

  <!-- QR CODE LIBRARY EMBEDDED -->
  <script>
    ___QRCODE_JS___
  </script>

  <!-- APPLICATION LOGIC -->
  <script>
    const RAW_DAYS_DATA = ___DAYS_JSON___;

    const MONTH_NAMES = [
      "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ];

    let currentMonth = 1;
    let currentView = 'month'; // 'month', 'stream', 'year', 'table'
    let quotaVT = 44;
    let quotaConge = 23;
    let tableFilter = 'all';

    let userAbsences = {};

    let selectedDayRecord = null;
    let tempAbsenceType = null;
    let tempStatus = 'pending';

    let isPuterConnected = false;
    let firebaseConfig = { url: '', pin: '' };

    window.addEventListener('DOMContentLoaded', () => {
      loadSavedData();
      checkUrlSyncPayload();
      initPuterState();
      renderMonthNav();
      updateAllStats();
      renderCurrentView();

      // AUTO-SYNC EN DIRECT LORSQUE L'UTILISATEUR REVIENT SUR L'ONGLET
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
          syncWithCloudSilently();
        }
      });
      window.addEventListener('focus', () => {
        syncWithCloudSilently();
      });

      // HEARTBEAT POLLING TOUTES LES 10 SECONDES POUR RECUPERER LES MODIFICATIONS FAITES SUR LE TELEPHONE
      setInterval(() => {
        if (document.visibilityState === 'visible') {
          syncWithCloudSilently();
        }
      }, 10000);
    });

    function showToast(msg, icon = '✅') {
      const box = document.getElementById('toastBox');
      document.getElementById('toastMsg').innerText = msg;
      document.getElementById('toastIcon').innerText = icon;
      box.classList.add('show');
      setTimeout(() => box.classList.remove('show'), 3500);
    }

    function checkUrlSyncPayload() {
      const hash = window.location.hash;
      const params = new URLSearchParams(window.location.search);
      let syncRaw = null;

      if (hash && hash.startsWith('#sync=')) {
        syncRaw = hash.replace('#sync=', '');
      } else if (params.get('sync')) {
        syncRaw = params.get('sync');
      }

      if (syncRaw) {
        try {
          const decoded = JSON.parse(decodeURIComponent(escape(atob(syncRaw))));
          if (decoded.v !== undefined) quotaVT = decoded.v;
          if (decoded.c !== undefined) quotaConge = decoded.c;
          if (decoded.a !== undefined) userAbsences = decoded.a;

          saveData();
          showToast("Synchronisation réussie ! Données importées.");
          window.history.replaceState(null, null, window.location.pathname);
        } catch(e) {
          console.error("Erreur de décodage sync", e);
        }
      }
    }

    function generateSyncUrl() {
      const minimalPayload = { v: quotaVT, c: quotaConge, a: userAbsences };
      const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(minimalPayload))));
      const baseUrl = window.location.origin + window.location.pathname;
      return `${baseUrl}#sync=${b64}`;
    }

    function loadSavedData() {
      const savedVT = localStorage.getItem('sncf_roulement_quota_vt');
      const savedConge = localStorage.getItem('sncf_roulement_quota_conge');
      const savedAbsences = localStorage.getItem('sncf_roulement_absences');
      const savedFb = localStorage.getItem('sncf_roulement_firebase');

      if (savedVT !== null) quotaVT = parseInt(savedVT, 10);
      if (savedConge !== null) quotaConge = parseInt(savedConge, 10);
      if (savedAbsences !== null) {
        try { userAbsences = JSON.parse(savedAbsences); } catch(e) {}
      }
      if (savedFb !== null) {
        try {
          firebaseConfig = JSON.parse(savedFb);
          document.getElementById('firebaseDbUrl').value = firebaseConfig.url || '';
          document.getElementById('firebaseSecretPin').value = firebaseConfig.pin || '';
        } catch(e) {}
      }

      document.getElementById('inputQuotaVT').value = quotaVT;
      document.getElementById('inputQuotaConge').value = quotaConge;
      document.getElementById('settingsQuotaVT').value = quotaVT;
      document.getElementById('settingsQuotaConge').value = quotaConge;
    }

    function saveData() {
      localStorage.setItem('sncf_roulement_quota_vt', quotaVT);
      localStorage.setItem('sncf_roulement_quota_conge', quotaConge);
      localStorage.setItem('sncf_roulement_absences', JSON.stringify(userAbsences));
      autoSyncCloud();
    }

    // CLOUD SYNC AUTOMATIQUE
    async function initPuterState() {
      if (typeof puter !== 'undefined' && puter.auth) {
        if (puter.auth.isSignedIn()) {
          isPuterConnected = true;
          const user = await puter.auth.getUser();
          document.getElementById('puterStatusText').innerText = "Connecté en direct ✅";
          document.getElementById('puterStatusText').style.color = "#059669";
          document.getElementById('puterUserName').innerText = user.username || 'Utilisateur Puter';
          document.getElementById('puterUserRow').style.display = 'flex';
          document.getElementById('btnPuterConnect').style.display = 'none';
          document.getElementById('btnPuterManualSync').style.display = 'block';
          document.getElementById('syncIndicator').style.background = '#10b981';
          syncWithPuter(true);
        }
      }
    }

    async function connectPuterCloud() {
      if (typeof puter === 'undefined') {
        alert("Puter.js indisponible.");
        return;
      }
      try {
        await puter.auth.signIn();
        initPuterState();
        showToast("Synchronisation Cloud Puter activée !");
      } catch(err) {
        alert("Connexion Puter annulée.");
      }
    }

    async function syncWithPuter(silent = false) {
      if (!isPuterConnected) return;
      try {
        const cloudDataStr = await puter.kv.get('sncf_roulement_2027');
        if (cloudDataStr) {
          const cloudData = JSON.parse(cloudDataStr);
          if (cloudData.updatedAt) {
            const localUpdated = parseInt(localStorage.getItem('sncf_roulement_updated_at') || '0', 10);
            if (cloudData.updatedAt > localUpdated) {
              quotaVT = cloudData.quotaVT || quotaVT;
              quotaConge = cloudData.quotaConge || quotaConge;
              userAbsences = cloudData.absences || userAbsences;
              localStorage.setItem('sncf_roulement_quota_vt', quotaVT);
              localStorage.setItem('sncf_roulement_quota_conge', quotaConge);
              localStorage.setItem('sncf_roulement_absences', JSON.stringify(userAbsences));
              localStorage.setItem('sncf_roulement_updated_at', cloudData.updatedAt);
              updateAllStats();
              renderCurrentView();
              updateLastSyncLabel();
              if (!silent) showToast("Synchronisé avec le Cloud !");
              return;
            }
          }
        }
        await autoSyncCloud();
        updateLastSyncLabel();
        if (!silent) showToast("Sauvegardé sur le Cloud !");
      } catch(e) {
        console.error("Sync error", e);
      }
    }

    function syncWithCloudSilently() {
      if (isPuterConnected) {
        syncWithPuter(true);
      }
      if (firebaseConfig.url) {
        syncWithFirebaseSilently();
      }
    }

    function updateLastSyncLabel() {
      const nowStr = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
      const el = document.getElementById('lastSyncTime');
      if (el) el.innerText = nowStr;
    }

    function autoSyncCloud() {
      const now = Date.now();
      localStorage.setItem('sncf_roulement_updated_at', now);
      const payload = {
        quotaVT: quotaVT,
        quotaConge: quotaConge,
        absences: userAbsences,
        updatedAt: now
      };

      if (isPuterConnected && typeof puter !== 'undefined') {
        puter.kv.set('sncf_roulement_2027', JSON.stringify(payload)).then(() => updateLastSyncLabel()).catch(e => console.error(e));
      }

      if (firebaseConfig.url) {
        const cleanBase = firebaseConfig.url.endsWith('/') ? firebaseConfig.url.slice(0, -1) : firebaseConfig.url;
        const endpoint = cleanBase + '/roulement_2027.json' + (firebaseConfig.pin ? '?auth=' + firebaseConfig.pin : '');
        fetch(endpoint, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(() => updateLastSyncLabel()).catch(e => console.error(e));
      }
    }

    async function syncWithFirebaseSilently() {
      if (!firebaseConfig.url) return;
      const cleanBase = firebaseConfig.url.endsWith('/') ? firebaseConfig.url.slice(0, -1) : firebaseConfig.url;
      const endpoint = cleanBase + '/roulement_2027.json' + (firebaseConfig.pin ? '?auth=' + firebaseConfig.pin : '');
      try {
        const res = await fetch(endpoint);
        const data = await res.json();
        if (data && data.updatedAt) {
          const localUpdated = parseInt(localStorage.getItem('sncf_roulement_updated_at') || '0', 10);
          if (data.updatedAt > localUpdated) {
            quotaVT = data.quotaVT || quotaVT;
            quotaConge = data.quotaConge || quotaConge;
            userAbsences = data.absences || userAbsences;
            localStorage.setItem('sncf_roulement_quota_vt', quotaVT);
            localStorage.setItem('sncf_roulement_quota_conge', quotaConge);
            localStorage.setItem('sncf_roulement_absences', JSON.stringify(userAbsences));
            localStorage.setItem('sncf_roulement_updated_at', data.updatedAt);
            updateAllStats();
            renderCurrentView();
            updateLastSyncLabel();
          }
        }
      } catch(e) {}
    }

    function saveFirebaseConfig() {
      const url = document.getElementById('firebaseDbUrl').value.trim();
      const pin = document.getElementById('firebaseSecretPin').value.trim();
      firebaseConfig = { url, pin };
      localStorage.setItem('sncf_roulement_firebase', JSON.stringify(firebaseConfig));
      autoSyncCloud();
      showToast("Firebase configuré !");
    }

    async function syncWithFirebase() {
      if (!firebaseConfig.url) {
        alert("Renseignez l'URL Firebase.");
        return;
      }
      await syncWithFirebaseSilently();
      showToast("Synchronisé avec Firebase !");
    }

    function updateQuotas() {
      const newVT = parseInt(document.getElementById('inputQuotaVT').value, 10);
      const newConge = parseInt(document.getElementById('inputQuotaConge').value, 10);
      if (!isNaN(newVT)) quotaVT = newVT;
      if (!isNaN(newConge)) quotaConge = newConge;
      document.getElementById('settingsQuotaVT').value = quotaVT;
      document.getElementById('settingsQuotaConge').value = quotaConge;
      saveData();
      updateAllStats();
      renderCurrentView();
    }

    function updateAllStats() {
      let vtPending = 0, vtAccepted = 0, vtRejected = 0;
      let congePending = 0, congeAccepted = 0, congeRejected = 0;

      Object.values(userAbsences).forEach(abs => {
        if (abs.type === 'VT') {
          if (abs.status === 'pending') vtPending++;
          else if (abs.status === 'accepted') vtAccepted++;
          else if (abs.status === 'rejected') vtRejected++;
        } else if (abs.type === 'CA') {
          if (abs.status === 'pending') congePending++;
          else if (abs.status === 'accepted') congeAccepted++;
          else if (abs.status === 'rejected') congeRejected++;
        }
      });

      const vtRemaining = Math.max(0, quotaVT - vtAccepted - vtPending);
      const congeRemaining = Math.max(0, quotaConge - congeAccepted - congePending);

      document.getElementById('statVTPending').innerText = vtPending;
      document.getElementById('statVTAccepted').innerText = vtAccepted;
      document.getElementById('statVTRemaining').innerText = vtRemaining;
      document.getElementById('statVTRejected').innerText = vtRejected;

      document.getElementById('statCongePending').innerText = congePending;
      document.getElementById('statCongeAccepted').innerText = congeAccepted;
      document.getElementById('statCongeRemaining').innerText = congeRemaining;
      document.getElementById('statCongeRejected').innerText = congeRejected;

      const vtAccPct = Math.min(100, (vtAccepted / quotaVT) * 100);
      const vtPendPct = Math.min(100 - vtAccPct, (vtPending / quotaVT) * 100);
      document.getElementById('barVTAccepted').style.width = vtAccPct + '%';
      document.getElementById('barVTPending').style.width = vtPendPct + '%';

      const congeAccPct = Math.min(100, (congeAccepted / quotaConge) * 100);
      const congePendPct = Math.min(100 - congeAccPct, (congePending / quotaConge) * 100);
      document.getElementById('barCongeAccepted').style.width = congeAccPct + '%';
      document.getElementById('barCongePending').style.width = congePendPct + '%';

      const workReal = 232 - (vtAccepted + congeAccepted);
      document.getElementById('statWorkReal').innerText = workReal;

      const totalDemandes = Object.keys(userAbsences).length;
      document.getElementById('countTableAll').innerText = totalDemandes;
      document.getElementById('countTablePending').innerText = vtPending + congePending;
      document.getElementById('countTableAccepted').innerText = vtAccepted + congeAccepted;
      document.getElementById('countTableRejected').innerText = vtRejected + congeRejected;
    }

    function renderMonthNav() {
      const navContainer = document.getElementById('monthNavButtons');
      navContainer.innerHTML = '';
      MONTH_NAMES.forEach((mName, idx) => {
        const btn = document.createElement('button');
        btn.className = `btn-month ${currentMonth === (idx + 1) ? 'active' : ''}`;
        btn.innerText = mName;
        btn.onclick = () => {
          currentMonth = idx + 1;
          renderMonthNav();
          renderCurrentView();
        };
        navContainer.appendChild(btn);
      });
    }

    function setView(view) {
      currentView = view;
      document.getElementById('btnViewMonth').classList.toggle('active', view === 'month');
      document.getElementById('btnViewStream').classList.toggle('active', view === 'stream');
      document.getElementById('btnViewYear').classList.toggle('active', view === 'year');
      document.getElementById('btnViewTable').classList.toggle('active', view === 'table');

      document.getElementById('bbarMonth').classList.toggle('active', view === 'month');
      document.getElementById('bbarStream').classList.toggle('active', view === 'stream');
      document.getElementById('bbarTable').classList.toggle('active', view === 'table');

      document.getElementById('viewMonthContainer').style.display = view === 'month' ? 'block' : 'none';
      document.getElementById('viewStreamContainer').style.display = view === 'stream' ? 'block' : 'none';
      document.getElementById('viewYearContainer').style.display = view === 'year' ? 'block' : 'none';
      document.getElementById('viewTableContainer').style.display = view === 'table' ? 'block' : 'none';

      renderCurrentView();
    }

    function renderCurrentView() {
      if (currentView === 'month') renderMonthView();
      else if (currentView === 'stream') renderStreamView();
      else if (currentView === 'year') renderYearView();
      else if (currentView === 'table') renderTableView();
    }

    // VUE MENSUELLE (GRILLE)
    function renderMonthView() {
      const grid = document.getElementById('monthGrid');
      grid.innerHTML = '';

      const monthDays = RAW_DAYS_DATA.filter(d => d.month === currentMonth);
      if (monthDays.length === 0) return;

      const firstWeekday = monthDays[0].weekdayIndex;
      for (let i = 0; i < firstWeekday; i++) {
        const empty = document.createElement('div');
        empty.className = 'day-cell is-empty';
        grid.appendChild(empty);
      }

      monthDays.forEach(dayRec => {
        const cell = document.createElement('div');
        cell.className = 'day-cell';
        if (dayRec.isWeekend) cell.classList.add('is-weekend');
        if (dayRec.isHoliday) cell.classList.add('is-holiday');

        const abs = userAbsences[dayRec.date];
        if (abs) {
          if (abs.type === 'VT') {
            if (abs.status === 'pending') cell.classList.add('has-vt-pending');
            else if (abs.status === 'accepted') cell.classList.add('has-vt-accepted');
            else if (abs.status === 'rejected') cell.classList.add('has-vt-rejected');
          } else if (abs.type === 'CA') {
            if (abs.status === 'pending') cell.classList.add('has-conge-pending');
            else if (abs.status === 'accepted') cell.classList.add('has-conge-accepted');
            else if (abs.status === 'rejected') cell.classList.add('has-conge-rejected');
          }
        }

        let shiftBadgeClass = 'badge-rp';
        if (dayRec.baseCode === 'TNY002') shiftBadgeClass = 'badge-tny002';
        else if (dayRec.baseCode === 'TNY003') shiftBadgeClass = 'badge-tny003';
        else if (dayRec.baseCode === 'TNY004') shiftBadgeClass = 'badge-tny004';
        else if (dayRec.baseCode === 'RU') shiftBadgeClass = 'badge-ru';

        let overrideHtml = '';
        if (abs) {
          let label = abs.type === 'VT' ? 'VT' : 'Congé';
          let statusLabel = '';
          let badgeClass = '';
          if (abs.status === 'pending') {
            statusLabel = '⏳ Posé';
            badgeClass = abs.type === 'VT' ? 'badge-vt-pending' : 'badge-conge-pending';
          } else if (abs.status === 'accepted') {
            statusLabel = '✅ Validé';
            badgeClass = abs.type === 'VT' ? 'badge-vt-accepted' : 'badge-conge-accepted';
          } else if (abs.status === 'rejected') {
            statusLabel = '❌ Refusé';
            badgeClass = abs.type === 'VT' ? 'badge-vt-rejected' : 'badge-conge-rejected';
          }
          overrideHtml = `<div class="day-override-badge ${badgeClass}">
            <span>${label}</span>
            <span>${statusLabel}</span>
          </div>`;
        }

        cell.innerHTML = `
          <div>
            <div class="day-cell-top">
              <span class="day-num">${dayRec.day}</span>
              ${dayRec.isHoliday ? `<span class="holiday-badge" title="${dayRec.holidayName}">${dayRec.holidayName}</span>` : ''}
            </div>
            <div>
              <span class="day-shift-badge ${shiftBadgeClass}">${dayRec.baseCode}</span>
            </div>
            ${dayRec.hoursLabel ? `<div class="day-hours">${dayRec.hoursLabel}</div>` : '<div class="day-hours" style="opacity:0.6;">Repos</div>'}
          </div>
          <div>${overrideHtml}</div>
        `;

        cell.onclick = () => openDayModal(dayRec);
        grid.appendChild(cell);
      });
    }

    // VUE PLANNING / AGENDA MOBILE STREAM (GRAND FORMAT LISIBLE)
    function renderStreamView() {
      const container = document.getElementById('streamList');
      container.innerHTML = '';

      const monthDays = RAW_DAYS_DATA.filter(d => d.month === currentMonth);
      if (monthDays.length === 0) return;

      monthDays.forEach(d => {
        const card = document.createElement('div');
        card.className = 'stream-card';
        if (d.isWeekend) card.classList.add('is-weekend');
        if (d.isHoliday) card.classList.add('is-holiday');

        const abs = userAbsences[d.date];

        let rightBadgeHtml = '<button class="btn btn-primary" style="padding: 4px 10px; font-size: 0.78rem;">Poser</button>';
        if (abs) {
          if (abs.type === 'VT') {
            if (abs.status === 'pending') rightBadgeHtml = '<span class="stream-badge-state" style="background:#fef3c7; color:#92400e; border:1px solid #fcd34d;">⏳ VT Posé</span>';
            else if (abs.status === 'accepted') rightBadgeHtml = '<span class="stream-badge-state" style="background:#d1fae5; color:#065f46; border:1px solid #a7f3d0;">✅ VT Validé</span>';
            else if (abs.status === 'rejected') rightBadgeHtml = '<span class="stream-badge-state" style="background:#fee2e2; color:#991b1b; border:1px solid #fca5a5;">❌ Refusé</span>';
          } else {
            if (abs.status === 'pending') rightBadgeHtml = '<span class="stream-badge-state" style="background:#fef3c7; color:#92400e; border:1px solid #fcd34d;">⏳ Congé Posé</span>';
            else if (abs.status === 'accepted') rightBadgeHtml = '<span class="stream-badge-state" style="background:#dbeafe; color:#1e40af; border:1px solid #bfdbfe;">🏖️ Congé Validé</span>';
            else if (abs.status === 'rejected') rightBadgeHtml = '<span class="stream-badge-state" style="background:#fee2e2; color:#991b1b; border:1px solid #fca5a5;">❌ Refusé</span>';
          }
        }

        let shiftBadgeClass = 'badge-rp';
        if (d.baseCode === 'TNY002') shiftBadgeClass = 'badge-tny002';
        else if (d.baseCode === 'TNY003') shiftBadgeClass = 'badge-tny003';
        else if (d.baseCode === 'TNY004') shiftBadgeClass = 'badge-tny004';
        else if (d.baseCode === 'RU') shiftBadgeClass = 'badge-ru';

        card.innerHTML = `
          <div class="stream-left">
            <div class="stream-date-badge">
              <span class="stream-weekday">${d.weekdayShort}</span>
              <span class="stream-daynum">${d.day}</span>
            </div>
            <div class="stream-info">
              <div class="stream-shift-row">
                <span class="day-shift-badge ${shiftBadgeClass}" style="margin:0;">${d.baseCode}</span>
                <span class="stream-hours">${d.hoursLabel || 'Jour de repos'}</span>
              </div>
              <div class="stream-meta">
                ${d.isHoliday ? '🎉 ' + d.holidayName : (d.isWeekend ? 'Week-end' : 'Semaine')}
                ${abs && abs.note ? ' • <i>' + abs.note + '</i>' : ''}
              </div>
            </div>
          </div>
          <div class="stream-right">
            ${rightBadgeHtml}
          </div>
        `;

        card.onclick = () => openDayModal(d);
        container.appendChild(card);
      });
    }

    function renderYearView() {
      const yearContainer = document.getElementById('yearGrid');
      yearContainer.innerHTML = '';

      for (let m = 1; m <= 12; m++) {
        const mDays = RAW_DAYS_DATA.filter(d => d.month === m);
        const card = document.createElement('div');
        card.className = 'year-month-card';

        const title = document.createElement('div');
        title.className = 'year-month-title';
        title.innerText = MONTH_NAMES[m - 1];
        card.appendChild(title);

        const calGrid = document.createElement('div');
        calGrid.className = 'year-month-calendar';

        const firstWeekday = mDays[0].weekdayIndex;
        for (let i = 0; i < firstWeekday; i++) {
          const emp = document.createElement('div');
          emp.className = 'year-mini-day';
          calGrid.appendChild(emp);
        }

        mDays.forEach(d => {
          const miniDay = document.createElement('div');
          miniDay.className = 'year-mini-day';
          miniDay.innerText = d.day;
          miniDay.title = `${d.day} ${MONTH_NAMES[m-1]} : ${d.baseCode} ${d.hoursLabel ? '('+d.hoursLabel+')' : ''}`;

          const abs = userAbsences[d.date];
          if (abs) {
            if (abs.type === 'VT') {
              miniDay.style.background = abs.status === 'accepted' ? '#10b981' : (abs.status === 'pending' ? '#f59e0b' : '#ef4444');
              miniDay.style.color = 'white';
            } else {
              miniDay.style.background = abs.status === 'accepted' ? '#3b82f6' : (abs.status === 'pending' ? '#f59e0b' : '#ef4444');
              miniDay.style.color = 'white';
            }
          } else if (d.isWork) {
            miniDay.style.background = '#e0f2fe';
            miniDay.style.color = '#0369a1';
          } else {
            miniDay.style.background = '#f1f5f9';
            miniDay.style.color = '#94a3b8';
          }

          miniDay.onclick = () => openDayModal(d);
          calGrid.appendChild(miniDay);
        });

        card.appendChild(calGrid);
        yearContainer.appendChild(card);
      }
    }

    function filterTable(filter) {
      tableFilter = filter;
      document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');
      renderTableView();
    }

    function renderTableView() {
      const tbody = document.getElementById('tableDemandesBody');
      tbody.innerHTML = '';

      const datesWithAbs = Object.keys(userAbsences).sort();
      if (datesWithAbs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 30px;">Aucune demande posée pour le moment. Cliquez sur un jour du calendrier.</td></tr>`;
        return;
      }

      datesWithAbs.forEach(dateStr => {
        const abs = userAbsences[dateStr];
        const dayRec = RAW_DAYS_DATA.find(d => d.date === dateStr);
        if (!dayRec) return;

        if (tableFilter === 'pending' && abs.status !== 'pending') return;
        if (tableFilter === 'accepted' && abs.status !== 'accepted') return;
        if (tableFilter === 'rejected' && abs.status !== 'rejected') return;
        if (tableFilter === 'VT' && abs.type !== 'VT') return;
        if (tableFilter === 'CA' && abs.type !== 'CA') return;

        const tr = document.createElement('tr');

        let statusBadge = '';
        if (abs.status === 'pending') statusBadge = '<span style="background: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 4px; font-weight:700;">⏳ En attente</span>';
        else if (abs.status === 'accepted') statusBadge = '<span style="background: #d1fae5; color: #065f46; padding: 4px 8px; border-radius: 4px; font-weight:700;">✅ Accepté</span>';
        else if (abs.status === 'rejected') statusBadge = '<span style="background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; font-weight:700;">❌ Refusé</span>';

        const typeLabel = abs.type === 'VT' 
          ? '<span style="font-weight:700; color: var(--color-vt);">⏱️ VT (Temps partiel)</span>' 
          : '<span style="font-weight:700; color: var(--color-conge);">🏖️ Congé Annuel</span>';

        tr.innerHTML = `
          <td style="font-weight: 700;">${dateStr}</td>
          <td>${dayRec.weekday}</td>
          <td>${typeLabel}</td>
          <td><span class="day-shift-badge ${dayRec.baseCode.startsWith('TNY') ? 'badge-'+dayRec.baseCode.toLowerCase() : 'badge-rp'}" style="margin:0;">${dayRec.baseCode}</span> ${dayRec.hoursLabel}</td>
          <td>${statusBadge}</td>
          <td style="color: var(--text-muted);">${abs.note || '—'}</td>
          <td>
            <div style="display: flex; gap: 6px;">
              ${abs.status !== 'accepted' ? `<button class="btn btn-success" style="padding: 4px 8px; font-size: 0.75rem;" onclick="setAbsenceStatus('${dateStr}', 'accepted')">Valider ✅</button>` : ''}
              ${abs.status !== 'rejected' ? `<button class="btn btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="setAbsenceStatus('${dateStr}', 'rejected')">Refuser ❌</button>` : ''}
              <button class="btn" style="background: #e2e8f0; padding: 4px 8px; font-size: 0.75rem;" onclick="removeAbsence('${dateStr}')">🗑️</button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function setAbsenceStatus(dateStr, newStatus) {
      if (userAbsences[dateStr]) {
        userAbsences[dateStr].status = newStatus;
        saveData();
        updateAllStats();
        renderCurrentView();
        showToast(`Statut mis à jour : ${newStatus === 'accepted' ? 'Accepté' : 'Refusé'}`);
      }
    }

    function removeAbsence(dateStr) {
      if (confirm(`Voulez-vous supprimer la demande pour le ${dateStr} ?`)) {
        delete userAbsences[dateStr];
        saveData();
        updateAllStats();
        renderCurrentView();
        showToast("Demande supprimée.");
      }
    }

    function openDayModal(dayRec) {
      selectedDayRecord = dayRec;
      const abs = userAbsences[dayRec.date];

      document.getElementById('modalDayTitle').innerText = `${dayRec.weekday} ${dayRec.day} ${MONTH_NAMES[dayRec.month - 1]} 2027`;
      
      let infoHtml = `
        <div class="info-box-row">
          <span><strong>Poste du roulement :</strong></span>
          <span><strong>${dayRec.baseCode}</strong></span>
        </div>
        <div class="info-box-row">
          <span>Horaires prévus :</span>
          <span>${dayRec.hoursLabel || 'Jour de repos'}</span>
        </div>
        <div class="info-box-row">
          <span>Régime :</span>
          <span>${dayRec.isHoliday ? '🎉 Jour Férié (' + dayRec.holidayName + ')' : (dayRec.isWeekend ? 'Week-end' : 'Semaine normal')}</span>
        </div>
      `;
      document.getElementById('modalInfoBox').innerHTML = infoHtml;

      if (abs) {
        tempAbsenceType = abs.type;
        tempStatus = abs.status;
        document.getElementById('modalNoteInput').value = abs.note || '';
        document.getElementById('btnDeleteAbsence').style.display = 'inline-flex';
      } else {
        tempAbsenceType = null;
        tempStatus = 'pending';
        document.getElementById('modalNoteInput').value = '';
        document.getElementById('btnDeleteAbsence').style.display = 'none';
      }

      updateModalUI();
      document.getElementById('dayModalBackdrop').classList.add('open');
    }

    function closeDayModal() {
      document.getElementById('dayModalBackdrop').classList.remove('open');
      selectedDayRecord = null;
    }

    function selectAbsenceType(type) {
      tempAbsenceType = type;
      updateModalUI();
    }

    function selectStatus(st) {
      tempStatus = st;
      updateModalUI();
    }

    function updateModalUI() {
      const choiceVT = document.getElementById('choiceVT');
      const choiceConge = document.getElementById('choiceConge');
      const statusGroup = document.getElementById('statusGroup');

      choiceVT.classList.toggle('selected-vt', tempAbsenceType === 'VT');
      choiceConge.classList.toggle('selected-conge', tempAbsenceType === 'CA');

      if (tempAbsenceType) {
        statusGroup.style.display = 'block';
        document.getElementById('btnStatusPending').classList.toggle('selected', tempStatus === 'pending');
        document.getElementById('btnStatusAccepted').classList.toggle('selected', tempStatus === 'accepted');
        document.getElementById('btnStatusRejected').classList.toggle('selected', tempStatus === 'rejected');
      } else {
        statusGroup.style.display = 'none';
      }
    }

    function saveAbsence() {
      if (!selectedDayRecord) return;
      if (!tempAbsenceType) {
        alert("Veuillez choisir VT ou Congé.");
        return;
      }

      userAbsences[selectedDayRecord.date] = {
        type: tempAbsenceType,
        status: tempStatus,
        note: document.getElementById('modalNoteInput').value.trim()
      };

      saveData();
      updateAllStats();
      closeDayModal();
      renderCurrentView();
      showToast("Demande enregistrée & synchronisée !");
    }

    function deleteCurrentAbsence() {
      if (!selectedDayRecord) return;
      delete userAbsences[selectedDayRecord.date];
      saveData();
      updateAllStats();
      closeDayModal();
      renderCurrentView();
      showToast("Absence supprimée.");
    }

    // MODAL SYNC
    let qrInstance = null;
    function openSyncModal() {
      generateQRCode();
      document.getElementById('syncModalBackdrop').classList.add('open');
    }

    function closeSyncModal() {
      document.getElementById('syncModalBackdrop').classList.remove('open');
    }

    function setSyncTab(tab) {
      document.getElementById('tabBtnPuter').classList.toggle('active', tab === 'puter');
      document.getElementById('tabBtnFirebase').classList.toggle('active', tab === 'firebase');
      document.getElementById('tabBtnQR').classList.toggle('active', tab === 'qr');

      document.getElementById('syncTabPuter').style.display = tab === 'puter' ? 'block' : 'none';
      document.getElementById('syncTabFirebase').style.display = tab === 'firebase' ? 'block' : 'none';
      document.getElementById('syncTabQR').style.display = tab === 'qr' ? 'block' : 'none';

      if (tab === 'qr') generateQRCode();
    }

    function generateQRCode() {
      const box = document.getElementById('qrcodeBox');
      box.innerHTML = '';
      const syncUrl = generateSyncUrl();
      const count = Object.keys(userAbsences).length;
      document.getElementById('qrCountAbsences').innerText = count;

      try {
        qrInstance = new QRCode(box, {
          text: syncUrl,
          width: 200,
          height: 200,
          colorDark: "#0f172a",
          colorLight: "#ffffff",
          correctLevel: QRCode.CorrectLevel.M
        });
      } catch(e) {}
    }

    function copySyncLink() {
      const syncUrl = generateSyncUrl();
      navigator.clipboard.writeText(syncUrl).then(() => {
        showToast("Lien magique copié !");
      }).catch(() => {
        prompt("Copiez le lien ci-dessous :", syncUrl);
      });
    }

    // MODAL PARAMÈTRES
    function openSettingsModal() {
      document.getElementById('settingsQuotaVT').value = quotaVT;
      document.getElementById('settingsQuotaConge').value = quotaConge;
      document.getElementById('settingsModalBackdrop').classList.add('open');
    }

    function closeSettingsModal() {
      document.getElementById('settingsModalBackdrop').classList.remove('open');
    }

    function saveSettings() {
      const newVT = parseInt(document.getElementById('settingsQuotaVT').value, 10);
      const newConge = parseInt(document.getElementById('settingsQuotaConge').value, 10);
      if (!isNaN(newVT)) quotaVT = newVT;
      if (!isNaN(newConge)) quotaConge = newConge;
      document.getElementById('inputQuotaVT').value = quotaVT;
      document.getElementById('inputQuotaConge').value = quotaConge;
      saveData();
      updateAllStats();
      closeSettingsModal();
      renderCurrentView();
      showToast("Paramètres sauvegardés !");
    }

    function resetAllData() {
      if (confirm("Supprimer toutes vos demandes de congés et VT ?")) {
        userAbsences = {};
        quotaVT = 44;
        quotaConge = 23;
        saveData();
        loadSavedData();
        updateAllStats();
        closeSettingsModal();
        renderCurrentView();
        showToast("Données réinitialisées.");
      }
    }

    function exportBackupJSON() {
      const exportObj = {
        quotaVT: quotaVT,
        quotaConge: quotaConge,
        absences: userAbsences,
        exportedAt: new Date().toISOString()
      };
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj, null, 2));
      const a = document.createElement('a');
      a.href = dataStr;
      a.download = "sauvegarde_roulement_2027.json";
      a.click();
    }

    function importBackupJSON(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target.result);
          if (imported.quotaVT !== undefined) quotaVT = imported.quotaVT;
          if (imported.quotaConge !== undefined) quotaConge = imported.quotaConge;
          if (imported.absences !== undefined) userAbsences = imported.absences;
          saveData();
          loadSavedData();
          updateAllStats();
          closeSettingsModal();
          renderCurrentView();
          showToast("Sauvegarde importée avec succès !");
        } catch(err) {
          alert("Fichier JSON invalide.");
        }
      };
      reader.readAsText(file);
    }

    function exportUpdatedICS() {
      let icsContent = "BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//SNCF//Roulement 2027 Personnalise//FR\\r\\nCALSCALE:GREGORIAN\\r\\nMETHOD:PUBLISH\\r\\nX-WR-CALNAME:Roulement SNCF 2027 (Avec VT et Conges)\\r\\nX-WR-TIMEZONE:Europe/Paris\\r\\n";
      const nowUtc = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

      RAW_DAYS_DATA.forEach(d => {
        const abs = userAbsences[d.date];
        const dateClean = d.date.replace(/-/g, "");

        if (abs && abs.status === 'accepted') {
          const nextDay = new Date(d.date);
          nextDay.setDate(nextDay.getDate() + 1);
          const nextDayStr = nextDay.toISOString().slice(0, 10).replace(/-/g, "");
          const label = abs.type === 'VT' ? 'VT (Temps Partiel)' : 'Congé Annuel';

          icsContent += "BEGIN:VEVENT\\r\\n";
          icsContent += `UID:sncf-${dateClean}-abs@roulement2027\\r\\n`;
          icsContent += `DTSTAMP:${nowUtc}\\r\\n`;
          icsContent += `DTSTART;VALUE=DATE:${dateClean}\\r\\n`;
          icsContent += `DTEND;VALUE=DATE:${nextDayStr}\\r\\n`;
          icsContent += `SUMMARY:${label}\\r\\n`;
          icsContent += `DESCRIPTION:Jour d'absence validé (${label})\\nPoste initial : ${d.baseCode}\\r\\n`;
          icsContent += "STATUS:CONFIRMED\\r\\nTRANSP:TRANSPARENT\\r\\nEND:VEVENT\\r\\n";
        } else if (d.isWork) {
          const startTimeParts = d.startTime.split(":");
          const endTimeParts = d.endTime.split(":");
          const dtStart = `${dateClean}T${startTimeParts[0]}${startTimeParts[1]}00`;

          let dtEnd = "";
          if (d.endTime === "00:00") {
            const nextDay = new Date(d.date);
            nextDay.setDate(nextDay.getDate() + 1);
            const nextDayStr = nextDay.toISOString().slice(0, 10).replace(/-/g, "");
            dtEnd = `${nextDayStr}T000000`;
          } else {
            dtEnd = `${dateClean}T${endTimeParts[0]}${endTimeParts[1]}00`;
          }

          let summaryExtra = "";
          if (abs && abs.status === 'pending') {
            summaryExtra = ` [${abs.type === 'VT' ? 'VT' : 'Congé'} POSÉ EN ATTENTE]`;
          }

          icsContent += "BEGIN:VEVENT\\r\\n";
          icsContent += `UID:sncf-${dateClean}-${d.baseCode}@roulement2027\\r\\n`;
          icsContent += `DTSTAMP:${nowUtc}\\r\\n`;
          icsContent += `DTSTART;TZID=Europe/Paris:${dtStart}\\r\\n`;
          icsContent += `DTEND;TZID=Europe/Paris:${dtEnd}\\r\\n`;
          icsContent += `SUMMARY:${d.baseCode} (${d.hoursLabel})${summaryExtra}\\r\\n`;
          icsContent += `DESCRIPTION:Poste: ${d.baseCode}\\nHoraires: ${d.hoursLabel}\\nLieu: Lannemezan Infra\\r\\n`;
          icsContent += "LOCATION:Lannemezan Infra\\r\\nSTATUS:CONFIRMED\\r\\nTRANSP:OPAQUE\\r\\nEND:VEVENT\\r\\n";
        }
      });

      icsContent += "END:VCALENDAR\\r\\n";

      const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = "roulement_2027_personnalise.ics";
      link.click();
    }
  </script>
</body>
</html>
"""

final_html = HTML_TEMPLATE.replace("___DAYS_JSON___", days_json_str).replace("___QRCODE_JS___", qrcode_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("index.html mis à jour avec ergonomie mobile PWA et synchro temps réel !")

with open("roulement_2027_interactif.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("roulement_2027_interactif.html mis à jour !")
