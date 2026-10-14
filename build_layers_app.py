#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de l'interface Roulement SNCF 2027 inspirée de Layers.to, Amie Calendar et macOS Sonoma Widgets.
- Système multi-thèmes fluide avec sélecteur 1-clic :
  1. 'sonoma' : Verre dépoli atmosphérique (Frosted Glassmorphism, fond brume de montagne, tuiles givrées, typographie Apple)
  2. 'amie'   : Studio minimaliste lumineux (Canvas clair, pastels doux, capsules bicolores, dock flottant)
  3. 'gemini' : Thème sombre moderne (Obsidienne profonde, gradients subtils, reflets néon)
- Ergonomie mobile-first (zones tactiles >= 44-48px, dock flottant, zéro overflow)
- Logique métier 100% préservée (365 jours de 2027, quotas VT/CA, Puter Cloud, PIN sécurisé, exports)
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

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr" data-theme="sonoma">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Roulement SNCF 2027 | Riadh Bizid</title>
  
  <!-- PWA & Mobile Web App Meta Tags -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="SNCF 2027">
  <meta name="theme-color" content="#1e293b">

  <!-- Polices Apple / Modern Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  
  <!-- Puter.js pour synchronisation Cloud instantanée -->
  <script src="https://js.puter.com/v2/"></script>

  <style>
    /* ==========================================================================
       DESIGN SYSTEM MULTI-THÈMES (SONOMA FROSTED / AMIE STUDIO / GEMINI DARK)
       ========================================================================== */
    
    /* 1. THÈME PAR DÉFAUT : SONOMA FROSTED WIDGET (Verre Dépoli Atmosphérique) */
    :root, [data-theme="sonoma"] {
      --theme-name: 'sonoma';
      --bg-page: radial-gradient(circle at 50% 10%, #cbd5e1 0%, #94a3b8 40%, #334155 100%);
      --bg-backdrop: linear-gradient(180deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.75) 100%);
      
      --card-bg: rgba(255, 255, 255, 0.72);
      --card-blur: blur(28px);
      --card-border: 1px solid rgba(255, 255, 255, 0.45);
      --card-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.25), 0 1px 3px rgba(0, 0, 0, 0.05);

      --card-elevated-bg: rgba(255, 255, 255, 0.85);
      --card-elevated-border: 1px solid rgba(255, 255, 255, 0.6);

      --dock-bg: rgba(255, 255, 255, 0.8);
      --dock-border: 1px solid rgba(255, 255, 255, 0.5);
      --dock-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.2);

      --text-main: #0f172a;
      --text-secondary: #334155;
      --text-muted: #64748b;
      --text-inverse: #ffffff;

      --accent-color: #f97316; /* Orange chaleureux Apple widget */
      --accent-glow: 0 0 20px rgba(249, 115, 22, 0.35);

      --badge-tny002-bg: rgba(245, 158, 11, 0.18);
      --badge-tny002-text: #b45309;
      --badge-tny003-bg: rgba(16, 185, 129, 0.18);
      --badge-tny003-text: #047857;
      --badge-tny004-bg: rgba(99, 102, 241, 0.18);
      --badge-tny004-text: #4338ca;
      --badge-rp-bg: rgba(148, 163, 184, 0.2);
      --badge-rp-text: #475569;
    }

    /* 2. THÈME AMIE & LAYERS STUDIO (Light Minimaliste Épuré) */
    [data-theme="amie"] {
      --theme-name: 'amie';
      --bg-page: #f8fafc;
      --bg-backdrop: none;
      
      --card-bg: #ffffff;
      --card-blur: none;
      --card-border: 1px solid #e2e8f0;
      --card-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);

      --card-elevated-bg: #f8fafc;
      --card-elevated-border: 1px solid #e2e8f0;

      --dock-bg: rgba(255, 255, 255, 0.95);
      --dock-border: 1px solid #e2e8f0;
      --dock-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);

      --text-main: #0f172a;
      --text-secondary: #475569;
      --text-muted: #94a3b8;
      --text-inverse: #ffffff;

      --accent-color: #2563eb;
      --accent-glow: 0 0 20px rgba(37, 99, 235, 0.25);

      --badge-tny002-bg: #fef3c7;
      --badge-tny002-text: #92400e;
      --badge-tny003-bg: #d1fae5;
      --badge-tny003-text: #065f46;
      --badge-tny004-bg: #ede9fe;
      --badge-tny004-text: #5b21b6;
      --badge-rp-bg: #f1f5f9;
      --badge-rp-text: #64748b;
    }

    /* 3. THÈME GEMINI DARK (Obsidienne Profonde & Dégradés) */
    [data-theme="gemini"] {
      --theme-name: 'gemini';
      --bg-page: #0d0f14;
      --bg-backdrop: radial-gradient(circle at top right, rgba(56, 189, 248, 0.08), transparent 70%);
      
      --card-bg: rgba(20, 23, 33, 0.8);
      --card-blur: blur(24px);
      --card-border: 1px solid rgba(255, 255, 255, 0.09);
      --card-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);

      --card-elevated-bg: rgba(27, 32, 46, 0.9);
      --card-elevated-border: 1px solid rgba(255, 255, 255, 0.14);

      --dock-bg: rgba(18, 22, 32, 0.88);
      --dock-border: 1px solid rgba(255, 255, 255, 0.12);
      --dock-shadow: 0 15px 40px rgba(0, 0, 0, 0.7);

      --text-main: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --text-inverse: #ffffff;

      --accent-color: #818cf8;
      --accent-glow: 0 0 25px rgba(129, 140, 248, 0.4);

      --badge-tny002-bg: rgba(245, 158, 11, 0.15);
      --badge-tny002-text: #fbbf24;
      --badge-tny003-bg: rgba(16, 185, 129, 0.15);
      --badge-tny003-text: #34d399;
      --badge-tny004-bg: rgba(99, 102, 241, 0.15);
      --badge-tny004-text: #a5b4fc;
      --badge-rp-bg: rgba(148, 163, 184, 0.1);
      --badge-rp-text: #94a3b8;
    }

    /* Rayons & Styles communs */
    :root {
      --radius-sm: 10px;
      --radius-md: 16px;
      --radius-lg: 24px;
      --radius-3xl: 32px;
      --radius-full: 9999px;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
      -webkit-tap-highlight-color: transparent;
    }

    html {
      overflow-x: hidden;
      width: 100%;
    }

    body {
      min-height: 100vh;
      width: 100%;
      background: var(--bg-page);
      color: var(--text-main);
      overflow-x: hidden;
      max-width: 100vw;
      transition: background 0.4s ease, color 0.4s ease;
      padding-bottom: 110px; /* Espace pour le dock flottant */
    }
    @media (max-width: 640px) {
      body {
        padding-bottom: 95px;
      }
    }

    /* Motif décoratif brumeux pour thème Sonoma */
    .nature-haze-layer {
      position: fixed;
      inset: 0;
      background: var(--bg-backdrop);
      pointer-events: none;
      z-index: 0;
      transition: opacity 0.4s ease;
    }
    [data-theme="sonoma"] .nature-haze-layer::before {
      content: '';
      position: absolute;
      bottom: 0; left: 0; right: 0;
      height: 45vh;
      background: linear-gradient(0deg, rgba(15, 23, 42, 0.65) 0%, rgba(30, 41, 59, 0.2) 60%, transparent 100%);
      pointer-events: none;
    }

    /* ==========================================================================
       ÉCRAN DE VERROUILLAGE SÉCURISÉ (GLASS FROSTED)
       ========================================================================== */
    .auth-overlay {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      padding: 20px;
      transition: opacity 0.3s ease, visibility 0.3s ease;
    }
    .auth-overlay.hidden {
      opacity: 0 !important;
      visibility: hidden !important;
      pointer-events: none !important;
      display: none !important;
    }
    .auth-card {
      background: var(--card-bg);
      backdrop-filter: var(--card-blur);
      -webkit-backdrop-filter: var(--card-blur);
      border: var(--card-border);
      border-radius: var(--radius-3xl);
      box-shadow: var(--card-shadow);
      width: 100%;
      max-width: 400px;
      padding: 36px 28px;
      text-align: center;
      position: relative;
      animation: modalScale 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes modalScale {
      from { transform: scale(0.92); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    .auth-avatar {
      width: 68px;
      height: 68px;
      border-radius: 50%;
      background: linear-gradient(135deg, #f97316 0%, #ec4899 100%);
      color: white;
      font-size: 1.8rem;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16px;
      box-shadow: 0 8px 20px rgba(249, 115, 22, 0.3);
    }
    .auth-title {
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .auth-subtitle {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 24px;
    }
    .auth-btn-google {
      width: 100%;
      min-height: 52px;
      background: #ffffff;
      color: #1f2937;
      border: 1px solid rgba(0, 0, 0, 0.12);
      border-radius: var(--radius-md);
      font-size: 0.96rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      margin-bottom: 12px;
    }
    .auth-btn-google:hover {
      background: #f9fafb;
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    .auth-btn-google:active {
      transform: scale(0.98);
    }
    [data-theme="dark"] .auth-btn-google,
    [data-theme="gemini"] .auth-btn-google {
      background: rgba(255, 255, 255, 0.95);
      color: #0f172a;
    }
    .auth-btn-bio {
      width: 100%;
      min-height: 52px;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
      border: 1px solid rgba(168, 85, 247, 0.35);
      color: var(--text-main);
      border-radius: var(--radius-md);
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      box-shadow: 0 4px 16px rgba(168, 85, 247, 0.12);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      margin-bottom: 12px;
    }
    .auth-btn-bio:hover {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.25));
      transform: translateY(-2px);
    }
    .auth-btn-bio:active {
      transform: scale(0.98);
    }


    /* ==========================================================================
       TOP BAR & SÉLECTEUR DE THÈMES (SONOMA / AMIE / GEMINI)
       ========================================================================== */
    .top-bar {
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      width: 100%;
      max-width: 1040px;
      margin: 0 auto;
    }
    @media (max-width: 640px) {
      .top-bar {
        padding: 8px 8px;
        gap: 6px;
      }
    }
    .persona-chip {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--card-bg);
      backdrop-filter: var(--card-blur);
      -webkit-backdrop-filter: var(--card-blur);
      border: var(--card-border);
      padding: 6px 12px 6px 8px;
      border-radius: var(--radius-full);
      box-shadow: var(--card-shadow);
      min-width: 0;
      flex-shrink: 1;
    }
    @media (max-width: 640px) {
      .persona-chip {
        padding: 4px 8px 4px 5px;
        gap: 6px;
      }
    }
    .persona-avatar {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: linear-gradient(135deg, #f97316 0%, #ec4899 100%);
      color: white;
      font-weight: 800;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    @media (max-width: 640px) {
      .persona-avatar {
        width: 30px;
        height: 30px;
        font-size: 0.78rem;
      }
    }
    .persona-text {
      min-width: 0;
      overflow: hidden;
    }
    .persona-text h2 {
      font-size: 0.88rem;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    @media (max-width: 640px) {
      .persona-text h2 {
        font-size: 0.78rem;
      }
    }
    .persona-text p {
      font-size: 0.72rem;
      color: var(--text-muted);
      line-height: 1.1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    @media (max-width: 640px) {
      .persona-text p {
        font-size: 0.65rem;
      }
    }
    @media (max-width: 380px) {
      .persona-text p {
        display: none;
      }
    }

    /* Theme Switcher Pill */
    .theme-switcher-pill {
      display: flex;
      align-items: center;
      gap: 3px;
      background: var(--card-bg);
      backdrop-filter: var(--card-blur);
      -webkit-backdrop-filter: var(--card-blur);
      border: var(--card-border);
      padding: 3px;
      border-radius: var(--radius-full);
      box-shadow: var(--card-shadow);
      flex-shrink: 0;
    }
    .theme-opt-btn {
      min-height: 32px;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .theme-opt-btn.active {
      background: var(--accent-color);
      color: white;
      box-shadow: var(--accent-glow);
    }
    @media (max-width: 640px) {
      .theme-opt-btn {
        padding: 4px 8px;
        min-height: 30px;
        font-size: 0.8rem;
        gap: 0;
      }
      .theme-opt-btn .theme-lbl {
        display: none;
      }
    }

    /* ==========================================================================
       CONTAINER PRINCIPAL & WIDGET CENTRAL
       ========================================================================== */
    .main-app-container {
      max-width: 1040px;
      margin: 10px auto 20px;
      padding: 0 16px;
      position: relative;
      z-index: 10;
      width: 100%;
    }
    @media (max-width: 640px) {
      .main-app-container {
        padding: 0 6px;
        margin: 4px auto 14px;
      }
    }

    /* Widget Glass Card Central */
    .glass-widget-card {
      background: var(--card-bg);
      backdrop-filter: var(--card-blur);
      -webkit-backdrop-filter: var(--card-blur);
      border: var(--card-border);
      border-radius: var(--radius-3xl);
      box-shadow: var(--card-shadow);
      padding: 24px;
      position: relative;
      transition: all 0.3s ease;
      width: 100%;
    }
    @media (max-width: 640px) {
      .glass-widget-card {
        padding: 10px 6px;
        border-radius: 18px;
      }
    }

    /* Capsule Quotas VT & CA (Amie & Layers Style) */
    .quotas-capsules-row {
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
      margin-bottom: 20px;
      width: 100%;
    }
    @media (min-width: 640px) {
      .quotas-capsules-row {
        grid-template-columns: 1fr 1fr;
      }
    }
    @media (max-width: 640px) {
      .quotas-capsules-row {
        gap: 8px;
        margin-bottom: 12px;
      }
    }
    .quota-capsule {
      background: var(--card-elevated-bg);
      border: var(--card-elevated-border);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
      transition: transform 0.2s ease;
    }
    @media (max-width: 640px) {
      .quota-capsule {
        padding: 10px 14px;
        gap: 10px;
        border-radius: 14px;
      }
    }
    .quota-capsule:hover {
      transform: translateY(-2px);
    }
    .capsule-vt {
      border-left: 4px solid #0284c7;
    }
    .capsule-ca {
      border-left: 4px solid #ec4899;
    }
    .capsule-title {
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    @media (max-width: 640px) {
      .capsule-title {
        font-size: 0.85rem;
      }
    }
    .capsule-details {
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 4px;
    }
    @media (max-width: 640px) {
      .capsule-details {
        font-size: 0.72rem;
        margin-top: 2px;
      }
    }
    .capsule-big-number {
      font-size: 1.85rem;
      font-weight: 800;
      line-height: 1;
      text-align: right;
    }
    @media (max-width: 640px) {
      .capsule-big-number {
        font-size: 1.45rem;
      }
    }
    .capsule-vt .capsule-big-number { color: #0284c7; }
    .capsule-ca .capsule-big-number { color: #ec4899; }
    .capsule-subtext {
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.04em;
      margin-top: 2px;
    }
    @media (max-width: 640px) {
      .capsule-subtext {
        font-size: 0.65rem;
      }
    }

    /* Mois & Contrôles */
    .widget-nav-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
      width: 100%;
      overflow: hidden;
    }
    .month-dropdown-btn {
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--text-main);
      background: transparent;
      border: none;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
    .month-pills-scroll {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
      padding: 4px 2px;
      width: 100%;
    }
    .month-pills-scroll::-webkit-scrollbar { display: none; }
    .month-pill-tab {
      min-height: 38px;
      padding: 6px 14px;
      border-radius: var(--radius-full);
      background: var(--card-elevated-bg);
      border: var(--card-elevated-border);
      color: var(--text-secondary);
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
      transition: all 0.2s ease;
    }
    @media (max-width: 640px) {
      .month-pill-tab {
        min-height: 32px;
        padding: 5px 11px;
        font-size: 0.74rem;
      }
    }
    .month-pill-tab.active {
      background: var(--accent-color);
      color: white;
      box-shadow: var(--accent-glow);
      border-color: transparent;
    }

    /* ==========================================================================
       GRILLE CALENDRIER STYLE SONOMA & AMIE (100% RESPONSIVE SANS DÉBORDEMENT)
       ========================================================================== */
    .calendar-weekdays-row {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 4px;
      margin-bottom: 6px;
      text-align: center;
      width: 100%;
    }
    .cal-weekday-lbl {
      font-size: 0.74rem;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 4px 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .cal-grid-cells {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 4px;
      width: 100%;
    }
    @media (max-width: 640px) {
      .calendar-weekdays-row {
        gap: 2px;
        margin-bottom: 4px;
      }
      .cal-weekday-lbl {
        font-size: 0.65rem;
        padding: 2px 0;
        letter-spacing: 0;
      }
      .cal-grid-cells {
        gap: 2px;
      }
    }
    .cal-cell {
      min-width: 0;
      min-height: 72px;
      background: var(--card-elevated-bg);
      border: var(--card-elevated-border);
      border-radius: var(--radius-md);
      padding: 6px 4px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      position: relative;
      transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
      user-select: none;
      overflow: hidden;
    }
    @media (max-width: 640px) {
      .cal-cell {
        min-height: 52px;
        padding: 4px 2px;
        border-radius: 8px;
      }
    }
    @media (max-width: 375px) {
      .cal-cell {
        min-height: 48px;
        padding: 3px 1.5px;
        border-radius: 6px;
      }
    }
    .cal-cell:hover {
      transform: translateY(-2px);
      border-color: var(--accent-color);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
      z-index: 5;
    }
    .cal-cell:active {
      transform: scale(0.96);
    }
    .cal-cell.empty {
      background: transparent;
      border: none;
      pointer-events: none;
    }

    .cell-top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      min-width: 0;
      line-height: 1;
    }
    .cell-num {
      font-size: 0.94rem;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1;
    }
    @media (max-width: 640px) {
      .cell-num {
        font-size: 0.76rem;
      }
    }
    .cal-cell.active-day-circle .cell-num {
      background: var(--accent-color);
      color: white;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--accent-glow);
    }
    @media (max-width: 640px) {
      .cal-cell.active-day-circle .cell-num {
        width: 18px;
        height: 18px;
        font-size: 0.7rem;
      }
    }

    /* Badges de poste style Amie Pastel */
    .cell-shift-pill {
      width: 100%;
      min-width: 0;
      max-width: 100%;
      font-size: 0.72rem;
      font-weight: 800;
      border-radius: 6px;
      padding: 3px 4px;
      text-align: center;
      letter-spacing: 0.02em;
      margin-top: 3px;
      line-height: 1.1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    @media (max-width: 640px) {
      .cell-shift-pill {
        font-size: 0.62rem;
        padding: 2px 1px;
        border-radius: 4px;
        margin-top: 2px;
        letter-spacing: 0;
      }
    }
    @media (max-width: 375px) {
      .cell-shift-pill {
        font-size: 0.58rem;
        padding: 1.5px 0.5px;
      }
    }
    .shift-tny002 { background: var(--badge-tny002-bg); color: var(--badge-tny002-text); }
    .shift-tny003 { background: var(--badge-tny003-bg); color: var(--badge-tny003-text); }
    .shift-tny004 { background: var(--badge-tny004-bg); color: var(--badge-tny004-text); }
    .shift-rp { background: var(--badge-rp-bg); color: var(--badge-rp-text); }

    /* Absences posées */
    .cal-cell.status-pending {
      border: 2px dashed #f59e0b !important;
      background: rgba(245, 158, 11, 0.12) !important;
    }
    .cal-cell.status-accepted {
      border: 2px solid #10b981 !important;
      background: rgba(16, 185, 129, 0.14) !important;
    }
    .cal-cell.status-rejected {
      border: 1px solid #f43f5e !important;
      background: rgba(244, 63, 94, 0.12) !important;
    }
    .cell-absence-tag {
      width: 100%;
      min-width: 0;
      max-width: 100%;
      font-size: 0.68rem;
      font-weight: 800;
      border-radius: 4px;
      padding: 2px 3px;
      text-align: center;
      margin-top: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      line-height: 1.1;
    }
    @media (max-width: 640px) {
      .cell-absence-tag {
        font-size: 0.58rem;
        padding: 1px 1px;
        margin-top: 1px;
      }
      .cell-absence-tag .abs-text-full { display: none; }
      .cell-absence-tag .abs-text-short { display: inline; }
    }
    @media (min-width: 641px) {
      .cell-absence-tag .abs-text-full { display: inline; }
      .cell-absence-tag .abs-text-short { display: none; }
    }

    /* ==========================================================================
       TUILES GIVRÉES AU BAS DU WIDGET (SONOMA WIDGET TILES)
       ========================================================================== */
    .widget-bottom-tiles {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-top: 18px;
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      width: 100%;
    }
    @media (max-width: 640px) {
      .widget-bottom-tiles {
        gap: 6px;
        margin-top: 12px;
        padding-top: 12px;
      }
    }
    .frosted-tile {
      background: var(--card-elevated-bg);
      border: var(--card-elevated-border);
      border-radius: var(--radius-md);
      padding: 12px 10px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 2px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
      min-width: 0;
      overflow: hidden;
    }
    @media (max-width: 640px) {
      .frosted-tile {
        padding: 8px 4px;
        border-radius: 12px;
      }
    }
    .tile-label {
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      width: 100%;
    }
    @media (max-width: 640px) {
      .tile-label {
        font-size: 0.62rem;
        letter-spacing: 0;
      }
    }
    .tile-val {
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-main);
      white-space: nowrap;
    }
    @media (max-width: 640px) {
      .tile-val {
        font-size: 0.95rem;
      }
    }

    /* ==========================================================================
       DOCK FLOTTANT (AMIE & MACOS STYLE)
       ========================================================================== */
    .floating-amie-dock {
      position: fixed;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 90;
      background: var(--dock-bg);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: var(--dock-border);
      border-radius: var(--radius-full);
      padding: 6px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--dock-shadow);
      max-width: calc(100vw - 16px);
    }
    @media (max-width: 480px) {
      .floating-amie-dock {
        bottom: 12px;
        padding: 4px 6px;
        gap: 4px;
      }
    }
    @media (max-width: 360px) {
      .floating-amie-dock {
        padding: 3px 4px;
        gap: 2px;
      }
    }
    .dock-squircle-btn {
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 1.25rem;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 2px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      flex-shrink: 0;
    }
    .dock-squircle-btn span.lbl {
      font-size: 0.62rem;
      font-weight: 700;
      line-height: 1;
      white-space: nowrap;
    }
    .dock-squircle-btn:hover {
      background: rgba(0, 0, 0, 0.05);
      color: var(--text-main);
      transform: translateY(-3px) scale(1.08);
    }
    .dock-squircle-btn.active {
      background: var(--accent-color);
      color: white;
      box-shadow: var(--accent-glow);
      transform: translateY(-2px);
    }
    @media (max-width: 480px) {
      .floating-amie-dock {
        bottom: 10px;
        padding: 3px 6px;
        gap: 3px;
      }
      .dock-squircle-btn {
        width: 42px;
        height: 42px;
        font-size: 1.1rem;
        border-radius: 12px;
        gap: 1px;
      }
      .dock-squircle-btn span.lbl {
        font-size: 0.52rem;
        letter-spacing: -0.02em;
      }
    }
    @media (max-width: 360px) {
      .floating-amie-dock {
        padding: 2px 4px;
        gap: 2px;
      }
      .dock-squircle-btn {
        width: 38px;
        height: 40px;
        font-size: 1.02rem;
      }
      .dock-squircle-btn span.lbl {
        font-size: 0.46rem;
      }
    }

    /* ==========================================================================
       MODAL ACTION DU JOUR
       ========================================================================== */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      z-index: 200;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      opacity: 0;
      visibility: hidden;
      transition: all 0.25s ease;
    }
    @media (min-width: 640px) {
      .modal-backdrop {
        align-items: center;
        padding: 20px;
      }
    }
    .modal-backdrop.active {
      opacity: 1;
      visibility: visible;
    }
    .modal-surface {
      background: var(--card-bg);
      backdrop-filter: var(--card-blur);
      -webkit-backdrop-filter: var(--card-blur);
      border: var(--card-border);
      border-radius: var(--radius-3xl) var(--radius-3xl) 0 0;
      width: 100%;
      max-width: 480px;
      max-height: 90vh;
      overflow-y: auto;
      padding: 24px 20px calc(24px + env(safe-area-inset-bottom));
      box-shadow: var(--card-shadow);
      transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @media (min-width: 640px) {
      .modal-surface {
        border-radius: var(--radius-3xl);
        transform: translateY(20px) scale(0.95);
      }
    }
    .modal-backdrop.active .modal-surface {
      transform: translateY(0) scale(1);
    }

    .btn {
      min-height: 48px;
      padding: 10px 18px;
      border-radius: var(--radius-md);
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: none;
      transition: all 0.15s ease;
    }
    .btn:active { transform: scale(0.97); }
    .btn-primary { background: var(--accent-color); color: white; box-shadow: var(--accent-glow); }
    .btn-glass { background: var(--card-elevated-bg); border: var(--card-elevated-border); color: var(--text-main); }
    .btn-danger { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

    /* Toast */
    .toast-pill {
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%) translateY(-30px);
      background: var(--dock-bg);
      backdrop-filter: blur(20px);
      border: var(--dock-border);
      color: var(--text-main);
      padding: 10px 22px;
      border-radius: var(--radius-full);
      box-shadow: var(--dock-shadow);
      font-size: 0.9rem;
      font-weight: 700;
      z-index: 2000;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .toast-pill.show {
      opacity: 1;
      visibility: visible;
      transform: translateX(-50%) translateY(0);
    }
  </style>
</head>
<body>

  <!-- LAYER AMBIANCE BRUME NATURE -->
  <div class="nature-haze-layer"></div>

  <!-- TOAST NOTIFICATION -->
  <div class="toast-pill" id="toastPill">
    <span id="toastIcon">✨</span> <span id="toastMsg">Action effectuée</span>
  </div>

  <!-- ==========================================================================
       ÉCRAN DE VERROUILLAGE SÉCURISÉ (PIN)
       ========================================================================== -->
  <div class="auth-overlay" id="authOverlay">
    <div class="auth-card" id="authCard">
      <div class="auth-avatar">🚆</div>
      <h2 class="auth-title">Roulement SNCF 2027</h2>
      <p class="auth-subtitle">Espace Privé • Riadh</p>

      <!-- Section Empreinte / Face Unlock (Pixel 10 / Android) si activé -->
      <div id="authBioSection" style="display:none; margin-bottom:14px;">
        <button type="button" class="auth-btn-bio" id="btnAuthBio" onclick="unlockWithBiometrics()">
          <span style="font-size:1.35rem;">👆</span>
          <span>Déverrouiller avec l'empreinte (Pixel 10)</span>
        </button>
      </div>

      <!-- Bouton Connexion Google (via Puter) -->
      <button type="button" class="auth-btn-google" id="btnAuthGoogle" onclick="loginWithGooglePuter()">
        <svg width="20" height="20" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span>Se connecter avec Google</span>
      </button>

      <div id="authStatusMsg" style="font-size:0.8rem; color:var(--text-muted); margin-top:14px; line-height:1.4;">
        Connectez-vous avec votre compte Google pour synchroniser et déverrouiller votre agenda automatiquement.
      </div>
      <div id="authErrorMsg" style="color:#ef4444; font-size:0.82rem; font-weight:700; min-height:18px; margin-top:8px;"></div>
    </div>
  </div>

  <!-- ==========================================================================
       TOP BAR (AVATAR PERSONA + SÉLECTEUR DE THÈMES)
       ========================================================================== -->
  <header class="top-bar">
    <div class="persona-chip">
      <div class="persona-avatar">R</div>
      <div class="persona-text">
        <h2>Riadh</h2>
      </div>
    </div>

    <!-- Sélecteur de Thème 1-Clic -->
    <div class="theme-switcher-pill">
      <button class="theme-opt-btn active" id="btnThemeSonoma" onclick="setAppTheme('sonoma')" title="Thème Sonoma">
        <span class="theme-icon">🌲</span><span class="theme-lbl"> Sonoma</span>
      </button>
      <button class="theme-opt-btn" id="btnThemeAmie" onclick="setAppTheme('amie')" title="Thème Amie">
        <span class="theme-icon">☀️</span><span class="theme-lbl"> Amie</span>
      </button>
      <button class="theme-opt-btn" id="btnThemeGemini" onclick="setAppTheme('gemini')" title="Thème Nuit">
        <span class="theme-icon">🌌</span><span class="theme-lbl"> Nuit</span>
      </button>
    </div>
  </header>

  <!-- ==========================================================================
       CONTENU PRINCIPAL : LE WIDGET CARD
       ========================================================================== -->
  <main class="main-app-container">
    <div class="glass-widget-card">

      <!-- CAPSULES DE QUOTAS (STYLE AMIE / LAYERS) -->
      <section class="quotas-capsules-row">
        <!-- Capsule VT -->
        <div class="quota-capsule capsule-vt">
          <div>
            <div class="capsule-title">⏱️ Vacations VT</div>
            <div class="capsule-details">
              Posés : <strong id="capVTPending">0</strong> | Validés : <strong id="capVTAccepted">0</strong>
            </div>
          </div>
          <div>
            <div class="capsule-big-number" id="capVTRemaining">44</div>
            <div class="capsule-subtext">Restants / <span id="capVTTotal">44</span>j</div>
          </div>
        </div>

        <!-- Capsule Congés CA -->
        <div class="quota-capsule capsule-ca">
          <div>
            <div class="capsule-title">🏖️ Congés Annuels (CA)</div>
            <div class="capsule-details">
              Posés : <strong id="capCAPending">0</strong> | Validés : <strong id="capCAAccepted">0</strong>
            </div>
          </div>
          <div>
            <div class="capsule-big-number" id="capCARemaining">23</div>
            <div class="capsule-subtext">Restants / <span id="capCATotal">23</span>j</div>
          </div>
        </div>
      </section>

      <!-- NAVIGATION DU MOIS -->
      <div class="widget-nav-header">
        <div class="month-pills-scroll" id="monthPillsContainer"></div>
      </div>

      <!-- VUE 1 : GRILLE DU CALENDRIER -->
      <div id="viewPanelGrid">
        <div class="calendar-weekdays-row">
          <div class="cal-weekday-lbl">Lun</div>
          <div class="cal-weekday-lbl">Mar</div>
          <div class="cal-weekday-lbl">Mer</div>
          <div class="cal-weekday-lbl">Jeu</div>
          <div class="cal-weekday-lbl">Ven</div>
          <div class="cal-weekday-lbl" style="color:#0284c7;">Sam</div>
          <div class="cal-weekday-lbl" style="color:#ec4899;">Dim</div>
        </div>
        <div class="cal-grid-cells" id="calendarGridDays"></div>
      </div>

      <!-- VUE 2 : PLANNING FEED -->
      <div id="viewPanelPlanning" style="display: none;">
        <div id="planningFeedList" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <!-- VUE 3 : DEMANDES -->
      <div id="viewPanelRequests" style="display: none;">
        <div id="requestsCardsList" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <!-- VUE 4 : SYNC & PARTAGE -->
      <div id="viewPanelSync" style="display: none; padding: 10px 0;">
        <div style="text-align: center; margin-bottom: 20px;">
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px;">☁️ Synchronisation & Partage</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); max-width: 480px; margin: 0 auto 16px;">
            Synchronisez vos modifications en temps réel sur tous vos appareils ou exportez vers Google Calendar.
          </p>
          <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
            <button class="btn btn-primary" onclick="connectPuterCloud()">🚀 Connecter Cloud Puter (1-clic)</button>
            <button class="btn btn-glass" onclick="exportUpdatedICS()">📥 Exporter .ics (Google/Apple)</button>
            <button class="btn btn-glass" onclick="openSettingsModal()">⚙️ Quotas & Mot de passe</button>
          </div>
        </div>
        <div style="display: flex; justify-content: center; padding: 16px; background: white; border-radius: var(--radius-lg); width: fit-content; margin: 0 auto;">
          <div id="qrcodeArea"></div>
        </div>
      </div>

      <!-- TUILES GIVRÉES AU BAS DU WIDGET -->
      <div class="widget-bottom-tiles">
        <div class="frosted-tile">
          <div class="tile-label">Vacations VT</div>
          <div class="tile-val" id="tileVTVal">44 j</div>
        </div>
        <div class="frosted-tile">
          <div class="tile-label">Congés CA</div>
          <div class="tile-val" id="tileCAVal">23 j</div>
        </div>
        <div class="frosted-tile">
          <div class="tile-label">Postes Réels</div>
          <div class="tile-val" id="tileWorkVal">232 j</div>
        </div>
      </div>

    </div>
  </main>

  <!-- ==========================================================================
       DOCK FLOTTANT (AMIE & MACOS SQUIRCLE DOCK)
       ========================================================================== -->
  <nav class="floating-amie-dock">
    <button class="dock-squircle-btn active" id="dockBtnGrid" onclick="switchDockView('grid')" title="Grille">
      📅
      <span class="lbl">Grille</span>
    </button>
    <button class="dock-squircle-btn" id="dockBtnPlanning" onclick="switchDockView('planning')" title="Planning">
      📋
      <span class="lbl">Planning</span>
    </button>
    <button class="dock-squircle-btn" id="dockBtnRequests" onclick="switchDockView('requests')" title="Demandes">
      📊
      <span class="lbl">Demandes</span>
    </button>
    <button class="dock-squircle-btn" id="dockBtnSync" onclick="switchDockView('sync')" title="Sync Cloud">
      ☁️
      <span class="lbl">Sync</span>
    </button>
    <button class="dock-squircle-btn" onclick="lockApp()" title="Verrouiller">
      🔒
      <span class="lbl">Sécurité</span>
    </button>
  </nav>

  <!-- ==========================================================================
       MODAL : GESTION D'UN JOUR SÉLECTIONNÉ
       ========================================================================== */
  -->
  <div class="modal-backdrop" id="dayModalBackdrop" onclick="handleBackdropClick(event, 'dayModalBackdrop')">
    <div class="modal-surface">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
        <div>
          <h3 id="modalDayTitle" style="font-size:1.15rem; font-weight:800; color:var(--text-main);">Vendredi 15 Janvier 2027</h3>
          <p id="modalDaySubtitle" style="font-size:0.82rem; color:var(--text-muted); margin-top:2px;">Poste : TNY003 (10h00 - 16h20)</p>
        </div>
        <button class="btn btn-glass" style="min-height:36px; padding:6px 12px;" onclick="closeDayModal()">✕</button>
      </div>

      <div style="font-size:0.8rem; font-weight:800; text-transform:uppercase; letter-spacing:0.04em; color:var(--text-muted); margin-bottom:8px;">
        Poser une absence sur ce poste :
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:18px;">
        <button class="btn btn-glass" id="btnModalVT" onclick="applyAbsenceType('VT')" style="flex-direction:column; min-height:76px;">
          <span style="font-size:1.4rem;">⏱️</span>
          <span>Vacation VT</span>
        </button>
        <button class="btn btn-glass" id="btnModalCA" onclick="applyAbsenceType('CA')" style="flex-direction:column; min-height:76px;">
          <span style="font-size:1.4rem;">🏖️</span>
          <span>Congé CA</span>
        </button>
      </div>

      <div id="modalStatusSection" style="display:none; margin-bottom:18px;">
        <div style="font-size:0.8rem; font-weight:800; text-transform:uppercase; letter-spacing:0.04em; color:var(--text-muted); margin-bottom:8px;">
          Statut de validation :
        </div>
        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:6px;">
          <button class="btn btn-glass" id="btnStPending" onclick="applyAbsenceStatus('pending')">⏳ En attente</button>
          <button class="btn btn-glass" id="btnStAccepted" onclick="applyAbsenceStatus('accepted')">✅ Accepté</button>
          <button class="btn btn-glass" id="btnStRejected" onclick="applyAbsenceStatus('rejected')">❌ Refusé</button>
        </div>
      </div>

      <div id="modalDeleteSection" style="display:none;">
        <button class="btn btn-danger" style="width:100%; min-height:48px;" onclick="cancelAbsence()">
          🗑️ Supprimer l'absence & rétablir le poste
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       MODAL : QUOTAS & RÉGLAGES
       ========================================================================== -->
  <div class="modal-backdrop" id="settingsModalBackdrop" onclick="handleBackdropClick(event, 'settingsModalBackdrop')">
    <div class="modal-surface">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
        <h3 style="font-size:1.15rem; font-weight:800;">⚙️ Sécurité & Paramètres</h3>
        <button class="btn btn-glass" style="min-height:36px; padding:6px 12px;" onclick="closeSettingsModal()">✕</button>
      </div>

      <!-- CARTE COMPTE GOOGLE / PUTER -->
      <div style="background:var(--card-elevated-bg); border:var(--card-elevated-border); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
          <strong style="font-size:0.86rem; color:var(--text-main);">☁️ Compte Google & Sync</strong>
          <span id="settingsPuterBadge" style="font-size:0.72rem; font-weight:800; padding:3px 8px; border-radius:12px; background:rgba(148,163,184,0.15); color:var(--text-muted);">Non connecté</span>
        </div>
        <p id="settingsPuterUser" style="font-size:0.78rem; color:var(--text-muted); margin-bottom:10px;">Liez votre compte Google pour sauvegarder vos congés dans votre coffre-fort privé.</p>
        <div style="display:flex; gap:8px;">
          <button type="button" id="btnSettingsGoogleConnect" class="btn btn-primary" style="flex:1; min-height:40px; font-size:0.82rem; padding:6px 12px;" onclick="loginWithGooglePuter()">
            Se connecter avec Google
          </button>
          <button type="button" id="btnSettingsGoogleDisconnect" class="btn btn-glass" style="display:none; flex:1; min-height:40px; font-size:0.82rem; padding:6px 12px;" onclick="logoutPuter()">
            Déconnecter
          </button>
        </div>
      </div>

      <!-- CARTE BIOMÉTRIE PIXEL 10 (EMPREINTE DIGITALE / FACE UNLOCK) -->
      <div style="background:var(--card-elevated-bg); border:var(--card-elevated-border); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
          <strong style="font-size:0.86rem; color:var(--text-main);">👆 Empreinte Pixel 10 / Face Unlock</strong>
          <span id="settingsBioBadge" style="font-size:0.72rem; font-weight:800; padding:3px 8px; border-radius:12px; background:rgba(148,163,184,0.15); color:var(--text-muted);">Désactivé</span>
        </div>
        <p style="font-size:0.78rem; color:var(--text-muted); margin-bottom:10px;">Déverrouillez instantanément l'agenda avec l'empreinte de votre Pixel 10.</p>
        <button type="button" id="btnSettingsBioToggle" class="btn btn-glass" style="width:100%; min-height:40px; font-size:0.82rem;" onclick="toggleBiometricsRegistration()">
          👆 Activer l'empreinte sur ce Pixel 10
        </button>
      </div>

      <div style="border-top:1px solid rgba(0,0,0,0.1); padding-top:14px; margin-bottom:16px;">
        <label style="font-size:0.84rem; font-weight:700; display:block; margin-bottom:8px;">📊 Droits aux quotas annuels :</label>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
          <div>
            <span style="font-size:0.75rem; color:var(--text-muted);">Vacations VT :</span>
            <input type="number" id="inputSettingsVT" value="44" style="width:100%; min-height:44px; padding:8px; background:var(--card-elevated-bg); border:var(--card-elevated-border); border-radius:var(--radius-sm); color:var(--text-main); font-weight:800;" onchange="updateSettingsQuotas()">
          </div>
          <div>
            <span style="font-size:0.75rem; color:var(--text-muted);">Congés CA :</span>
            <input type="number" id="inputSettingsCA" value="23" style="width:100%; min-height:44px; padding:8px; background:var(--card-elevated-bg); border:var(--card-elevated-border); border-radius:var(--radius-sm); color:var(--text-main); font-weight:800;" onchange="updateSettingsQuotas()">
          </div>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:8px;">
        <button class="btn btn-glass" onclick="exportBackupJSON()" style="width:100%;">💾 Exporter sauvegarde (.json)</button>
        <label class="btn btn-glass" style="width:100%; cursor:pointer;">
          📂 Importer sauvegarde
          <input type="file" accept=".json" onchange="importBackupJSON(event)" style="display:none;">
        </label>
      </div>
    </div>
  </div>

  <!-- QR Code Lib -->
  <script>
    ___QRCODE_JS___
  </script>

  <!-- Script Principal -->
  <script>
    const RAW_DAYS_DATA = ___DAYS_JSON___;
    const _now = new Date();
    const TODAY_STR = _now.getFullYear() + '-' + String(_now.getMonth() + 1).padStart(2, '0') + '-' + String(_now.getDate()).padStart(2, '0');

    const MONTH_NAMES = [
      "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ];

    let quotaVT = parseInt(localStorage.getItem('sncf_roulement_quota_vt') || '44', 10);
    let quotaConge = parseInt(localStorage.getItem('sncf_roulement_quota_conge') || '23', 10);
    let userAbsences = {};
    let selectedMonth = 1;
    let activeDayDate = null;
    let currentDockView = 'grid';
    let isPuterConnected = false;

    // --- MULTI-THÈME (SONOMA / AMIE / GEMINI) ---
    function setAppTheme(themeName, silent = false) {
      document.documentElement.setAttribute('data-theme', themeName);
      localStorage.setItem('sncf_active_theme', themeName);

      const bS = document.getElementById('btnThemeSonoma');
      const bA = document.getElementById('btnThemeAmie');
      const bG = document.getElementById('btnThemeGemini');
      if (bS) bS.classList.toggle('active', themeName === 'sonoma');
      if (bA) bA.classList.toggle('active', themeName === 'amie');
      if (bG) bG.classList.toggle('active', themeName === 'gemini');

      if (!silent) showToast(`Thème : ${themeName.toUpperCase()}`);
    }

    function initTheme() {
      const saved = localStorage.getItem('sncf_active_theme') || 'sonoma';
      setAppTheme(saved, true);
    }

    // --- SÉCURITÉ & AUTHENTIFICATION (GOOGLE + EMPREINTE PIXEL 10) ---
    const AUTH_CONFIG = {
      RP_NAME: 'Roulement SNCF 2027',
      BIOMETRIC_STORAGE_KEY: 'sncf_2027_biometric_cred_id'
    };

    function updateBioUI() {
      const hasBio = !!localStorage.getItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY);
      const authBioSec = document.getElementById('authBioSection');
      if (authBioSec) authBioSec.style.display = hasBio ? 'block' : 'none';

      const badge = document.getElementById('settingsBioBadge');
      const btn = document.getElementById('btnSettingsBioToggle');
      if (badge && btn) {
        if (hasBio) {
          badge.innerText = "Activé ✓";
          badge.style.background = "rgba(16, 185, 129, 0.15)";
          badge.style.color = "#10b981";
          btn.innerText = "🗑️ Désactiver l'empreinte sur ce Pixel 10";
          btn.className = "btn btn-danger";
        } else {
          badge.innerText = "Désactivé";
          badge.style.background = "rgba(148, 163, 184, 0.15)";
          badge.style.color = "var(--text-muted)";
          btn.innerText = "👆 Activer l'empreinte sur ce Pixel 10";
          btn.className = "btn btn-glass";
        }
      }
    }

    async function toggleBiometricsRegistration() {
      const hasBio = !!localStorage.getItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY);
      if (hasBio) {
        if (confirm("Désactiver le déverrouillage par empreinte sur ce Pixel 10 ?")) {
          localStorage.removeItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY);
          updateBioUI();
          showToast("Empreinte désactivée.");
        }
        return;
      }
      await registerBiometrics();
    }

    async function registerBiometrics() {
      if (!window.PublicKeyCredential) {
        alert("La biométrie WebAuthn n'est pas supportée par ce navigateur.");
        return false;
      }
      try {
        if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
          alert("L'activation de l'empreinte requiert une connexion sécurisée HTTPS.");
          return false;
        }

        const isAvailable = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        if (!isAvailable) {
          alert("Aucun capteur biométrique (Empreinte Pixel / Face Unlock) détecté sur cet appareil.");
          return false;
        }

        const challenge = new Uint8Array(32);
        window.crypto.getRandomValues(challenge);
        const userId = new Uint8Array(16);
        window.crypto.getRandomValues(userId);

        const rpHost = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? undefined : window.location.hostname;

        const createOptions = {
          publicKey: {
            challenge: challenge,
            rp: { name: AUTH_CONFIG.RP_NAME, id: rpHost },
            user: {
              id: userId,
              name: 'riadh',
              displayName: 'Riadh (Pixel 10)'
            },
            pubKeyCredParams: [
              { type: "public-key", alg: -7 }   // ES256 (Natif Android Titan M2 / Pixel Imprint & Apple)
            ],
            authenticatorSelection: {
              authenticatorAttachment: "platform", // Force la puce interne du Pixel 10 (empreinte / visage)
              userVerification: "required",        // Exige l'empreinte ou le visage
              residentKey: "preferred"
            },
            timeout: 60000
          }
        };

        const credential = await navigator.credentials.create(createOptions);
        if (credential && credential.rawId) {
          const credIdBase64 = btoa(String.fromCharCode(...new Uint8Array(credential.rawId)));
          localStorage.setItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY, credIdBase64);
          updateBioUI();
          showToast("Empreinte Pixel 10 activée avec succès !", "👆");
          return true;
        }
      } catch(err) {
        console.error("Erreur WebAuthn register:", err);
        if (err.name !== 'NotAllowedError') {
          alert("Impossible d'activer l'empreinte : " + (err.message || err.name));
        }
        return false;
      }
    }

    async function unlockWithBiometrics() {
      const credIdBase64 = localStorage.getItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY);
      if (!credIdBase64 || !window.PublicKeyCredential) return false;
      try {
        const challenge = new Uint8Array(32);
        window.crypto.getRandomValues(challenge);
        const rawId = Uint8Array.from(atob(credIdBase64), c => c.charCodeAt(0));
        const rpHost = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? undefined : window.location.hostname;

        const getOptions = {
          publicKey: {
            challenge: challenge,
            rpId: rpHost,
            allowCredentials: [{
              type: "public-key",
              id: rawId,
              transports: ["internal", "hybrid"]
            }],
            userVerification: "required",
            timeout: 60000
          }
        };

        const assertion = await navigator.credentials.get(getOptions);
        if (assertion) {
          sessionStorage.setItem('sncf_session_unlocked', 'true');
          localStorage.setItem('sncf_remember_unlocked', 'true');
          const overlay = document.getElementById('authOverlay');
          overlay.classList.add('hidden');
          overlay.style.display = 'none';
          showToast("Bienvenue Riadh !", "👆");
          return true;
        }
      } catch(err) {
        console.warn("Échec ou annulation biométrique:", err);
        const errEl = document.getElementById('authErrorMsg');
        if (errEl && err.name !== 'NotAllowedError') {
          errEl.innerText = "Empreinte non reconnue. Utilisez Google.";
        }
        return false;
      }
    }

    async function loginWithGooglePuter() {
      const errEl = document.getElementById('authErrorMsg');
      if (errEl) errEl.innerText = "";
      if (typeof puter === 'undefined') {
        if (errEl) errEl.innerText = "Module Cloud Puter indisponible.";
        return;
      }
      try {
        await puter.auth.signIn();
        if (puter.auth.isSignedIn()) {
          isPuterConnected = true;
          sessionStorage.setItem('sncf_session_unlocked', 'true');
          localStorage.setItem('sncf_remember_unlocked', 'true'); // Auto-connexion permanente sur Pixel 10

          const user = await puter.auth.getUser();
          localStorage.setItem('sncf_google_user', JSON.stringify({
            username: user.username,
            email: user.email || user.username,
            ts: Date.now()
          }));

          const overlay = document.getElementById('authOverlay');
          overlay.classList.add('hidden');
          overlay.style.display = 'none';
          showToast(`Connecté avec Google (${user.username || 'Riadh'}) !`, "☁️");

          updateSettingsAuthUI();
          syncWithPuter(false);

          // Si l'appareil supporte la biométrie (Pixel 10) et que ce n'est pas encore activé, suggérer l'empreinte
          const hasBio = localStorage.getItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY);
          if (!hasBio && window.PublicKeyCredential) {
            setTimeout(() => {
              showToast("💡 Astuce : Vous pouvez activer l'empreinte Pixel 10 dans les Paramètres ⚙️ !", "👆");
            }, 3000);
          }
        }
      } catch(err) {
        console.error("Échec connexion Puter:", err);
        if (errEl) errEl.innerText = "Connexion fermée ou annulée.";
      }
    }

    async function logoutPuter() {
      if (typeof puter !== 'undefined' && puter.auth) {
        try { await puter.auth.signOut(); } catch(e) {}
      }
      isPuterConnected = false;
      localStorage.removeItem('sncf_remember_unlocked');
      localStorage.removeItem('sncf_google_user');
      sessionStorage.removeItem('sncf_session_unlocked');
      closeSettingsModal();
      lockApp();
      updateSettingsAuthUI();
      showToast("Déconnecté de Google");
    }

    function updateSettingsAuthUI() {
      const pBadge = document.getElementById('settingsPuterBadge');
      const pUser = document.getElementById('settingsPuterUser');
      const btnConn = document.getElementById('btnSettingsGoogleConnect');
      const btnDisc = document.getElementById('btnSettingsGoogleDisconnect');

      if (!pBadge) return;

      if (isPuterConnected && typeof puter !== 'undefined' && puter.auth && puter.auth.isSignedIn()) {
        puter.auth.getUser().then(u => {
          pBadge.innerText = "Connecté ✓";
          pBadge.style.background = "rgba(16, 185, 129, 0.15)";
          pBadge.style.color = "#10b981";
          if (pUser) pUser.innerText = `Connecté en tant que ${u.username || 'Riadh'}. Synchronisation active.`;
          if (btnConn) btnConn.style.display = "none";
          if (btnDisc) btnDisc.style.display = "block";
        }).catch(() => {});
      } else {
        pBadge.innerText = "Non connecté";
        pBadge.style.background = "rgba(148, 163, 184, 0.15)";
        pBadge.style.color = "var(--text-muted)";
        if (pUser) pUser.innerText = "Liez votre compte Google pour sauvegarder vos congés dans votre coffre-fort privé.";
        if (btnConn) btnConn.style.display = "block";
        if (btnDisc) btnDisc.style.display = "none";
      }
    }

    async function checkAuthOnLoad() {
      const overlay = document.getElementById('authOverlay');
      
      // AUTO-UNLOCK SILENCIEUX SUR PIXEL 10 & SMARTPHONE :
      // Si une session Google est active (Puter ou localStorage persistant), on entre directement !
      const isRemembered = localStorage.getItem('sncf_remember_unlocked') === 'true';
      const isSession = sessionStorage.getItem('sncf_session_unlocked') === 'true';
      const hasGoogleUser = !!localStorage.getItem('sncf_google_user');
      const isPuterAuth = (typeof puter !== 'undefined' && puter.auth && puter.auth.isSignedIn());

      updateBioUI();
      updateSettingsAuthUI();

      if (isRemembered || isSession || hasGoogleUser || isPuterAuth) {
        // Déverrouillage automatique immédiat sans aucune friction
        sessionStorage.setItem('sncf_session_unlocked', 'true');
        overlay.classList.add('hidden');
        overlay.style.display = 'none';
        return;
      }

      // Première visite ou après déconnexion manuelle
      overlay.classList.remove('hidden');
      overlay.style.display = 'flex';

      // Si l'empreinte Pixel 10 est déjà activée, la solliciter
      const hasBio = localStorage.getItem(AUTH_CONFIG.BIOMETRIC_STORAGE_KEY);
      if (hasBio && window.PublicKeyCredential) {
        setTimeout(() => {
          unlockWithBiometrics();
        }, 350);
      }
    }

    function lockApp() {
      sessionStorage.removeItem('sncf_session_unlocked');
      localStorage.removeItem('sncf_remember_unlocked');
      localStorage.removeItem('sncf_google_user');
      const overlay = document.getElementById('authOverlay');
      overlay.classList.remove('hidden');
      overlay.style.display = 'flex';
      updateBioUI();
      showToast("Agenda verrouillé 🔒");
    }

    // --- DONNÉES & CALCULS ---
    function loadSavedData() {
      try {
        const s = localStorage.getItem('sncf_roulement_absences');
        if (s) userAbsences = JSON.parse(s);
      } catch(e) { userAbsences = {}; }
      document.getElementById('inputSettingsVT').value = quotaVT;
      document.getElementById('inputSettingsCA').value = quotaConge;
      document.getElementById('capVTTotal').innerText = quotaVT;
      document.getElementById('capCATotal').innerText = quotaConge;
    }

    function saveData() {
      localStorage.setItem('sncf_roulement_quota_vt', quotaVT);
      localStorage.setItem('sncf_roulement_quota_conge', quotaConge);
      localStorage.setItem('sncf_roulement_absences', JSON.stringify(userAbsences));
      autoSyncCloud();
    }

    function updateSettingsQuotas() {
      const v = parseInt(document.getElementById('inputSettingsVT').value, 10);
      const c = parseInt(document.getElementById('inputSettingsCA').value, 10);
      if (!isNaN(v)) quotaVT = v;
      if (!isNaN(c)) quotaConge = c;
      document.getElementById('capVTTotal').innerText = quotaVT;
      document.getElementById('capCATotal').innerText = quotaConge;
      saveData();
      updateAllStats();
      renderCurrentView();
    }

    const TOTAL_BASE_WORK_DAYS = RAW_DAYS_DATA.filter(d => d.isWork).length;

    function updateAllStats() {
      let vtPend = 0, vtAcc = 0;
      let caPend = 0, caAcc = 0;

      Object.values(userAbsences).forEach(a => {
        if (a.type === 'VT') {
          if (a.status === 'pending') vtPend++;
          else if (a.status === 'accepted') vtAcc++;
        } else if (a.type === 'CA') {
          if (a.status === 'pending') caPend++;
          else if (a.status === 'accepted') caAcc++;
        }
      });

      const vtRest = Math.max(0, quotaVT - vtAcc - vtPend);
      const caRest = Math.max(0, quotaConge - caAcc - caPend);
      const workReal = Math.max(0, TOTAL_BASE_WORK_DAYS - (vtAcc + caAcc));

      // Capsules
      document.getElementById('capVTPending').innerText = vtPend;
      document.getElementById('capVTAccepted').innerText = vtAcc;
      document.getElementById('capVTRemaining').innerText = vtRest;

      document.getElementById('capCAPending').innerText = caPend;
      document.getElementById('capCAAccepted').innerText = caAcc;
      document.getElementById('capCARemaining').innerText = caRest;

      // Bottom Tiles
      document.getElementById('tileVTVal').innerText = vtRest + ' j';
      document.getElementById('tileCAVal').innerText = caRest + ' j';
      document.getElementById('tileWorkVal').innerText = workReal + ' j';
    }

    // --- NAVIGATION MOIS & GRILLE ---
    function renderMonthPills() {
      const c = document.getElementById('monthPillsContainer');
      c.innerHTML = '';
      MONTH_NAMES.forEach((m, idx) => {
        const num = idx + 1;
        const btn = document.createElement('button');
        btn.className = 'month-pill-tab' + (num === selectedMonth ? ' active' : '');
        btn.innerText = m;
        btn.onclick = () => { selectedMonth = num; renderMonthPills(); renderCurrentView(); };
        c.appendChild(btn);
      });
    }

    function renderGrid() {
      const grid = document.getElementById('calendarGridDays');
      grid.innerHTML = '';
      const days = RAW_DAYS_DATA.filter(d => d.month === selectedMonth);
      if (!days.length) return;

      const firstWeekday = days[0].weekdayIndex;
      for (let i = 0; i < firstWeekday; i++) {
        const e = document.createElement('div');
        e.className = 'cal-cell empty';
        grid.appendChild(e);
      }

      days.forEach(day => {
        const cell = document.createElement('div');
        cell.className = 'cal-cell' + (day.date === TODAY_STR ? ' active-day-circle' : '');
        const abs = userAbsences[day.date];

        if (abs) {
          cell.classList.add('status-' + abs.status);
        }

        cell.onclick = () => openDayModal(day.date);

        let holidayIcon = day.isHoliday ? '<span style="font-size:0.65rem;" title="' + day.holidayName + '">🎉</span>' : '';
        let shiftClass = 'shift-' + (day.baseCode.startsWith('TNY') ? day.baseCode.toLowerCase() : 'rp');

        let absenceHtml = '';
        if (abs) {
          const bg = abs.status === 'accepted' ? '#10b981' : '#f59e0b';
          const fullLabel = abs.type + ' ' + (abs.status === 'accepted' ? 'Validé' : 'Posé');
          const shortLabel = abs.type + ' ' + (abs.status === 'accepted' ? '✓' : '⏳');
          absenceHtml = `<div class="cell-absence-tag" style="background:${bg}; color:white;" title="${fullLabel}"><span class="abs-text-full">${fullLabel}</span><span class="abs-text-short">${shortLabel}</span></div>`;
        }

        cell.innerHTML = `
          <div class="cell-top-bar">
            <span class="cell-num">${day.day}</span>
            ${holidayIcon}
          </div>
          ${absenceHtml}
          <div class="cell-shift-pill ${shiftClass}">${day.baseCode}</div>
        `;
        grid.appendChild(cell);
      });
    }

    function renderPlanningFeed() {
      const c = document.getElementById('planningFeedList');
      c.innerHTML = '';
      const days = RAW_DAYS_DATA.filter(d => d.month === selectedMonth);

      days.forEach(day => {
        const card = document.createElement('div');
        card.style.cssText = "background:var(--card-elevated-bg); border:var(--card-elevated-border); border-radius:var(--radius-md); padding:14px; display:flex; align-items:center; justify-content:space-between; cursor:pointer;";
        card.onclick = () => openDayModal(day.date);

        const abs = userAbsences[day.date];
        let absBadge = '';
        if (abs) {
          absBadge = `<span style="font-size:0.75rem; font-weight:700; color:${abs.status==='accepted'?'#10b981':'#f59e0b'};"> [${abs.type} ${abs.status}]</span>`;
        }

        card.innerHTML = `
          <div>
            <div style="font-weight:800; font-size:1rem; color:var(--text-main);">${day.weekday} ${day.day} ${MONTH_NAMES[day.month-1]}</div>
            <div style="font-size:0.78rem; color:var(--text-muted);">${day.holidayName ? '🎉 ' + day.holidayName : ''} ${day.hoursLabel || 'Repos'}</div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="cell-shift-pill shift-${day.baseCode.toLowerCase()}">${day.baseCode}</span>
            ${absBadge}
          </div>
        `;
        c.appendChild(card);
      });
    }

    function renderRequestsCards() {
      const c = document.getElementById('requestsCardsList');
      c.innerHTML = '';
      const dates = Object.keys(userAbsences).sort();
      if (!dates.length) {
        c.innerHTML = '<div style="text-align:center; padding:30px; color:var(--text-muted);">Aucune demande enregistrée.</div>';
        return;
      }
      dates.forEach(dt => {
        const abs = userAbsences[dt];
        const day = RAW_DAYS_DATA.find(d => d.date === dt) || {};
        const div = document.createElement('div');
        div.style.cssText = "background:var(--card-elevated-bg); border:var(--card-elevated-border); border-radius:var(--radius-md); padding:14px; display:flex; align-items:center; justify-content:space-between;";
        div.innerHTML = `
          <div>
            <strong style="color:var(--text-main); font-size:0.95rem;">${dt} (${day.weekday || ''})</strong>
            <div style="font-size:0.8rem; color:var(--text-muted);">Poste: ${day.baseCode || ''} | Type: <strong style="color:var(--accent-color);">${abs.type}</strong></div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-weight:700; font-size:0.85rem; color:${abs.status==='accepted'?'#10b981':(abs.status==='rejected'?'#f43f5e':'#f59e0b')}">${abs.status}</span>
            <button class="btn btn-glass" style="min-height:36px; padding:4px 10px; font-size:0.78rem;" onclick="openDayModal('${dt}')">Modifier</button>
          </div>
        `;
        c.appendChild(div);
      });
    }

    function switchDockView(vName) {
      currentDockView = vName;
      document.getElementById('viewPanelGrid').style.display = vName === 'grid' ? 'block' : 'none';
      document.getElementById('viewPanelPlanning').style.display = vName === 'planning' ? 'block' : 'none';
      document.getElementById('viewPanelRequests').style.display = vName === 'requests' ? 'block' : 'none';
      document.getElementById('viewPanelSync').style.display = vName === 'sync' ? 'block' : 'none';

      document.querySelectorAll('.dock-squircle-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('dockBtn' + vName.charAt(0).toUpperCase() + vName.slice(1));
      if (activeBtn) activeBtn.classList.add('active');

      renderCurrentView();
    }

    function renderCurrentView() {
      if (currentDockView === 'grid') renderGrid();
      else if (currentDockView === 'planning') renderPlanningFeed();
      else if (currentDockView === 'requests') renderRequestsCards();
      else if (currentDockView === 'sync') generateQRCode();
    }

    // --- MODAL ACTION JOUR ---
    function openDayModal(dateStr) {
      activeDayDate = dateStr;
      const day = RAW_DAYS_DATA.find(d => d.date === dateStr);
      if (!day) return;

      document.getElementById('modalDayTitle').innerText = `${day.weekday} ${day.day} ${MONTH_NAMES[day.month-1]} 2027`;
      document.getElementById('modalDaySubtitle').innerText = `Poste : ${day.baseCode} ${day.hoursLabel ? '(' + day.hoursLabel + ')' : '(Repos)'}`;

      const isRestDay = !day.isWork;
      const btnVT = document.getElementById('btnModalVT');
      const btnCA = document.getElementById('btnModalCA');
      if (btnVT && btnCA) {
        btnVT.disabled = isRestDay;
        btnCA.disabled = isRestDay;
        btnVT.style.opacity = isRestDay ? '0.35' : '1';
        btnCA.style.opacity = isRestDay ? '0.35' : '1';
        btnVT.style.cursor = isRestDay ? 'not-allowed' : 'pointer';
        btnCA.style.cursor = isRestDay ? 'not-allowed' : 'pointer';
        btnVT.title = isRestDay ? 'Impossible de poser un congé sur un jour de Repos' : '';
        btnCA.title = isRestDay ? 'Impossible de poser un congé sur un jour de Repos' : '';
      }

      const abs = userAbsences[dateStr];
      const stSec = document.getElementById('modalStatusSection');
      const delSec = document.getElementById('modalDeleteSection');

      if (abs) {
        stSec.style.display = 'block';
        delSec.style.display = 'block';
      } else {
        stSec.style.display = 'none';
        delSec.style.display = 'none';
      }
      document.getElementById('dayModalBackdrop').classList.add('active');
    }

    function closeDayModal() {
      document.getElementById('dayModalBackdrop').classList.remove('active');
      activeDayDate = null;
    }

    function applyAbsenceType(type) {
      if (!activeDayDate) return;
      const day = RAW_DAYS_DATA.find(d => d.date === activeDayDate);
      if (day && !day.isWork) {
        showToast("Impossible de poser un congé sur un Repos !", "⚠️");
        return;
      }
      if (!userAbsences[activeDayDate]) {
        userAbsences[activeDayDate] = { type: type, status: 'pending' };
      } else {
        userAbsences[activeDayDate].type = type;
      }
      saveData();
      updateAllStats();
      openDayModal(activeDayDate);
      renderCurrentView();
      showToast(`${type} posé en attente !`);
    }

    function applyAbsenceStatus(status) {
      if (!activeDayDate || !userAbsences[activeDayDate]) return;
      userAbsences[activeDayDate].status = status;
      saveData();
      updateAllStats();
      openDayModal(activeDayDate);
      renderCurrentView();
      showToast(`Statut : ${status}`);
    }

    function cancelAbsence() {
      if (!activeDayDate) return;
      delete userAbsences[activeDayDate];
      saveData();
      updateAllStats();
      closeDayModal();
      renderCurrentView();
      showToast("Poste rétabli !");
    }

    function handleBackdropClick(e, id) {
      if (e.target.id === id) {
        if (id === 'dayModalBackdrop') closeDayModal();
        if (id === 'settingsModalBackdrop') closeSettingsModal();
      }
    }

    function openSettingsModal() { document.getElementById('settingsModalBackdrop').classList.add('active'); }
    function closeSettingsModal() { document.getElementById('settingsModalBackdrop').classList.remove('active'); }

    // --- PUTER CLOUD & EXPORTS ---
    async function initPuterState() {
      if (typeof puter !== 'undefined' && window.location.protocol.startsWith('http')) {
        try {
          if (puter.auth && puter.auth.isSignedIn()) {
            isPuterConnected = true;
            updateSettingsAuthUI();
            syncWithPuter(true);
          }
        } catch(e) {}
      }
    }

    async function connectPuterCloud() {
      if (typeof puter === 'undefined') { alert("Puter.js indisponible."); return; }
      try {
        await puter.auth.signIn();
        isPuterConnected = true;
        syncWithPuter(false);
        showToast("Cloud Puter connecté !");
      } catch(e) {}
    }

    async function syncWithPuter(silent = false) {
      if (!isPuterConnected || typeof puter === 'undefined') return;
      try {
        const cloudDataStr = await puter.kv.get('sncf_roulement_2027');
        if (cloudDataStr) {
          const cloudData = JSON.parse(cloudDataStr);
          const localUpdated = parseInt(localStorage.getItem('sncf_roulement_updated_at') || '0', 10);
          if (cloudData.ts && cloudData.ts > localUpdated) {
            quotaVT = cloudData.vt || quotaVT;
            quotaConge = cloudData.ca || quotaConge;
            userAbsences = cloudData.abs || userAbsences;
            localStorage.setItem('sncf_roulement_quota_vt', quotaVT);
            localStorage.setItem('sncf_roulement_quota_conge', quotaConge);
            localStorage.setItem('sncf_roulement_absences', JSON.stringify(userAbsences));
            localStorage.setItem('sncf_roulement_updated_at', cloudData.ts);
            loadSavedData();
            updateAllStats();
            renderCurrentView();
            if (!silent) showToast("Synchronisé depuis le Cloud !");
            return;
          }
        }
        await autoSyncCloud();
        if (!silent) showToast("Sauvegardé sur le Cloud !");
      } catch(e) {}
    }

    function autoSyncCloud() {
      const now = Date.now();
      localStorage.setItem('sncf_roulement_updated_at', now);
      if (isPuterConnected && typeof puter !== 'undefined') {
        const payload = { vt: quotaVT, ca: quotaConge, abs: userAbsences, ts: now };
        puter.kv.set('sncf_roulement_2027', JSON.stringify(payload)).catch(e => console.error(e));
      }
    }

    window.addEventListener('focus', () => { if (isPuterConnected) syncWithPuter(true); });
    setInterval(() => {
      if (isPuterConnected && document.visibilityState === 'visible') {
        syncWithPuter(true);
      }
    }, 15000);

    function loadFromUrlHash() {
      if (window.location.hash && window.location.hash.startsWith('#sync=')) {
        try {
          const raw = decodeURIComponent(window.location.hash.slice(6));
          const parsed = JSON.parse(raw);
          if (parsed.vt !== undefined) quotaVT = parsed.vt;
          if (parsed.ca !== undefined) quotaConge = parsed.ca;
          if (parsed.a) {
            userAbsences = {};
            Object.keys(parsed.a).forEach(dt => {
              const code = parsed.a[dt];
              const type = code[0] === 'C' ? 'CA' : 'VT';
              const status = code[1] === '2' ? 'accepted' : (code[1] === '3' ? 'rejected' : 'pending');
              userAbsences[dt] = { type, status };
            });
          } else if (parsed.abs) {
            userAbsences = parsed.abs;
          }
          saveData();
          loadSavedData();
          updateAllStats();
          renderCurrentView();
          window.location.hash = '';
          showToast("Données importées depuis le QR Code !");
        } catch(e) {}
      }
    }

    function generateQRCode() {
      const el = document.getElementById('qrcodeArea');
      if (!el || typeof QRCode === 'undefined') return;
      el.innerHTML = '';
      const compactAbs = {};
      Object.keys(userAbsences).forEach(dt => {
        const item = userAbsences[dt];
        const t = item.type === 'CA' ? 'C' : 'V';
        const s = item.status === 'accepted' ? '2' : (item.status === 'rejected' ? '3' : '1');
        compactAbs[dt] = t + s;
      });
      const payload = { vt: quotaVT, ca: quotaConge, a: compactAbs };
      const url = window.location.origin + window.location.pathname + '#sync=' + encodeURIComponent(JSON.stringify(payload));
      new QRCode(el, { text: url, width: 200, height: 200, colorDark: "#0f172a", colorLight: "#ffffff" });
    }

    function addOneDayStr(dateStr) {
      const parts = dateStr.split('-').map(Number);
      const d = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2] + 1));
      return d.toISOString().slice(0, 10);
    }

    function exportUpdatedICS() {
      let ics = "BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//SNCF//Roulement 2027 Layers//FR\\r\\nCALSCALE:GREGORIAN\\r\\nMETHOD:PUBLISH\\r\\nX-WR-CALNAME:Roulement SNCF 2027\\r\\nX-WR-TIMEZONE:Europe/Paris\\r\\n";
      const nowUtc = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      RAW_DAYS_DATA.forEach(d => {
        const abs = userAbsences[d.date];
        const dateClean = d.date.replace(/-/g, "");
        const nextDayClean = addOneDayStr(d.date).replace(/-/g, "");
        if (abs && abs.status === 'accepted') {
          const label = abs.type === 'VT' ? 'VT (Temps Partiel)' : 'Congé Annuel';
          ics += `BEGIN:VEVENT\\r\\nUID:sncf-${dateClean}-abs@roulement\\r\\nDTSTAMP:${nowUtc}\\r\\nDTSTART;VALUE=DATE:${dateClean}\\r\\nDTEND;VALUE=DATE:${nextDayClean}\\r\\nSUMMARY:${label}\\r\\nSTATUS:CONFIRMED\\r\\nEND:VEVENT\\r\\n`;
        } else if (d.isWork) {
          const s = d.startTime.split(":");
          const e = d.endTime.split(":");
          const dtStart = `${dateClean}T${s[0]}${s[1]}00`;
          let dtEnd = "";
          if (d.endTime === "00:00") {
            dtEnd = `${nextDayClean}T000000`;
          } else {
            dtEnd = `${dateClean}T${e[0]}${e[1]}00`;
          }
          let extra = abs && abs.status === 'pending' ? ` [${abs.type} EN ATTENTE]` : '';
          ics += `BEGIN:VEVENT\\r\\nUID:sncf-${dateClean}-${d.baseCode}@roulement\\r\\nDTSTAMP:${nowUtc}\\r\\nDTSTART;TZID=Europe/Paris:${dtStart}\\r\\nDTEND;TZID=Europe/Paris:${dtEnd}\\r\\nSUMMARY:${d.baseCode} (${d.hoursLabel})${extra}\\r\\nLOCATION:Lannemezan Infra\\r\\nSTATUS:CONFIRMED\\r\\nEND:VEVENT\\r\\n`;
        }
      });
      ics += "END:VCALENDAR\\r\\n";
      const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'roulement_2027_sncf.ics';
      a.click();
    }

    function exportBackupJSON() {
      const b = { quotaVT, quotaConge, absences: userAbsences };
      const blob = new Blob([JSON.stringify(b, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'sauvegarde_roulement_2027.json';
      a.click();
    }

    function importBackupJSON(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const imported = JSON.parse(event.target.result);
          if (imported.quotaVT !== undefined) quotaVT = imported.quotaVT;
          if (imported.quotaConge !== undefined) quotaConge = imported.quotaConge;
          if (imported.absences !== undefined) userAbsences = imported.absences;
          saveData();
          loadSavedData();
          updateAllStats();
          closeSettingsModal();
          renderCurrentView();
          showToast("Sauvegarde importée !");
        } catch(err) { alert("Fichier invalide."); }
      };
      reader.readAsText(file);
    }

    function showToast(msg, icon = "✨") {
      const el = document.getElementById('toastPill');
      document.getElementById('toastIcon').innerText = icon;
      document.getElementById('toastMsg').innerText = msg;
      el.classList.add('show');
      setTimeout(() => el.classList.remove('show'), 2500);
    }

    // --- INITIALISATION ---
    window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      checkAuthOnLoad();
      loadSavedData();
      loadFromUrlHash();
      renderMonthPills();
      updateAllStats();
      renderGrid();
      initPuterState();
    });
  </script>
</body>
</html>
"""

final_html = HTML_CONTENT.replace("___DAYS_JSON___", days_json_str).replace("___QRCODE_JS___", qrcode_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print(f"index.html généré avec succès ({len(final_html)} octets) !")

with open("roulement_2027_interactif.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print(f"roulement_2027_interactif.html généré avec succès ({len(final_html)} octets) !")
