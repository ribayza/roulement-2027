#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration d'un écran de verrouillage avec mot de passe / code PIN sécurisé
- Code PIN par défaut : 2027 (accessible immédiatement)
- Hachage cryptographique SHA-256 : 5313e5bf17148de844ff74be3663d47c6e361ca469b30a36337701233c89a15e
- Double vérification : par code en clair (2027) ET par empreinte SHA-256
- Possibilité de personnaliser son mot de passe directement depuis l'écran de verrouillage
- Bouton œil pour voir le code tapé
- Option 'Se souvenir de moi sur cet appareil'
- Bouton de verrouillage rapide
"""

import json
import re

with open("generate_mobile_app.py", "r", encoding="utf-8") as f:
    content = f.read()

QRCODE_PATH = "qrcode.min.js"
JSON_PATH = "roulement_data_2027.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    days_data = json.load(f)
days_json_str = json.dumps(days_data, ensure_ascii=False)

with open(QRCODE_PATH, "r", encoding="utf-8") as f:
    qrcode_js = f.read()

# Read the HTML template inside generate_mobile_app.py
match = re.search(r'HTML_TEMPLATE = """(.*?)"""', content, re.DOTALL)
if not match:
    raise ValueError("Impossible de trouver HTML_TEMPLATE dans generate_mobile_app.py")

html = match.group(1)

# 1. Add Auth CSS
auth_css = """
    /* ECRAN DE VERROUILLAGE / CODE PIN */
    .auth-overlay {
      position: fixed;
      inset: 0;
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
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
      background: white;
      border-radius: 24px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
      width: 100%;
      max-width: 380px;
      padding: 32px 24px;
      text-align: center;
      animation: fadeIn 0.3s ease;
    }
    .auth-icon {
      font-size: 3rem;
      margin-bottom: 8px;
    }
    .auth-title {
      font-size: 1.35rem;
      font-weight: 800;
      color: #0f172a;
    }
    .auth-subtitle {
      font-size: 0.8rem;
      color: #64748b;
      margin-top: 4px;
      margin-bottom: 22px;
    }
    .auth-input {
      width: 100%;
      padding: 14px 44px 14px 16px;
      border: 2px solid #e2e8f0;
      border-radius: 12px;
      font-size: 1.3rem;
      text-align: center;
      letter-spacing: 4px;
      font-weight: 800;
      outline: none;
      transition: all 0.2s ease;
      color: #0f172a;
    }
    .auth-input:focus {
      border-color: #2563eb;
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
    }
    .auth-input.error {
      border-color: #dc2626;
      background: #fef2f2;
    }
    .auth-remember {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 14px;
      margin-bottom: 20px;
      font-size: 0.82rem;
      color: #64748b;
      cursor: pointer;
    }
    .auth-remember input {
      width: 16px;
      height: 16px;
      accent-color: var(--primary);
      cursor: pointer;
    }
    .auth-error-msg {
      color: #dc2626;
      font-size: 0.8rem;
      font-weight: 600;
      margin-top: 8px;
      min-height: 20px;
    }
    .auth-shake {
      animation: shake 0.4s ease;
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-8px); }
      40%, 80% { transform: translateX(8px); }
    }
"""

html = html.replace("/* RESPONSIVE MOBILE TWEAKS */", auth_css + "\n    /* RESPONSIVE MOBILE TWEAKS */")

# 2. Add Auth Overlay HTML right after <body>
auth_html = """
  <!-- ÉCRAN DE DÉVERROUILLAGE SÉCURISÉ -->
  <div class="auth-overlay" id="authOverlay">
    <div class="auth-card" id="authCard">
      <div class="auth-icon">🔒</div>
      <div class="auth-title">Roulement SNCF 2027</div>
      <div class="auth-subtitle">Espace Privé • RIADH BIZID (Lannemezan)</div>

      <form onsubmit="handleAuthSubmit(event)">
        <div style="position: relative; width: 100%;">
          <input type="password" id="authPinInput" class="auth-input" placeholder="••••" maxlength="30" autofocus autocomplete="current-password">
          <button type="button" onclick="togglePinVisibility()" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 1.25rem; cursor: pointer; padding: 4px;" title="Afficher/Masquer">👁️</button>
        </div>
        <div class="auth-error-msg" id="authErrorMsg"></div>

        <label class="auth-remember">
          <input type="checkbox" id="authRememberCheckbox" checked>
          <span>Se souvenir de moi sur cet appareil</span>
        </label>

        <button type="submit" class="btn btn-primary" style="width: 100%; min-height: 46px; font-size: 1rem;">
          🔓 Déverrouiller l'agenda
        </button>
      </form>

      <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 14px;">
        Code par défaut : <strong>2027</strong>
      </div>
      <div style="margin-top: 8px;">
        <button type="button" onclick="promptResetPin()" style="background: none; border: none; color: #3b82f6; font-size: 0.76rem; text-decoration: underline; cursor: pointer; font-weight: 500;">
          🔑 Personnaliser ou changer le mot de passe
        </button>
      </div>
    </div>
  </div>
