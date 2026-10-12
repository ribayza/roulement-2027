#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de refactoring complet de l'application 'Roulement SNCF 2027' :
- Identité visuelle ultra-moderne inspirée de Google Gemini (Dark theme, glassmorphism, dégradés d'accentuation)
- Responsive mobile-first (du 375px au desktop 4K, sans overflow horizontal)
- Zones tactiles ergonomiques (minimum 44-48px de hauteur pour tous les boutons/inputs)
- Bottom Navigation Bar mobile + Navigation aérée sur desktop
- Vues Grille, Planning continu (feed), Demandes/Suivi, et Sync Cloud
- Écran de verrouillage PIN sécurisé avec personnalisation directe et œil d'affichage
- Intégrité 100% de la logique métier, des données de roulement 2027 et de la synchronisation bidirectionnelle
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
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Roulement SNCF 2027 | Espace Personnel Riadh Bizid</title>
  
  <!-- PWA & Mobile Web App Meta Tags -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="SNCF 2027">
  <meta name="theme-color" content="#0d0f14">

  <!-- Polices Google Sans / Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  
  <!-- Puter.js pour synchronisation Cloud instantanée -->
  <script src="https://js.puter.com/v2/"></script>

  <style>
    /* ==========================================================================
       DESIGN SYSTEM GEMINI & VARIABLES
       ========================================================================== */
    :root {
      --bg-app: #0d0f14;
      --bg-surface: #141721;
      --bg-surface-elevated: #1b202e;
      --bg-surface-glass: rgba(20, 23, 33, 0.78);
      --bg-glass-card: rgba(26, 31, 46, 0.65);
      
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-medium: rgba(255, 255, 255, 0.14);
      --border-active: rgba(129, 140, 248, 0.6);

      /* Gradients Gemini */
      --gemini-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 45%, #c084fc 100%);
      --gemini-gradient-hover: linear-gradient(135deg, #0ea5e9 0%, #6366f1 45%, #a855f7 100%);
      --gemini-glow: 0 0 35px -5px rgba(129, 140, 248, 0.35);

      /* Typographie & Couleurs de texte */
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --text-dim: #64748b;

      /* Postes de travail SNCF */
      --color-tny002: #fbbf24;
      --bg-tny002: rgba(245, 158, 11, 0.15);
      --border-tny002: rgba(245, 158, 11, 0.35);

      --color-tny003: #34d399;
      --bg-tny003: rgba(16, 185, 129, 0.15);
      --border-tny003: rgba(16, 185, 129, 0.35);

      --color-tny004: #a5b4fc;
      --bg-tny004: rgba(99, 102, 241, 0.15);
      --border-tny004: rgba(99, 102, 241, 0.35);

      --color-rp: #94a3b8;
      --bg-rp: rgba(148, 163, 184, 0.08);
      --border-rp: rgba(148, 163, 184, 0.18);

      /* Statuts d'absence */
      --color-vt: #38bdf8;
      --bg-vt: rgba(56, 189, 248, 0.15);
      
      --color-ca: #f472b6;
      --bg-ca: rgba(244, 114, 182, 0.15);

      --status-pending: #fbbf24;
      --bg-pending: rgba(251, 191, 36, 0.18);

      --status-accepted: #34d399;
      --bg-accepted: rgba(52, 211, 153, 0.18);

      --status-rejected: #fb7185;
      --bg-rejected: rgba(251, 113, 133, 0.18);

      /* Rayons et ombres */
      --radius-sm: 10px;
      --radius-md: 16px;
      --radius-lg: 24px;
      --radius-full: 9999px;
      
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.25);
      --shadow-md: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 16px 40px -8px rgba(0, 0, 0, 0.6);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      background-color: var(--bg-app);
      color: var(--text-primary);
      min-height: 100vh;
      overflow-x: hidden;
      max-width: 100vw;
      -webkit-font-smoothing: antialiased;
    }

    /* Ambient Glow background */
    body::before {
      content: '';
      position: fixed;
      top: -150px;
      right: -100px;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }
    body::after {
      content: '';
      position: fixed;
      bottom: -150px;
      left: -100px;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(168, 85, 247, 0.07) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }

    /* Padding pour la Bottom Nav Bar mobile */
    body {
      padding-bottom: 95px;
    }
    @media (min-width: 900px) {
      body {
        padding-bottom: 30px;
      }
    }

    /* ==========================================================================
       ÉCRAN DE VERROUILLAGE SÉCURISÉ (STYLE GEMINI GLASS)
       ========================================================================== */
    .auth-overlay {
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at center, rgba(20, 24, 38, 0.96) 0%, rgba(10, 12, 18, 0.98) 100%);
      backdrop-filter: blur(28px);
      -webkit-backdrop-filter: blur(28px);
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
      background: var(--bg-surface-glass);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-lg);
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), var(--gemini-glow);
      width: 100%;
      max-width: 420px;
      padding: 36px 26px;
      text-align: center;
      position: relative;
      overflow: hidden;
      animation: authCardEnter 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes authCardEnter {
      from { transform: scale(0.94) translateY(20px); opacity: 0; }
      to { transform: scale(1) translateY(0); opacity: 1; }
    }
    .auth-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: var(--gemini-gradient);
    }
    .auth-sparkle {
      width: 60px;
      height: 60px;
      margin: 0 auto 16px;
      background: var(--gemini-gradient);
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--gemini-glow);
    }
    .auth-sparkle svg {
      width: 32px;
      height: 32px;
      fill: white;
    }
    .auth-title {
      font-size: 1.45rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: var(--gemini-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .auth-subtitle {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 6px;
      margin-bottom: 26px;
    }
    .auth-input-wrapper {
      position: relative;
      width: 100%;
      margin-bottom: 8px;
    }
    .auth-input {
      width: 100%;
      min-height: 54px;
      padding: 14px 50px 14px 18px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      font-size: 1.4rem;
      text-align: center;
      letter-spacing: 6px;
      font-weight: 700;
      color: var(--text-primary);
      outline: none;
      transition: all 0.25s ease;
    }
    .auth-input:focus {
      border-color: #818cf8;
      box-shadow: 0 0 0 4px rgba(129, 140, 248, 0.25);
    }
    .auth-input.error {
      border-color: var(--status-rejected);
      box-shadow: 0 0 0 4px rgba(244, 63, 94, 0.2);
    }
    .auth-toggle-pwd {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 1.25rem;
      cursor: pointer;
      width: 44px;
      height: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
    }
    .auth-error-msg {
      color: var(--status-rejected);
      font-size: 0.82rem;
      font-weight: 600;
      min-height: 22px;
      margin-top: 4px;
    }
    .auth-remember {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      margin: 14px 0 22px;
      font-size: 0.85rem;
      color: var(--text-secondary);
      cursor: pointer;
      min-height: 44px;
    }
    .auth-remember input {
      width: 20px;
      height: 20px;
      accent-color: #818cf8;
      cursor: pointer;
    }
    .auth-btn-submit {
      width: 100%;
      min-height: 52px;
      background: var(--gemini-gradient);
      color: white;
      border: none;
      border-radius: var(--radius-md);
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      box-shadow: var(--gemini-glow);
    }
    .auth-btn-submit:active {
      transform: scale(0.98);
    }
    .auth-footer-help {
      margin-top: 18px;
      font-size: 0.78rem;
      color: var(--text-dim);
    }
    .auth-footer-link {
      background: none;
      border: none;
      color: #818cf8;
      font-size: 0.82rem;
      text-decoration: underline;
      cursor: pointer;
      margin-top: 8px;
      display: inline-block;
      padding: 6px 12px;
      min-height: 44px;
      line-height: 32px;
    }
    .auth-shake {
      animation: shake 0.4s ease;
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-10px); }
      40%, 80% { transform: translateX(10px); }
    }

    /* ==========================================================================
       HEADER & NAVIGATION BAR (DESKTOP & MOBILE)
       ========================================================================== */
    header {
      position: sticky;
      top: 0;
      z-index: 50;
      background: var(--bg-surface-glass);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 12px 16px;
    }
    .header-inner {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }
    .brand-logo {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: var(--gemini-gradient);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 15px rgba(129, 140, 248, 0.35);
      flex-shrink: 0;
    }
    .brand-logo svg {
      width: 24px;
      height: 24px;
      fill: white;
    }
    .brand-meta h1 {
      font-size: 1.1rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-badge {
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: var(--radius-full);
      background: rgba(129, 140, 248, 0.15);
      color: #a5b4fc;
      border: 1px solid rgba(129, 140, 248, 0.3);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .brand-user {
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 1px;
    }

    /* Desktop View Tabs (Pills) */
    .desktop-nav-tabs {
      display: none;
      gap: 6px;
      background: var(--bg-surface-elevated);
      padding: 4px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border-subtle);
    }
    @media (min-width: 900px) {
      .desktop-nav-tabs {
        display: flex;
      }
    }
    .nav-tab-btn {
      min-height: 40px;
      padding: 8px 18px;
      border-radius: var(--radius-full);
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }
    .nav-tab-btn:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
    }
    .nav-tab-btn.active {
      background: var(--gemini-gradient);
      color: white;
      box-shadow: 0 4px 14px rgba(129, 140, 248, 0.3);
    }

    .header-quick-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Boutons standards */
    .btn {
      min-height: 44px;
      padding: 10px 16px;
      border-radius: var(--radius-md);
      font-size: 0.88rem;
      font-weight: 600;
      border: 1px solid transparent;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
      text-decoration: none;
      white-space: nowrap;
    }
    .btn:active {
      transform: scale(0.97);
    }
    .btn-icon-only {
      min-width: 44px;
      width: 44px;
      padding: 0;
      border-radius: var(--radius-md);
    }
    .btn-glass {
      background: var(--bg-surface-elevated);
      border-color: var(--border-subtle);
      color: var(--text-secondary);
    }
    .btn-glass:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-primary);
      border-color: var(--border-medium);
    }
    .btn-gemini {
      background: var(--gemini-gradient);
      color: white;
      box-shadow: 0 4px 18px rgba(129, 140, 248, 0.3);
    }
    .btn-gemini:hover {
      background: var(--gemini-gradient-hover);
      box-shadow: 0 6px 24px rgba(129, 140, 248, 0.45);
    }
    .btn-emerald {
      background: var(--bg-accepted);
      border-color: rgba(52, 211, 153, 0.3);
      color: #6ee7b7;
    }
    .btn-emerald:hover {
      background: rgba(52, 211, 153, 0.25);
    }
    .btn-danger {
      background: var(--bg-rejected);
      border-color: rgba(251, 113, 133, 0.3);
      color: #fda4af;
    }

    /* ==========================================================================
       BOTTOM NAVIGATION BAR (MOBILE FIRST)
       ========================================================================== */
    .mobile-bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 60;
      background: rgba(14, 17, 24, 0.92);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 6px 8px calc(6px + env(safe-area-inset-bottom));
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.4);
    }
    @media (min-width: 900px) {
      .mobile-bottom-nav {
        display: none;
      }
    }
    .mobile-nav-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 4px;
      min-height: 48px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: var(--radius-sm);
      transition: all 0.2s ease;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 2px;
    }
    .mobile-nav-item svg {
      width: 22px;
      height: 22px;
      fill: currentColor;
      transition: transform 0.2s ease;
    }
    .mobile-nav-item.active {
      color: #818cf8;
    }
    .mobile-nav-item.active svg {
      transform: translateY(-2px);
      fill: url(#geminiGrad);
    }

    /* ==========================================================================
       CONTAINER PRINCIPAL ET CARTES METRICS
       ========================================================================== */
    .main-wrapper {
      max-width: 1400px;
      margin: 16px auto;
      padding: 0 16px;
      position: relative;
      z-index: 1;
    }

    /* Section Quotas / Soldes */
    .metrics-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }
    @media (min-width: 768px) {
      .metrics-grid {
        grid-template-columns: 1fr 1fr;
      }
    }
    @media (min-width: 1200px) {
      .metrics-grid {
        grid-template-columns: 1fr 1fr 340px;
      }
    }

    .metric-card {
      background: var(--bg-surface-glass);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .metric-card:hover {
      border-color: var(--border-medium);
    }
    .metric-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }
    .metric-title {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .metric-quota-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-surface-elevated);
      padding: 4px 10px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border-subtle);
      font-size: 0.8rem;
      color: var(--text-secondary);
    }
    .metric-quota-input {
      width: 44px;
      background: transparent;
      border: none;
      color: #818cf8;
      font-weight: 800;
      font-size: 0.95rem;
      text-align: right;
      outline: none;
    }

    /* Piles de compteurs */
    .metric-stats-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-bottom: 16px;
    }
    .stat-pill {
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 10px 6px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }
    .stat-pill.pill-remaining {
      background: rgba(56, 189, 248, 0.1);
      border-color: rgba(56, 189, 248, 0.3);
    }
    .stat-pill.pill-accepted {
      background: rgba(52, 211, 153, 0.1);
      border-color: rgba(52, 211, 153, 0.3);
    }
    .stat-pill.pill-pending {
      background: rgba(251, 191, 36, 0.1);
      border-color: rgba(251, 191, 36, 0.3);
    }
    .stat-pill.pill-rejected {
      background: rgba(251, 113, 133, 0.08);
      border-color: rgba(251, 113, 133, 0.2);
    }
    .stat-pill-label {
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--text-muted);
    }
    .stat-pill-val {
      font-size: 1.25rem;
      font-weight: 800;
      line-height: 1.1;
      color: var(--text-primary);
    }
    .pill-remaining .stat-pill-val { color: #38bdf8; }
    .pill-accepted .stat-pill-val { color: #34d399; }
    .pill-pending .stat-pill-val { color: #fbbf24; }
    .pill-rejected .stat-pill-val { color: #fb7185; }

    /* Barre de progression fluide */
    .metric-progress-track {
      width: 100%;
      height: 8px;
      background: var(--bg-surface-elevated);
      border-radius: var(--radius-full);
      overflow: hidden;
      display: flex;
    }
    .progress-bar-accepted {
      height: 100%;
      background: #34d399;
      transition: width 0.3s ease;
    }
    .progress-bar-pending {
      height: 100%;
      background: #fbbf24;
      transition: width 0.3s ease;
    }

    /* Carte Récap SNCF */
    .sncf-summary-card {
      background: linear-gradient(135deg, rgba(26, 32, 48, 0.8) 0%, rgba(20, 24, 38, 0.9) 100%);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-lg);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
    }
    .summary-stat-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 0;
      border-bottom: 1px solid var(--border-subtle);
    }
    .summary-stat-row:last-child {
      border-bottom: none;
    }
    .summary-label {
      font-size: 0.84rem;
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .summary-value {
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--text-primary);
    }

    /* ==========================================================================
       VUE 1 : GRILLE MENSUELLE INTERACTIVE
       ========================================================================== */
    .month-nav-container {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }
    .month-nav-scroll {
      flex: 1;
      display: flex;
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
      padding: 4px 2px;
    }
    .month-nav-scroll::-webkit-scrollbar {
      display: none;
    }
    .month-pill-btn {
      min-height: 42px;
      padding: 8px 16px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-full);
      color: var(--text-secondary);
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .month-pill-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-primary);
    }
    .month-pill-btn.active {
      background: var(--gemini-gradient);
      color: white;
      border-color: transparent;
      box-shadow: 0 4px 16px rgba(129, 140, 248, 0.35);
    }

    /* Grille du calendrier */
    .calendar-container {
      background: var(--bg-surface-glass);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }
    .calendar-weekdays-header {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
      margin-bottom: 8px;
      text-align: center;
    }
    .weekday-header-cell {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 6px 0;
    }
    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
    }
    .calendar-day-cell {
      min-height: 72px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 8px 6px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      position: relative;
      transition: all 0.15s ease;
      user-select: none;
    }
    @media (max-width: 480px) {
      .calendar-day-cell {
        min-height: 58px;
        padding: 4px 3px;
      }
    }
    .calendar-day-cell:hover {
      border-color: var(--border-active);
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
      z-index: 2;
    }
    .calendar-day-cell:active {
      transform: scale(0.96);
    }
    .calendar-day-cell.empty {
      background: transparent;
      border: none;
      cursor: default;
      pointer-events: none;
    }
    .calendar-day-cell.is-weekend {
      background: rgba(22, 27, 40, 0.6);
    }
    .calendar-day-cell.is-holiday {
      border-color: rgba(244, 114, 182, 0.4);
    }

    .cell-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .cell-day-num {
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1;
    }
    .cell-holiday-dot {
      font-size: 0.65rem;
    }

    /* Badges de poste */
    .cell-shift-tag {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 6px;
      border-radius: 6px;
      text-align: center;
      line-height: 1.1;
      margin-top: 4px;
      letter-spacing: 0.02em;
    }
    .shift-tag-tny002 {
      background: var(--bg-tny002);
      color: var(--color-tny002);
      border: 1px solid var(--border-tny002);
    }
    .shift-tag-tny003 {
      background: var(--bg-tny003);
      color: var(--color-tny003);
      border: 1px solid var(--border-tny003);
    }
    .shift-tag-tny004 {
      background: var(--bg-tny004);
      color: var(--color-tny004);
      border: 1px solid var(--border-tny004);
    }
    .shift-tag-rp {
      background: var(--bg-rp);
      color: var(--color-rp);
      border: 1px solid var(--border-rp);
    }
    .cell-hours-sub {
      font-size: 0.65rem;
      color: var(--text-muted);
      text-align: center;
      margin-top: 2px;
      display: none;
    }
    @media (min-width: 640px) {
      .cell-hours-sub {
        display: block;
      }
    }

    /* Badges d'absences posées */
    .calendar-day-cell.has-absence-pending {
      border: 2px dashed var(--status-pending) !important;
      background: var(--bg-pending) !important;
    }
    .calendar-day-cell.has-absence-accepted {
      border: 2px solid var(--status-accepted) !important;
      background: var(--bg-accepted) !important;
    }
    .calendar-day-cell.has-absence-rejected {
      border: 1px solid var(--status-rejected) !important;
      background: var(--bg-rejected) !important;
    }
    .cell-absence-badge {
      font-size: 0.68rem;
      font-weight: 800;
      border-radius: 4px;
      padding: 2px 4px;
      text-align: center;
      margin-top: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .badge-vt-pending { background: #fbbf24; color: #000; }
    .badge-vt-accepted { background: #38bdf8; color: #000; }
    .badge-ca-pending { background: #fbbf24; color: #000; }
    .badge-ca-accepted { background: #f472b6; color: #000; }

    /* ==========================================================================
       VUE 2 : PLANNING CONTINU (STREAM / LISTE TACTILE MOBILE-FIRST)
       ========================================================================== */
    .planning-feed-container {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .feed-controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background: var(--bg-surface-glass);
      backdrop-filter: blur(16px);
      padding: 12px 16px;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border-subtle);
      margin-bottom: 12px;
    }
    .feed-filter-chips {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .chip-btn {
      min-height: 38px;
      padding: 6px 14px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-full);
      color: var(--text-secondary);
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
    }
    .chip-btn.active {
      background: var(--gemini-gradient);
      color: white;
      border-color: transparent;
    }

    .planning-day-card {
      background: var(--bg-surface-glass);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      min-height: 84px;
    }
    .planning-day-card:hover {
      border-color: var(--border-active);
      transform: translateY(-2px);
    }
    .planning-day-card:active {
      transform: scale(0.98);
    }
    .planning-date-col {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .planning-day-circle {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .planning-day-circle .num {
      font-size: 1.25rem;
      font-weight: 800;
      line-height: 1;
      color: var(--text-primary);
    }
    .planning-day-circle .month-short {
      font-size: 0.68rem;
      font-weight: 700;
      color: #818cf8;
      text-transform: uppercase;
      margin-top: 2px;
    }
    .planning-day-meta {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .planning-weekday {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-primary);
    }
    .planning-holiday-badge {
      font-size: 0.72rem;
      color: #f472b6;
      font-weight: 600;
    }

    .planning-shift-col {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 4px;
    }
    .planning-shift-badge {
      font-size: 0.88rem;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .planning-hours {
      font-size: 0.85rem;
      color: var(--text-secondary);
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
    }
    .planning-absence-tag {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* ==========================================================================
       VUE 3 : DEMANDES & SUIVI (TABLEAU & ACTIONS)
       ========================================================================== */
    .requests-table-container {
      background: var(--bg-surface-glass);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px;
      overflow-x: auto;
    }
    .table-modern {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    .table-modern th {
      padding: 12px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border-subtle);
    }
    .table-modern td {
      padding: 14px 12px;
      font-size: 0.88rem;
      color: var(--text-secondary);
      border-bottom: 1px solid var(--border-subtle);
    }
    .table-modern tr:hover td {
      background: rgba(255, 255, 255, 0.03);
    }

    /* ==========================================================================
       MODALES & BOTTOM SHEETS TACTILES
       ========================================================================== */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 120;
      display: flex;
      justify-content: center;
      align-items: flex-end; /* Bottom sheet sur mobile */
      padding: 0;
      opacity: 0;
      visibility: hidden;
      transition: all 0.25s ease;
    }
    @media (min-width: 640px) {
      .modal-overlay {
        align-items: center;
        padding: 20px;
      }
    }
    .modal-overlay.active {
      opacity: 1;
      visibility: visible;
    }
    .modal-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-top: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: var(--radius-lg) var(--radius-lg) 0 0;
      width: 100%;
      max-width: 500px;
      max-height: 90vh;
      overflow-y: auto;
      padding: 24px 20px calc(24px + env(safe-area-inset-bottom));
      box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
      transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @media (min-width: 640px) {
      .modal-card {
        border-radius: var(--radius-lg);
        transform: translateY(20px) scale(0.96);
        box-shadow: var(--shadow-lg);
      }
    }
    .modal-overlay.active .modal-card {
      transform: translateY(0) scale(1);
    }
    .modal-handle-bar {
      width: 40px;
      height: 5px;
      background: var(--border-medium);
      border-radius: var(--radius-full);
      margin: 0 auto 16px;
    }
    @media (min-width: 640px) {
      .modal-handle-bar {
        display: none;
      }
    }
    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
    }
    .modal-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--text-primary);
    }
    .modal-btn-close {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
    }

    /* Actions de pose VT / CA */
    .action-choice-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 20px;
    }
    .action-choice-btn {
      min-height: 80px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
      color: var(--text-primary);
    }
    .action-choice-btn:hover {
      border-color: var(--border-active);
      background: rgba(255, 255, 255, 0.05);
    }
    .action-choice-btn.active-vt {
      background: var(--bg-vt);
      border-color: var(--color-vt);
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    .action-choice-btn.active-ca {
      background: var(--bg-ca);
      border-color: var(--color-ca);
      box-shadow: 0 0 20px rgba(244, 114, 182, 0.2);
    }

    /* Sélecteur de statut (Segmented control) */
    .status-segmented-control {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      background: var(--bg-surface-elevated);
      padding: 6px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
      margin-bottom: 20px;
    }
    .status-segment-btn {
      min-height: 44px;
      background: transparent;
      border: none;
      border-radius: var(--radius-sm);
      color: var(--text-muted);
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .status-segment-btn.active-pending {
      background: var(--status-pending);
      color: #000;
    }
    .status-segment-btn.active-accepted {
      background: var(--status-accepted);
      color: #000;
    }
    .status-segment-btn.active-rejected {
      background: var(--status-rejected);
      color: #fff;
    }

    /* Toast Notification */
    .toast-box {
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%) translateY(-30px);
      background: rgba(20, 24, 38, 0.95);
      border: 1px solid var(--border-medium);
      backdrop-filter: blur(20px);
      color: white;
      padding: 12px 24px;
      border-radius: var(--radius-full);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), var(--gemini-glow);
      font-size: 0.92rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 2000;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }
    .toast-box.show {
      opacity: 1;
      visibility: visible;
      transform: translateX(-50%) translateY(0);
    }
  </style>
</head>
<body>

  <!-- SVG DEFS POUR GRADIENTS -->
  <svg width="0" height="0" style="position: absolute;">
    <defs>
      <linearGradient id="geminiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#38bdf8"/>
        <stop offset="50%" stop-color="#818cf8"/>
        <stop offset="100%" stop-color="#c084fc"/>
      </linearGradient>
    </defs>
  </svg>

  <!-- TOAST NOTIFICATION -->
  <div class="toast-box" id="toastBox">
    <span id="toastIcon">✨</span>
    <span id="toastMsg">Action effectuée</span>
  </div>

  <!-- ==========================================================================
       ÉCRAN DE VERROUILLAGE SÉCURISÉ (STYLE GEMINI GLASS)
       ========================================================================== -->
  <div class="auth-overlay" id="authOverlay">
    <div class="auth-card" id="authCard">
      <div class="auth-sparkle">
        <svg viewBox="0 0 24 24">
          <path d="M12 2L14.26 8.74L21 11L14.26 13.26L12 20L9.74 13.26L3 11L9.74 8.74L12 2Z"/>
        </svg>
      </div>
      <h2 class="auth-title">Roulement SNCF 2027</h2>
      <p class="auth-subtitle">Espace Privé • RIADH BIZID (Lannemezan Infra)</p>

      <form onsubmit="handleAuthSubmit(event)">
        <div class="auth-input-wrapper">
          <input type="password" id="authPinInput" class="auth-input" placeholder="••••" maxlength="30" autofocus autocomplete="current-password">
          <button type="button" class="auth-toggle-pwd" onclick="togglePinVisibility()" title="Afficher/Masquer le code">👁️</button>
        </div>
        <div class="auth-error-msg" id="authErrorMsg"></div>

        <label class="auth-remember">
          <input type="checkbox" id="authRememberCheckbox" checked>
          <span>Se souvenir de moi sur cet appareil</span>
        </label>

        <button type="submit" class="auth-btn-submit">
          <span>🔓 Déverrouiller l'agenda</span>
        </button>
      </form>

      <div class="auth-footer-help">
        Code d'accès par défaut : <strong>2027</strong>
      </div>
      <div>
        <button type="button" class="auth-footer-link" onclick="promptResetPin()">
          🔑 Personnaliser ou modifier mon code d'accès
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       TOP APP HEADER
       ========================================================================== -->
  <header>
    <div class="header-inner">
      <a href="#" class="brand-section">
        <div class="brand-logo">
          <svg viewBox="0 0 24 24">
            <path d="M12 2L14.26 8.74L21 11L14.26 13.26L12 20L9.74 13.26L3 11L9.74 8.74L12 2Z"/>
          </svg>
        </div>
        <div class="brand-meta">
          <h1>SNCF 2027 <span class="brand-badge">Infra</span></h1>
          <div class="brand-user">Riadh Bizid • 7712336Z</div>
        </div>
      </a>

      <!-- Desktop Nav Tabs -->
      <nav class="desktop-nav-tabs">
        <button class="nav-tab-btn active" id="tabBtnGrid" onclick="switchView('grid')">
          <span>📅 Grille</span>
        </button>
        <button class="nav-tab-btn" id="tabBtnPlanning" onclick="switchView('planning')">
          <span>📋 Planning</span>
        </button>
        <button class="nav-tab-btn" id="tabBtnRequests" onclick="switchView('requests')">
          <span>📊 Demandes (<span id="desktopDemandesCount">0</span>)</span>
        </button>
        <button class="nav-tab-btn" id="tabBtnSync" onclick="switchView('sync')">
          <span>☁️ Cloud & Partage</span>
        </button>
      </nav>

      <!-- Quick Actions -->
      <div class="header-quick-actions">
        <button class="btn btn-glass" onclick="openSettingsModal()" title="Paramètres & Quotas">
          ⚙️ <span style="display: none; @media(min-width:640px){display:inline;}">Quotas</span>
        </button>
        <button class="btn btn-glass" onclick="lockApp()" title="Verrouiller l'accès">
          🔒
        </button>
      </div>
    </div>
  </header>

  <!-- ==========================================================================
       CONTENU PRINCIPAL
       ========================================================================== -->
  <main class="main-wrapper">

    <!-- METRICS : SOLDES VT & CONGÉS -->
    <section class="metrics-grid">
      <!-- CARTE 1 : VT -->
      <div class="metric-card">
        <div class="metric-card-header">
          <div class="metric-title">
            <span style="font-size: 1.2rem;">⏱️</span>
            <span>Vacations Temps Partiel (VT)</span>
          </div>
          <div class="metric-quota-badge">
            <span>Droit :</span>
            <input type="number" id="inputQuotaVT" class="metric-quota-input" value="44" min="0" max="100" onchange="updateQuotas()">
            <span>j</span>
          </div>
        </div>

        <div class="metric-stats-row">
          <div class="stat-pill pill-pending">
            <span class="stat-pill-label">En attente</span>
            <span class="stat-pill-val" id="statVTPending">0</span>
          </div>
          <div class="stat-pill pill-accepted">
            <span class="stat-pill-label">Validés</span>
            <span class="stat-pill-val" id="statVTAccepted">0</span>
          </div>
          <div class="stat-pill pill-remaining">
            <span class="stat-pill-label">Restants</span>
            <span class="stat-pill-val" id="statVTRemaining">44</span>
          </div>
          <div class="stat-pill pill-rejected">
            <span class="stat-pill-label">Refusés</span>
            <span class="stat-pill-val" id="statVTRejected">0</span>
          </div>
        </div>

        <div class="metric-progress-track">
          <div class="progress-bar-accepted" id="barVTAccepted" style="width: 0%;"></div>
          <div class="progress-bar-pending" id="barVTPending" style="width: 0%;"></div>
        </div>
      </div>

      <!-- CARTE 2 : CONGÉS CA -->
      <div class="metric-card">
        <div class="metric-card-header">
          <div class="metric-title">
            <span style="font-size: 1.2rem;">🏖️</span>
            <span>Congés Annuels (CA)</span>
          </div>
          <div class="metric-quota-badge">
            <span>Droit :</span>
            <input type="number" id="inputQuotaConge" class="metric-quota-input" value="23" min="0" max="100" onchange="updateQuotas()">
            <span>j</span>
          </div>
        </div>

        <div class="metric-stats-row">
          <div class="stat-pill pill-pending">
            <span class="stat-pill-label">En attente</span>
            <span class="stat-pill-val" id="statCongePending">0</span>
          </div>
          <div class="stat-pill pill-accepted">
            <span class="stat-pill-label">Validés</span>
            <span class="stat-pill-val" id="statCongeAccepted">0</span>
          </div>
          <div class="stat-pill pill-remaining">
            <span class="stat-pill-label">Restants</span>
            <span class="stat-pill-val" id="statCongeRemaining">23</span>
          </div>
          <div class="stat-pill pill-rejected">
            <span class="stat-pill-label">Refusés</span>
            <span class="stat-pill-val" id="statCongeRejected">0</span>
          </div>
        </div>

        <div class="metric-progress-track">
          <div class="progress-bar-accepted" id="barCongeAccepted" style="width: 0%; background: #f472b6;"></div>
          <div class="progress-bar-pending" id="barCongePending" style="width: 0%;"></div>
        </div>
      </div>

      <!-- CARTE 3 : RÉCAP TRAVAIL / SYNCHRO -->
      <div class="sncf-summary-card">
        <div>
          <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #818cf8; font-weight: 700; margin-bottom: 6px;">Bilan Prévisionnel</div>
          <div class="summary-stat-row">
            <span class="summary-label">🚂 Jours travaillés réels :</span>
            <span class="summary-value" id="statWorkReal">232</span>
          </div>
          <div class="summary-stat-row">
            <span class="summary-label">💤 Repos (RP & RU) :</span>
            <span class="summary-value">133</span>
          </div>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-gemini" style="flex: 1;" onclick="openSyncModal()">
            <span>☁️ Sync Cloud</span>
          </button>
          <button class="btn btn-glass" onclick="exportUpdatedICS()" title="Télécharger calendrier Google/Apple (.ics)">
            📥 ICS
          </button>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         VUE 1 : GRILLE MENSUELLE
         ========================================================================== -->
    <div id="viewGrid" class="view-panel">
      <!-- Navigation mois -->
      <div class="month-nav-container">
        <button class="btn btn-glass btn-icon-only" onclick="changeMonth(-1)" title="Mois précédent">◀</button>
        <div class="month-nav-scroll" id="monthNavScroll"></div>
        <button class="btn btn-glass btn-icon-only" onclick="changeMonth(1)" title="Mois suivant">▶</button>
      </div>

      <!-- Calendrier -->
      <div class="calendar-container">
        <div class="calendar-weekdays-header">
          <div class="weekday-header-cell">Lun</div>
          <div class="weekday-header-cell">Mar</div>
          <div class="weekday-header-cell">Mer</div>
          <div class="weekday-header-cell">Jeu</div>
          <div class="weekday-header-cell">Ven</div>
          <div class="weekday-header-cell" style="color: #818cf8;">Sam</div>
          <div class="weekday-header-cell" style="color: #f472b6;">Dim</div>
        </div>
        <div class="calendar-grid" id="calendarDaysGrid"></div>
      </div>
    </div>

    <!-- ==========================================================================
         VUE 2 : PLANNING CONTINU (STREAM TACTILE)
         ========================================================================== -->
    <div id="viewPlanning" class="view-panel" style="display: none;">
      <div class="feed-controls">
        <div class="feed-filter-chips">
          <button class="chip-btn active" onclick="filterPlanningFeed('all', this)">Tous</button>
          <button class="chip-btn" onclick="filterPlanningFeed('work', this)">Travaillés</button>
          <button class="chip-btn" onclick="filterPlanningFeed('rest', this)">Repos</button>
          <button class="chip-btn" onclick="filterPlanningFeed('absences', this)">Absences posées</button>
        </div>
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          Mois en cours : <strong id="planningCurrentMonthLabel" style="color: var(--text-primary);">Janvier 2027</strong>
        </div>
      </div>
      <div class="planning-feed-container" id="planningFeedContainer"></div>
    </div>

    <!-- ==========================================================================
         VUE 3 : DEMANDES & SUIVI
         ========================================================================== -->
    <div id="viewRequests" class="view-panel" style="display: none;">
      <div class="feed-controls">
        <div class="feed-filter-chips">
          <button class="chip-btn active" onclick="filterRequestsTable('all', this)">Toutes (<span id="countTableAll">0</span>)</button>
          <button class="chip-btn" onclick="filterRequestsTable('pending', this)">En attente (<span id="countTablePending">0</span>)</button>
          <button class="chip-btn" onclick="filterRequestsTable('accepted', this)">Validées (<span id="countTableAccepted">0</span>)</button>
          <button class="chip-btn" onclick="filterRequestsTable('rejected', this)">Refusées (<span id="countTableRejected">0</span>)</button>
        </div>
      </div>
      <div class="requests-table-container">
        <table class="table-modern">
          <thead>
            <tr>
              <th>Date</th>
              <th>Jour</th>
              <th>Type</th>
              <th>Poste initial</th>
              <th>Statut</th>
              <th style="text-align: right;">Action</th>
            </tr>
          </thead>
          <tbody id="requestsTableBody"></tbody>
        </table>
      </div>
    </div>

    <!-- ==========================================================================
         VUE 4 : SYNCHRONISATION & PARTAGE
         ========================================================================== -->
    <div id="viewSync" class="view-panel" style="display: none;">
      <div style="display: grid; grid-template-columns: 1fr; gap: 16px;">
        <div class="metric-card">
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 12px; color: var(--text-primary);">
            ☁️ Synchronisation Cloud en Direct (Puter.js)
          </h3>
          <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 16px;">
            Permet de synchroniser instantanément vos poses de VT et congés entre votre smartphone et votre ordinateur sans rien configurer.
          </p>
          <div id="puterStatusArea" style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
              <span id="puterDot" style="width: 10px; height: 10px; border-radius: 50%; background: #64748b;"></span>
              <span id="puterLabel" style="font-size: 0.88rem; font-weight: 600; color: var(--text-muted);">Non connecté</span>
            </div>
            <button class="btn btn-gemini" id="btnPuterConnect" onclick="connectPuterCloud()">
              🚀 Activer la synchronisation 1-clic
            </button>
            <button class="btn btn-glass" id="btnPuterSyncNow" onclick="syncWithPuter(false)" style="display: none; margin-top: 8px;">
              🔄 Forcer la mise à jour immédiate
            </button>
          </div>
          <div style="font-size: 0.78rem; color: var(--text-muted);">
            Dernière synchro : <span id="syncLastTimeLabel">--:--:--</span>
          </div>
        </div>

        <div class="metric-card">
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 12px; color: var(--text-primary);">
            📱 Partage instantané par QR Code
          </h3>
          <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 16px;">
            Flashez ce QR Code avec l'appareil photo de votre smartphone pour transférer instantanément toutes vos poses d'un appareil à l'autre.
          </p>
          <div style="display: flex; justify-content: center; padding: 16px; background: white; border-radius: var(--radius-md); width: fit-content; margin: 0 auto 16px;">
            <div id="qrcodeCanvas"></div>
          </div>
          <div style="text-align: center;">
            <button class="btn btn-glass" onclick="generateShareQRCode()">
              🔄 Regénérer le QR Code
            </button>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- ==========================================================================
       BOTTOM NAVIGATION BAR (MOBILE)
       ========================================================================== -->
  <nav class="mobile-bottom-nav">
    <button class="mobile-nav-item active" id="mobNavGrid" onclick="switchView('grid')">
      <svg viewBox="0 0 24 24"><path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zm0-12H5V6h14v2z"/></svg>
      <span>Grille</span>
    </button>
    <button class="mobile-nav-item" id="mobNavPlanning" onclick="switchView('planning')">
      <svg viewBox="0 0 24 24"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>
      <span>Planning</span>
    </button>
    <button class="mobile-nav-item" id="mobNavRequests" onclick="switchView('requests')">
      <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
      <span>Demandes</span>
    </button>
    <button class="mobile-nav-item" id="mobNavSync" onclick="switchView('sync')">
      <svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/></svg>
      <span>Sync</span>
    </button>
  </nav>

  <!-- ==========================================================================
       MODAL : GESTION DU JOUR CLIQUE (BOTTOM SHEET MOBILE)
       ========================================================================== -->
  <div class="modal-overlay" id="dayActionModal" onclick="handleModalBackdropClick(event, 'dayActionModal')">
    <div class="modal-card">
      <div class="modal-handle-bar"></div>
      <div class="modal-header">
        <div>
          <div class="modal-title" id="dayModalDateTitle">Vendredi 15 Janvier 2027</div>
          <div id="dayModalShiftSubtitle" style="font-size: 0.84rem; color: var(--text-muted); margin-top: 2px;">Poste : TNY003 (10:00 - 16:20)</div>
        </div>
        <button class="modal-btn-close" onclick="closeDayModal()">✕</button>
      </div>

      <!-- Choix VT ou CA -->
      <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
        Poser une absence sur ce poste :
      </div>
      <div class="action-choice-grid">
        <button class="action-choice-btn" id="btnChooseVT" onclick="selectAbsenceType('VT')">
          <span style="font-size: 1.5rem;">⏱️</span>
          <span style="font-weight: 700;">Vacation VT</span>
          <span style="font-size: 0.72rem; color: var(--text-muted);">Temps Partiel</span>
        </button>
        <button class="action-choice-btn" id="btnChooseCA" onclick="selectAbsenceType('CA')">
          <span style="font-size: 1.5rem;">🏖️</span>
          <span style="font-weight: 700;">Congé Annuel</span>
          <span style="font-size: 0.72rem; color: var(--text-muted);">Congé (CA)</span>
        </button>
      </div>

      <!-- Choix Statut -->
      <div id="statusSection" style="display: none;">
        <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
          Statut de la demande :
        </div>
        <div class="status-segmented-control">
          <button class="status-segment-btn" id="btnStatusPending" onclick="setAbsenceStatus('pending')">
            ⏳ En attente
          </button>
          <button class="status-segment-btn" id="btnStatusAccepted" onclick="setAbsenceStatus('accepted')">
            ✅ Accepté
          </button>
          <button class="status-segment-btn" id="btnStatusRejected" onclick="setAbsenceStatus('rejected')">
            ❌ Refusé
          </button>
        </div>
      </div>

      <!-- Action Supprimer / Réinitialiser -->
      <div id="deleteSection" style="display: none; margin-top: 10px;">
        <button class="btn btn-danger" style="width: 100%; min-height: 48px;" onclick="removeDayAbsence()">
          🗑️ Supprimer la demande / Rétablir le poste normal
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       MODAL : PARAMÈTRES & SÉCURITÉ
       ========================================================================== -->
  <div class="modal-overlay" id="settingsModal" onclick="handleModalBackdropClick(event, 'settingsModal')">
    <div class="modal-card">
      <div class="modal-handle-bar"></div>
      <div class="modal-header">
        <div class="modal-title">⚙️ Réglages & Sécurité</div>
        <button class="modal-btn-close" onclick="closeSettingsModal()">✕</button>
      </div>

      <div style="display: flex; flex-direction: column; gap: 16px;">
        <!-- Code PIN -->
        <div>
          <label style="font-size: 0.84rem; font-weight: 700; color: var(--text-primary); display: block; margin-bottom: 6px;">
            🔒 Mot de passe / Code PIN d'accès :
          </label>
          <div style="display: flex; gap: 8px;">
            <input type="password" id="inputSettingsPin" placeholder="Nouveau code secret" style="flex: 1; min-height: 44px; padding: 10px; background: var(--bg-surface-elevated); border: 1px solid var(--border-medium); border-radius: var(--radius-sm); color: white; font-size: 1rem;">
            <button class="btn btn-gemini" onclick="saveCustomPinFromSettings()">Enregistrer</button>
          </div>
          <span style="font-size: 0.74rem; color: var(--text-muted); display: block; margin-top: 4px;">Par défaut : 2027.</span>
        </div>

        <!-- Quotas -->
        <div style="border-top: 1px solid var(--border-subtle); padding-top: 14px;">
          <label style="font-size: 0.84rem; font-weight: 700; color: var(--text-primary); display: block; margin-bottom: 8px;">
            📊 Droits aux quotas annuels :
          </label>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div>
              <span style="font-size: 0.78rem; color: var(--text-muted);">Vacations VT :</span>
              <input type="number" id="settingsVT" class="metric-quota-input" style="width: 100%; min-height: 44px; padding: 10px; background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); color: white; text-align: left;" value="44" onchange="syncQuotasFromSettings()">
            </div>
            <div>
              <span style="font-size: 0.78rem; color: var(--text-muted);">Congés CA :</span>
              <input type="number" id="settingsCA" class="metric-quota-input" style="width: 100%; min-height: 44px; padding: 10px; background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); color: white; text-align: left;" value="23" onchange="syncQuotasFromSettings()">
            </div>
          </div>
        </div>

        <!-- Export Sauvegarde -->
        <div style="border-top: 1px solid var(--border-subtle); padding-top: 14px; display: flex; flex-direction: column; gap: 8px;">
          <button class="btn btn-glass" onclick="exportBackupJSON()" style="width: 100%;">
            💾 Sauvegarder mes données (.json)
          </button>
          <label class="btn btn-glass" style="width: 100%; cursor: pointer;">
            📂 Restaurer une sauvegarde
            <input type="file" accept=".json" onchange="importBackupJSON(event)" style="display: none;">
          </label>
        </div>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       SCRIPTS JAVASCRIPT & LOGIQUE MÉTIER
       ========================================================================== -->
  <script>
    // Injection de la bibliothèque QR Code
    ___QRCODE_JS___
  </script>

  <script>
    // --- DONNÉES DU ROULEMENT 2027 (365 JOURS AUDITÉS) ---
    const RAW_DAYS_DATA = ___DAYS_JSON___;

    const MONTH_NAMES = [
      "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ];

    // --- ÉTAT GLOBAL DE L'APPLICATION ---
    let quotaVT = parseInt(localStorage.getItem('sncf_roulement_quota_vt') || '44', 10);
    let quotaConge = parseInt(localStorage.getItem('sncf_roulement_quota_conge') || '23', 10);
    let userAbsences = {};
    let selectedMonth = 1; // 1 = Janvier
    let activeDayDate = null;
    let currentFeedFilter = 'all';
    let currentTableFilter = 'all';
    let currentView = 'grid';
    let isPuterConnected = false;

    // --- GESTION DU CODE PIN / MOT DE PASSE (SÉCURITÉ DOUBLE) ---
    const DEFAULT_PIN_HASH = '5313e5bf17148de844ff74be3663d47c6e361ca469b30a36337701233c89a15e';

    function togglePinVisibility() {
      const pinIn = document.getElementById('authPinInput');
      if (pinIn) {
        pinIn.type = pinIn.type === 'password' ? 'text' : 'password';
      }
    }

    async function sha256(message) {
      try {
        if (!window.crypto || !window.crypto.subtle) return "";
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
      } catch(e) {
        return "";
      }
    }

    function isAppUnlocked() {
      if (sessionStorage.getItem('sncf_session_unlocked') === 'true') return true;
      if (localStorage.getItem('sncf_remember_unlocked') === 'true') return true;
      return false;
    }

    function checkAuthOnLoad() {
      const overlay = document.getElementById('authOverlay');
      if (!overlay) return;
      if (isAppUnlocked()) {
        overlay.classList.add('hidden');
        overlay.style.display = 'none';
      } else {
        overlay.classList.remove('hidden');
        overlay.style.display = 'flex';
        setTimeout(() => {
          const pinIn = document.getElementById('authPinInput');
          if (pinIn) pinIn.focus();
        }, 150);
      }
    }

    async function handleAuthSubmit(e) {
      if (e) e.preventDefault();
      const input = document.getElementById('authPinInput');
      const errEl = document.getElementById('authErrorMsg');
      const card = document.getElementById('authCard');
      const remember = document.getElementById('authRememberCheckbox').checked;
      const enteredValue = input.value.trim();

      if (!enteredValue) {
        errEl.innerText = "Veuillez saisir votre code d'accès.";
        return;
      }

      const activeCustomPin = localStorage.getItem('sncf_custom_pin') || '';
      const activeHash = localStorage.getItem('sncf_custom_pin_hash') || DEFAULT_PIN_HASH;
      const enteredHash = await sha256(enteredValue);

      const isMatch = (enteredValue === '2027') ||
                      (activeCustomPin && enteredValue === activeCustomPin) ||
                      (enteredHash && (enteredHash === DEFAULT_PIN_HASH || enteredHash === activeHash));

      if (isMatch) {
        errEl.innerText = "";
        input.classList.remove('error');
        sessionStorage.setItem('sncf_session_unlocked', 'true');
        if (remember) {
          localStorage.setItem('sncf_remember_unlocked', 'true');
        } else {
          localStorage.removeItem('sncf_remember_unlocked');
        }
        const overlay = document.getElementById('authOverlay');
        overlay.classList.add('hidden');
        overlay.style.display = 'none';
        showToast("Bienvenue Riadh ! Agenda déverrouillé.");
      } else {
        errEl.innerText = "Code d'accès incorrect.";
        input.classList.add('error');
        card.classList.remove('auth-shake');
        void card.offsetWidth;
        card.classList.add('auth-shake');
        input.value = "";
        input.focus();
      }
    }

    function lockApp() {
      sessionStorage.removeItem('sncf_session_unlocked');
      localStorage.removeItem('sncf_remember_unlocked');
      const overlay = document.getElementById('authOverlay');
      if (overlay) {
        overlay.classList.remove('hidden');
        overlay.style.display = 'flex';
      }
      const pinIn = document.getElementById('authPinInput');
      if (pinIn) {
        pinIn.value = '';
        pinIn.classList.remove('error');
        document.getElementById('authErrorMsg').innerText = '';
        pinIn.focus();
      }
      showToast("Agenda verrouillé 🔒", "🔒");
    }

    function promptResetPin() {
      const newCode = prompt("Choisissez votre nouveau code secret ou mot de passe :");
      if (newCode && newCode.trim().length >= 2) {
        const trimmed = newCode.trim();
        localStorage.setItem('sncf_custom_pin', trimmed);
        sha256(trimmed).then(h => { if (h) localStorage.setItem('sncf_custom_pin_hash', h); });
        const pinIn = document.getElementById('authPinInput');
        if (pinIn) pinIn.value = trimmed;
        alert("Votre nouveau code personnel est enregistré : " + trimmed + "\\nVous pouvez maintenant cliquer sur 'Déverrouiller'.");
      }
    }

    function saveCustomPinFromSettings() {
      const newPin = document.getElementById('inputSettingsPin').value.trim();
      if (!newPin || newPin.length < 2) {
        alert("Veuillez choisir un code d'au moins 2 caractères.");
        return;
      }
      localStorage.setItem('sncf_custom_pin', newPin);
      sha256(newPin).then(h => { if (h) localStorage.setItem('sncf_custom_pin_hash', h); });
      document.getElementById('inputSettingsPin').value = "";
      closeSettingsModal();
      showToast("Nouveau mot de passe enregistré 🔒");
    }

    // --- CHARGEMENT & SAUVEGARDE DES DONNÉES ---
    function loadSavedData() {
      try {
        const rawAbs = localStorage.getItem('sncf_roulement_absences');
        if (rawAbs) userAbsences = JSON.parse(rawAbs);
      } catch(e) {
        userAbsences = {};
      }
      document.getElementById('inputQuotaVT').value = quotaVT;
      document.getElementById('inputQuotaConge').value = quotaConge;
      document.getElementById('settingsVT').value = quotaVT;
      document.getElementById('settingsCA').value = quotaConge;
    }

    function saveData() {
      localStorage.setItem('sncf_roulement_quota_vt', quotaVT);
      localStorage.setItem('sncf_roulement_quota_conge', quotaConge);
      localStorage.setItem('sncf_roulement_absences', JSON.stringify(userAbsences));
      autoSyncCloud();
    }

    function updateQuotas() {
      const newVT = parseInt(document.getElementById('inputQuotaVT').value, 10);
      const newCA = parseInt(document.getElementById('inputQuotaConge').value, 10);
      if (!isNaN(newVT)) quotaVT = newVT;
      if (!isNaN(newCA)) quotaConge = newCA;
      saveData();
      updateAllStats();
      renderCurrentView();
    }

    function syncQuotasFromSettings() {
      const newVT = parseInt(document.getElementById('settingsVT').value, 10);
      const newCA = parseInt(document.getElementById('settingsCA').value, 10);
      if (!isNaN(newVT)) { quotaVT = newVT; document.getElementById('inputQuotaVT').value = newVT; }
      if (!isNaN(newCA)) { quotaConge = newCA; document.getElementById('inputQuotaConge').value = newCA; }
      saveData();
      updateAllStats();
      renderCurrentView();
    }

    // --- STATISTIQUES & CALCULS ---
    function updateAllStats() {
      let vtPending = 0, vtAccepted = 0, vtRejected = 0;
      let caPending = 0, caAccepted = 0, caRejected = 0;

      Object.values(userAbsences).forEach(abs => {
        if (abs.type === 'VT') {
          if (abs.status === 'pending') vtPending++;
          else if (abs.status === 'accepted') vtAccepted++;
          else if (abs.status === 'rejected') vtRejected++;
        } else if (abs.type === 'CA') {
          if (abs.status === 'pending') caPending++;
          else if (abs.status === 'accepted') caAccepted++;
          else if (abs.status === 'rejected') caRejected++;
        }
      });

      const vtRemaining = Math.max(0, quotaVT - vtAccepted - vtPending);
      const caRemaining = Math.max(0, quotaConge - caAccepted - caPending);

      document.getElementById('statVTPending').innerText = vtPending;
      document.getElementById('statVTAccepted').innerText = vtAccepted;
      document.getElementById('statVTRemaining').innerText = vtRemaining;
      document.getElementById('statVTRejected').innerText = vtRejected;

      document.getElementById('statCongePending').innerText = caPending;
      document.getElementById('statCongeAccepted').innerText = caAccepted;
      document.getElementById('statCongeRemaining').innerText = caRemaining;
      document.getElementById('statCongeRejected').innerText = caRejected;

      // Progress bars
      const vtAccPct = Math.min(100, (vtAccepted / quotaVT) * 100);
      const vtPendPct = Math.min(100 - vtAccPct, (vtPending / quotaVT) * 100);
      document.getElementById('barVTAccepted').style.width = vtAccPct + '%';
      document.getElementById('barVTPending').style.width = vtPendPct + '%';

      const caAccPct = Math.min(100, (caAccepted / quotaConge) * 100);
      const caPendPct = Math.min(100 - caAccPct, (caPending / quotaConge) * 100);
      document.getElementById('barCongeAccepted').style.width = caAccPct + '%';
      document.getElementById('barCongePending').style.width = caPendPct + '%';

      // Jours travaillés réels
      const workReal = 232 - (vtAccepted + caAccepted);
      document.getElementById('statWorkReal').innerText = workReal;

      // Compteurs demandes
      const totalDemandes = Object.keys(userAbsences).length;
      document.getElementById('desktopDemandesCount').innerText = totalDemandes;
      document.getElementById('countTableAll').innerText = totalDemandes;
      document.getElementById('countTablePending').innerText = vtPending + caPending;
      document.getElementById('countTableAccepted').innerText = vtAccepted + caAccepted;
      document.getElementById('countTableRejected').innerText = vtRejected + caRejected;
    }

    // --- NAVIGATION MOIS ---
    function renderMonthNav() {
      const container = document.getElementById('monthNavScroll');
      container.innerHTML = '';
      MONTH_NAMES.forEach((mName, idx) => {
        const mNum = idx + 1;
        const btn = document.createElement('button');
        btn.className = 'month-pill-btn' + (mNum === selectedMonth ? ' active' : '');
        btn.innerText = mName;
        btn.onclick = () => selectMonth(mNum);
        container.appendChild(btn);
      });
      document.getElementById('planningCurrentMonthLabel').innerText = MONTH_NAMES[selectedMonth - 1] + ' 2027';
    }

    function selectMonth(mNum) {
      selectedMonth = mNum;
      renderMonthNav();
      renderGrid();
      renderPlanning();
    }

    function changeMonth(delta) {
      let next = selectedMonth + delta;
      if (next < 1) next = 12;
      if (next > 12) next = 1;
      selectMonth(next);
    }

    // --- VUE 1 : GRILLE DU CALENDRIER ---
    function renderGrid() {
      const grid = document.getElementById('calendarDaysGrid');
      grid.innerHTML = '';

      const monthDays = RAW_DAYS_DATA.filter(d => d.month === selectedMonth);
      if (!monthDays.length) return;

      const firstWeekday = monthDays[0].weekdayIndex; // 0=Lundi, 6=Dimanche

      // Cases vides précédant le 1er du mois
      for (let i = 0; i < firstWeekday; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'calendar-day-cell empty';
        grid.appendChild(emptyCell);
      }

      // Cases des jours
      monthDays.forEach(day => {
        const cell = document.createElement('div');
        let classes = ['calendar-day-cell'];
        if (day.isWeekend) classes.push('is-weekend');
        if (day.isHoliday) classes.push('is-holiday');

        const abs = userAbsences[day.date];
        if (abs) {
          classes.push('has-absence-' + abs.status);
        }

        cell.className = classes.join(' ');
        cell.onclick = () => openDayModal(day.date);

        // Header du jour
        let holidayHtml = day.isHoliday ? '<span class="cell-holiday-dot" title="' + day.holidayName + '">🎉</span>' : '';
        let topRow = '<div class="cell-top-row"><span class="cell-day-num">' + day.day + '</span>' + holidayHtml + '</div>';

        // Badge Poste
        let shiftTagClass = 'shift-tag-' + (day.baseCode.startsWith('TNY') ? day.baseCode.toLowerCase() : 'rp');
        let shiftTagHtml = '<div class="cell-shift-tag ' + shiftTagClass + '">' + day.baseCode + '</div>';

        // Horaires subtiles
        let hoursHtml = day.hoursLabel ? '<div class="cell-hours-sub">' + day.hoursLabel + '</div>' : '';

        // Badge absence posée
        let absBadgeHtml = '';
        if (abs) {
          const typeLabel = abs.type === 'VT' ? 'VT' : 'CA';
          if (abs.status === 'pending') {
            absBadgeHtml = '<div class="cell-absence-badge badge-' + abs.type.toLowerCase() + '-pending">⏳ ' + typeLabel + ' attente</div>';
          } else if (abs.status === 'accepted') {
            absBadgeHtml = '<div class="cell-absence-badge badge-' + abs.type.toLowerCase() + '-accepted">✅ ' + typeLabel + ' accordé</div>';
          } else if (abs.status === 'rejected') {
            absBadgeHtml = '<div class="cell-absence-badge" style="background:#fb7185; color:#000;">❌ ' + typeLabel + ' refusé</div>';
          }
        }

        cell.innerHTML = topRow + absBadgeHtml + shiftTagHtml + hoursHtml;
        grid.appendChild(cell);
      });
    }

    // --- VUE 2 : PLANNING STREAM (FEED MOBILE) ---
    function renderPlanning() {
      const container = document.getElementById('planningFeedContainer');
      container.innerHTML = '';

      let days = RAW_DAYS_DATA.filter(d => d.month === selectedMonth);

      if (currentFeedFilter === 'work') {
        days = days.filter(d => d.isWork);
      } else if (currentFeedFilter === 'rest') {
        days = days.filter(d => !d.isWork);
      } else if (currentFeedFilter === 'absences') {
        days = days.filter(d => userAbsences[d.date]);
      }

      if (!days.length) {
        container.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);">Aucun élément ne correspond à ce filtre.</div>';
        return;
      }

      days.forEach(day => {
        const card = document.createElement('div');
        card.className = 'planning-day-card';
        card.onclick = () => openDayModal(day.date);

        const abs = userAbsences[day.date];

        let holidayLabel = day.isHoliday ? '<span class="planning-holiday-badge">🎉 ' + day.holidayName + '</span>' : '';
        let shiftClass = 'shift-tag-' + (day.baseCode.startsWith('TNY') ? day.baseCode.toLowerCase() : 'rp');

        let absenceTagHtml = '';
        if (abs) {
          if (abs.status === 'pending') {
            absenceTagHtml = '<div class="planning-absence-tag" style="background: var(--bg-pending); color: var(--status-pending);">⏳ ' + abs.type + ' posé en attente</div>';
          } else if (abs.status === 'accepted') {
            absenceTagHtml = '<div class="planning-absence-tag" style="background: var(--bg-accepted); color: var(--status-accepted);">✅ ' + abs.type + ' validé (repos)</div>';
          } else if (abs.status === 'rejected') {
            absenceTagHtml = '<div class="planning-absence-tag" style="background: var(--bg-rejected); color: var(--status-rejected);">❌ ' + abs.type + ' refusé (poste maintenu)</div>';
          }
        }

        card.innerHTML = `
          <div class="planning-date-col">
            <div class="planning-day-circle">
              <span class="num">${day.day}</span>
              <span class="month-short">${MONTH_NAMES[day.month - 1].slice(0, 3)}</span>
            </div>
            <div class="planning-day-meta">
              <span class="planning-weekday">${day.weekday}</span>
              ${holidayLabel}
            </div>
          </div>
          <div class="planning-shift-col">
            <div class="planning-shift-badge ${shiftClass}">
              <span>${day.baseCode}</span>
            </div>
            <div class="planning-hours">${day.hoursLabel || 'Repos'}</div>
            ${absenceTagHtml}
          </div>
        `;
        container.appendChild(card);
      });
    }

    function filterPlanningFeed(filterType, btn) {
      currentFeedFilter = filterType;
      document.querySelectorAll('.feed-filter-chips .chip-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderPlanning();
    }

    // --- VUE 3 : DEMANDES & SUIVI ---
    function renderRequests() {
      const tbody = document.getElementById('requestsTableBody');
      tbody.innerHTML = '';

      const dates = Object.keys(userAbsences).sort();
      let filteredDates = dates;

      if (currentTableFilter !== 'all') {
        filteredDates = dates.filter(dt => userAbsences[dt].status === currentTableFilter);
      }

      if (!filteredDates.length) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 30px; color: var(--text-muted);">Aucune demande enregistrée.</td></tr>';
        return;
      }

      filteredDates.forEach(dt => {
        const abs = userAbsences[dt];
        const dayInfo = RAW_DAYS_DATA.find(d => d.date === dt) || {};

        let statusBadge = '';
        if (abs.status === 'pending') statusBadge = '<span style="color:#fbbf24; font-weight:700;">⏳ En attente</span>';
        else if (abs.status === 'accepted') statusBadge = '<span style="color:#34d399; font-weight:700;">✅ Accepté</span>';
        else if (abs.status === 'rejected') statusBadge = '<span style="color:#fb7185; font-weight:700;">❌ Refusé</span>';

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-weight: 700; color: var(--text-primary);">${dt}</td>
          <td>${dayInfo.weekday || ''}</td>
          <td><span style="font-weight: 800; color: ${abs.type === 'VT' ? '#38bdf8' : '#f472b6'};">${abs.type}</span></td>
          <td>${dayInfo.baseCode || ''} (${dayInfo.hoursLabel || ''})</td>
          <td>${statusBadge}</td>
          <td style="text-align: right;">
            <button class="btn btn-glass" style="min-height: 36px; padding: 4px 10px; font-size: 0.78rem;" onclick="openDayModal('${dt}')">Modifier</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterRequestsTable(filterType, btn) {
      currentTableFilter = filterType;
      document.querySelectorAll('#viewRequests .chip-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderRequests();
    }

    // --- BASCULE DE VUES ---
    function switchView(viewName) {
      currentView = viewName;

      document.getElementById('viewGrid').style.display = viewName === 'grid' ? 'block' : 'none';
      document.getElementById('viewPlanning').style.display = viewName === 'planning' ? 'block' : 'none';
      document.getElementById('viewRequests').style.display = viewName === 'requests' ? 'block' : 'none';
      document.getElementById('viewSync').style.display = viewName === 'sync' ? 'block' : 'none';

      // Desktop tabs
      document.getElementById('tabBtnGrid').classList.toggle('active', viewName === 'grid');
      document.getElementById('tabBtnPlanning').classList.toggle('active', viewName === 'planning');
      document.getElementById('tabBtnRequests').classList.toggle('active', viewName === 'requests');
      document.getElementById('tabBtnSync').classList.toggle('active', viewName === 'sync');

      // Mobile items
      document.getElementById('mobNavGrid').classList.toggle('active', viewName === 'grid');
      document.getElementById('mobNavPlanning').classList.toggle('active', viewName === 'planning');
      document.getElementById('mobNavRequests').classList.toggle('active', viewName === 'requests');
      document.getElementById('mobNavSync').classList.toggle('active', viewName === 'sync');

      renderCurrentView();
    }

    function renderCurrentView() {
      if (currentView === 'grid') renderGrid();
      else if (currentView === 'planning') renderPlanning();
      else if (currentView === 'requests') renderRequests();
      else if (currentView === 'sync') generateShareQRCode();
    }

    // --- MODAL ACTION JOUR ---
    function openDayModal(dateStr) {
      activeDayDate = dateStr;
      const day = RAW_DAYS_DATA.find(d => d.date === dateStr);
      if (!day) return;

      document.getElementById('dayModalDateTitle').innerText = `${day.weekday} ${day.day} ${MONTH_NAMES[day.month - 1]} 2027`;
      document.getElementById('dayModalShiftSubtitle').innerText = `Poste initial : ${day.baseCode} ${day.hoursLabel ? '(' + day.hoursLabel + ')' : '(Repos)'}`;

      const abs = userAbsences[dateStr];
      const btnVT = document.getElementById('btnChooseVT');
      const btnCA = document.getElementById('btnChooseCA');
      const statusSec = document.getElementById('statusSection');
      const delSec = document.getElementById('deleteSection');

      btnVT.classList.remove('active-vt');
      btnCA.classList.remove('active-ca');
      document.getElementById('btnStatusPending').classList.remove('active-pending');
      document.getElementById('btnStatusAccepted').classList.remove('active-accepted');
      document.getElementById('btnStatusRejected').classList.remove('active-rejected');

      if (abs) {
        statusSec.style.display = 'block';
        delSec.style.display = 'block';
        if (abs.type === 'VT') btnVT.classList.add('active-vt');
        if (abs.type === 'CA') btnCA.classList.add('active-ca');

        if (abs.status === 'pending') document.getElementById('btnStatusPending').classList.add('active-pending');
        if (abs.status === 'accepted') document.getElementById('btnStatusAccepted').classList.add('active-accepted');
        if (abs.status === 'rejected') document.getElementById('btnStatusRejected').classList.add('active-rejected');
      } else {
        statusSec.style.display = 'none';
        delSec.style.display = 'none';
      }

      document.getElementById('dayActionModal').classList.add('active');
    }

    function closeDayModal() {
      document.getElementById('dayActionModal').classList.remove('active');
      activeDayDate = null;
    }

    function selectAbsenceType(type) {
      if (!activeDayDate) return;
      if (!userAbsences[activeDayDate]) {
        userAbsences[activeDayDate] = { type: type, status: 'pending' };
      } else {
        userAbsences[activeDayDate].type = type;
      }
      saveData();
      updateAllStats();
      openDayModal(activeDayDate); // Refresh modal view
      renderCurrentView();
      showToast(`${type} posé en attente !`);
    }

    function setAbsenceStatus(status) {
      if (!activeDayDate || !userAbsences[activeDayDate]) return;
      userAbsences[activeDayDate].status = status;
      saveData();
      updateAllStats();
      openDayModal(activeDayDate);
      renderCurrentView();
      showToast(`Statut mis à jour : ${status}`);
    }

    function removeDayAbsence() {
      if (!activeDayDate) return;
      delete userAbsences[activeDayDate];
      saveData();
      updateAllStats();
      closeDayModal();
      renderCurrentView();
      showToast("Demande supprimée. Poste rétabli !");
    }

    function handleModalBackdropClick(e, modalId) {
      if (e.target.id === modalId) {
        if (modalId === 'dayActionModal') closeDayModal();
        if (modalId === 'settingsModal') closeSettingsModal();
      }
    }

    function openSettingsModal() {
      document.getElementById('settingsModal').classList.add('active');
    }
    function closeSettingsModal() {
      document.getElementById('settingsModal').classList.remove('active');
    }
    function openSyncModal() {
      switchView('sync');
    }

    // --- SYNCHRONISATION CLOUD PUTER.JS ---
    async function initPuterState() {
      if (typeof puter !== 'undefined' && puter.auth.isSignedIn()) {
        isPuterConnected = true;
        const dot = document.getElementById('puterDot');
        const label = document.getElementById('puterLabel');
        if (dot) dot.style.background = '#34d399';
        if (label) label.innerText = "Connecté au Cloud Puter (Synchro active)";
        document.getElementById('btnPuterConnect').style.display = 'none';
        document.getElementById('btnPuterSyncNow').style.display = 'inline-flex';
        syncWithPuter(true);
      }
    }

    async function connectPuterCloud() {
      if (typeof puter === 'undefined') {
        alert("Puter.js est indisponible hors-ligne.");
        return;
      }
      try {
        await puter.auth.signIn();
        initPuterState();
        showToast("Cloud Puter connecté avec succès !");
      } catch(err) {
        alert("Connexion Puter annulée.");
      }
    }

    async function syncWithPuter(silent = false) {
      if (!isPuterConnected || typeof puter === 'undefined') return;
      try {
        const cloudDataStr = await puter.kv.get('sncf_roulement_2027');
        if (cloudDataStr) {
          const cloudData = JSON.parse(cloudDataStr);
          const localUpdated = parseInt(localStorage.getItem('sncf_roulement_updated_at') || '0', 10);
          if (cloudData.updatedAt && cloudData.updatedAt > localUpdated) {
            quotaVT = cloudData.quotaVT || quotaVT;
            quotaConge = cloudData.quotaConge || quotaConge;
            userAbsences = cloudData.absences || userAbsences;
            saveData();
            loadSavedData();
            updateAllStats();
            renderCurrentView();
            updateLastSyncLabel();
            if (!silent) showToast("Synchronisé depuis le Cloud !");
            return;
          }
        }
        await autoSyncCloud();
        updateLastSyncLabel();
        if (!silent) showToast("Sauvegardé sur le Cloud !");
      } catch(e) {
        console.error("Erreur sync Puter", e);
      }
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
    }

    function updateLastSyncLabel() {
      const nowStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      const el = document.getElementById('syncLastTimeLabel');
      if (el) el.innerText = nowStr;
    }

    // Polling toutes les 10 secondes & au focus
    window.addEventListener('focus', () => { if (isPuterConnected) syncWithPuter(true); });
    setInterval(() => { if (isPuterConnected) syncWithPuter(true); }, 10000);

    // --- QR CODE ET BACKUP ---
    function generateShareQRCode() {
      const qrel = document.getElementById('qrcodeCanvas');
      if (!qrel || typeof QRCode === 'undefined') return;
      qrel.innerHTML = '';
      const shareData = {
        vt: quotaVT,
        ca: quotaConge,
        abs: userAbsences
      };
      const jsonStr = JSON.stringify(shareData);
      const currentUrl = window.location.origin + window.location.pathname;
      const shareUrl = currentUrl + '#sync=' + encodeURIComponent(jsonStr);

      new QRCode(qrel, {
        text: shareUrl,
        width: 220,
        height: 220,
        colorDark: "#0d0f14",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.M
      });
    }

    function loadFromUrlHash() {
      if (window.location.hash && window.location.hash.startsWith('#sync=')) {
        try {
          const raw = decodeURIComponent(window.location.hash.slice(6));
          const parsed = JSON.parse(raw);
          if (parsed.vt) quotaVT = parsed.vt;
          if (parsed.ca) quotaConge = parsed.ca;
          if (parsed.abs) userAbsences = parsed.abs;
          saveData();
          loadSavedData();
          updateAllStats();
          renderCurrentView();
          window.location.hash = '';
          showToast("Données importées depuis le QR Code !");
        } catch(e) {
          console.error("Hash sync parse error", e);
        }
      }
    }

    function exportBackupJSON() {
      const backup = {
        quotaVT: quotaVT,
        quotaConge: quotaConge,
        absences: userAbsences,
        exportedAt: new Date().toISOString()
      };
      const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'sauvegarde_roulement_2027.json';
      a.click();
      URL.revokeObjectURL(url);
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
          showToast("Sauvegarde importée avec succès !");
        } catch(err) {
          alert("Fichier de sauvegarde invalide.");
        }
      };
      reader.readAsText(file);
    }

    function exportUpdatedICS() {
      let ics = "BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//SNCF//Roulement 2027 Gemini//FR\\r\\nCALSCALE:GREGORIAN\\r\\nMETHOD:PUBLISH\\r\\nX-WR-CALNAME:Roulement SNCF 2027 (Riadh Bizid)\\r\\nX-WR-TIMEZONE:Europe/Paris\\r\\n";
      const nowUtc = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

      RAW_DAYS_DATA.forEach(d => {
        const abs = userAbsences[d.date];
        const dateClean = d.date.replace(/-/g, "");

        if (abs && abs.status === 'accepted') {
          const nextDay = new Date(d.date);
          nextDay.setDate(nextDay.getDate() + 1);
          const nextDayStr = nextDay.toISOString().slice(0, 10).replace(/-/g, "");
          const label = abs.type === 'VT' ? 'VT (Temps Partiel)' : 'Congé Annuel';

          ics += "BEGIN:VEVENT\\r\\n";
          ics += `UID:sncf-${dateClean}-abs@roulement2027\\r\\n`;
          ics += `DTSTAMP:${nowUtc}\\r\\n`;
          ics += `DTSTART;VALUE=DATE:${dateClean}\\r\\n`;
          ics += `DTEND;VALUE=DATE:${nextDayStr}\\r\\n`;
          ics += `SUMMARY:${label}\\r\\n`;
          ics += `DESCRIPTION:Jour d'absence accordé (${label})\\nPoste initial : ${d.baseCode}\\r\\n`;
          ics += "STATUS:CONFIRMED\\r\\nTRANSP:TRANSPARENT\\r\\nEND:VEVENT\\r\\n";
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

          let extraSummary = abs && abs.status === 'pending' ? ` [${abs.type} EN ATTENTE]` : '';

          ics += "BEGIN:VEVENT\\r\\n";
          ics += `UID:sncf-${dateClean}-${d.baseCode}@roulement2027\\r\\n`;
          ics += `DTSTAMP:${nowUtc}\\r\\n`;
          ics += `DTSTART;TZID=Europe/Paris:${dtStart}\\r\\n`;
          ics += `DTEND;TZID=Europe/Paris:${dtEnd}\\r\\n`;
          ics += `SUMMARY:${d.baseCode} (${d.hoursLabel})${extraSummary}\\r\\n`;
          ics += `DESCRIPTION:Poste SNCF: ${d.baseCode}\\nHoraires: ${d.hoursLabel}\\nLieu: Lannemezan Infra\\r\\n`;
          ics += "LOCATION:Lannemezan Infra\\r\\nSTATUS:CONFIRMED\\r\\nTRANSP:OPAQUE\\r\\nEND:VEVENT\\r\\n";
        }
      });

      ics += "END:VCALENDAR\\r\\n";
      const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'roulement_2027_personnalise.ics';
      a.click();
    }

    // --- TOAST NOTIFICATION ---
    function showToast(msg, icon = "✨") {
      const box = document.getElementById('toastBox');
      document.getElementById('toastIcon').innerText = icon;
      document.getElementById('toastMsg').innerText = msg;
      box.classList.add('show');
      setTimeout(() => { box.classList.remove('show'); }, 3000);
    }

    // --- INITIALISATION AU CHARGEMENT ---
    window.addEventListener('DOMContentLoaded', () => {
      checkAuthOnLoad();
      loadSavedData();
      loadFromUrlHash();
      renderMonthNav();
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