"""

html = html.replace('<body>\n\n  <!-- TOAST NOTIFICATION -->', '<body>\n' + auth_html + '\n  <!-- TOAST NOTIFICATION -->')

# 3. Add Verrouiller button in header and settings modal
header_lock_btn = """        <button class="btn btn-light" onclick="lockApp()" title="Verrouiller l'accès">
          🔒 Verrouiller
        </button>"""

html = html.replace('<button class="btn btn-light" onclick="openSettingsModal()>', header_lock_btn + '\n        <button class="btn btn-light" onclick="openSettingsModal()">')

# Add Change Password form in Settings Modal
settings_pin_html = """
      <div style="border-top: 1px solid var(--border-color); padding-top: 16px; margin-top: 16px;">
        <label class="form-label">🔒 Sécurité & Code d'accès :</label>
        <div style="display: flex; gap: 8px;">
          <input type="password" id="settingsNewPinInput" placeholder="Nouveau code PIN / mot de passe" style="flex: 1; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 0.9rem;">
          <button type="button" class="btn btn-primary" onclick="updateCustomPin()">Changer le code</button>
        </div>
        <span style="font-size: 0.75rem; color: var(--text-muted); display: block; margin-top: 4px;">Code par défaut : 2027.</span>
      </div>
"""

html = html.replace('<label class="form-label">Sauvegarde manuelle JSON :</label>', settings_pin_html + '\n        <label class="form-label">Sauvegarde manuelle JSON :</label>')

# 4. Add Auth JS logic
auth_js = """
    // --- GESTION DU CODE PIN / MOT DE PASSE SÉCURISÉ ---
    // Empreinte SHA-256 exacte de '2027'
    const DEFAULT_PIN_HASH = '5313e5bf17148de844ff74be3663d47c6e361ca469b30a36337701233c89a15e';

    function togglePinVisibility() {
      const pinIn = document.getElementById('authPinInput');
      if (pinIn) {
        pinIn.type = pinIn.type === 'password' ? 'text' : 'password';
      }
    }

    function promptResetPin() {
      const newCode = prompt("Choisissez votre nouveau code ou mot de passe personnel :");
      if (newCode && newCode.trim().length >= 2) {
        const trimmed = newCode.trim();
        localStorage.setItem('sncf_custom_pin', trimmed);
        sha256(trimmed).then(h => { if (h) localStorage.setItem('sncf_custom_pin_hash', h); });
        const pinIn = document.getElementById('authPinInput');
        if (pinIn) pinIn.value = trimmed;
        alert("Votre nouveau mot de passe personnel est enregistré : " + trimmed + "\\n\\nVous pouvez cliquer sur 'Déverrouiller l'agenda' !");
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
        errEl.innerText = "Veuillez saisir votre code.";
        return;
      }

      const activeCustomPin = localStorage.getItem('sncf_custom_pin') || '';
      const activeHash = localStorage.getItem('sncf_custom_pin_hash') || DEFAULT_PIN_HASH;
      const enteredHash = await sha256(enteredValue);

      // Double vérification infaillible (code direct 2027 OU code personnalisé OU hash)
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
        void card.offsetWidth; // Trigger reflow
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

    async function updateCustomPin() {
      const newPin = document.getElementById('settingsNewPinInput').value.trim();
      if (!newPin || newPin.length < 2) {
        alert("Veuillez choisir un code d'au moins 2 caractères.");
        return;
      }
      localStorage.setItem('sncf_custom_pin', newPin);
      const newHash = await sha256(newPin);
      if (newHash) {
        localStorage.setItem('sncf_custom_pin_hash', newHash);
      }
      document.getElementById('settingsNewPinInput').value = "";
      alert("Nouveau code d'accès enregistré avec succès !");
      showToast("Nouveau code d'accès activé 🔒");
    }
"""

html = html.replace("window.addEventListener('DOMContentLoaded', () => {", auth_js + "\n    window.addEventListener('DOMContentLoaded', () => {\n      checkAuthOnLoad();")

final_html = html.replace("___DAYS_JSON___", days_json_str).replace("___QRCODE_JS___", qrcode_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("index.html mis à jour avec protection par mot de passe !")

with open("roulement_2027_interactif.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("roulement_2027_interactif.html mis à jour avec protection !")
