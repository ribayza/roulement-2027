# Agenda Roulement SNCF 2027 (Lannemezan Infra)

Ce dossier contient les fichiers d'agenda prêts à être importés dans **Google Agenda** (ainsi qu'Apple Calendrier, Outlook, etc.) calculés à partir du document officiel `roulement 2027.pdf`.

---

## 📅 Synthèse du Roulement 2027

- **Total de l'année 2027** : 365 jours
  - **TNY002** : 78 jours
  - **TNY003** : 77 jours
  - **TNY004** : 77 jours
  - **RP (Repos Périodique)** : 121 jours
  - **RU (Repos Unique / supplémentaire)** : 12 jours
- **Total de journées de travail** : 232 jours
- **Total de journées de repos** : 133 jours

---

## ⏰ Règles des Horaires Appliquées

### 1. Jours de semaine normaux (Lundi au Vendredi, hors jours fériés)
- **TNY002** : `03h50` – `10h00` (durée 6h10)
- **TNY003** : `10h00` – `16h20` (durée 6h20)
- **TNY004** : `16h20` – `00h00 (Minuit)` (durée 7h40)

### 2. Samedis, Dimanches et Jours Fériés (France métropolitaine 2027)
- **TNY002** : `04h50` – `12h50` (durée 8h00)
- **TNY003** : `12h40` – `18h30` (durée 5h50)
- **TNY004** : `18h30` – `00h00 (Minuit)` (durée 5h30)

---

## 🇫🇷 Vérification des 11 Jours Fériés 2027

| Date | Jour | Fête | Statut Roulement | Horaires appliqués |
| :--- | :--- | :--- | :--- | :--- |
| **01/01/2027** | Vendredi | Jour de l'An | **RP** (Repos) | Journée libre |
| **29/03/2027** | Lundi | Lundi de Pâques | **RU** (Repos) | Journée libre |
| **01/05/2027** | Samedi | Fête du Travail | **RP** (Repos) | Journée libre |
| **06/05/2027** | Jeudi | **Ascension** | **TNY002** | **04h50 – 12h50** (Horaires Férié) |
| **08/05/2027** | Samedi | Victoire 1945 | **RP** (Repos) | Journée libre |
| **17/05/2027** | Lundi | **Lundi de Pentecôte** | **TNY003** | **12h40 – 18h30** (Horaires Férié) |
| **14/07/2027** | Mercredi | **Fête Nationale** | **TNY002** | **04h50 – 12h50** (Horaires Férié) |
| **15/08/2027** | Dimanche | Assomption | **RP** (Repos) | Journée libre |
| **01/11/2027** | Lundi | **Toussaint** | **TNY003** | **12h40 – 18h30** (Horaires Férié) |
| **11/11/2027** | Jeudi | **Armistice 1918** | **TNY004** | **18h30 – 00h00** (Horaires Férié) |
| **25/12/2027** | Samedi | Noël | **RP** (Repos) | Journée libre |

---

## 📁 Fichiers Disponibles

1. **`index.html` / `roulement_2027_interactif.html` (⭐ Application Interactive)** :
   - Application Web complète autonome (aucun serveur requis, fonctionne hors-ligne).
   - Gestionnaire des soldes **VT (44 j)** et **Congés (23 j)** personnalisables.
   - Workflow d'approbation complet : **Posé (En attente)**, **Accepté (Validé)**, **Refusé**.
   - Calcul des soldes restants en temps réel.
   - Vue Mensuelle, Vue Annuelle panoramique, et Vue Tableau des demandes.
   - Export de l'agenda `.ics` mis à jour intégrant les absences acceptées !
   - Sauvegarde automatique locale (localStorage) + Export/Import JSON.
2. **`roulement_2027_travail.ics` (Recommandé pour Google Agenda)** :
   - Contient uniquement vos **232 journées de travail** avec les horaires précis, le lieu (*Lannemezan Infra*) et le détail dans la description.
   - Idéal pour garder votre agenda clair et bien lisible.
3. **`roulement_2027_complet.ics`** :
   - Contient l'intégralité de l'année (les **232 journées de travail** + les **133 jours de repos** RP et RU affichés en événements "Journée entière" non bloquants).
4. **`roulement_2027_travail.csv`** et **`roulement_2027_complet.csv`** :
   - Format tableur CSV au standard Google Calendar.
5. **`generer_agenda_2027.py`** & **`audit_complet.py`** :
   - Scripts Python d'extraction et d'audit intégral du roulement.

---

## 📲 Comment importer sur Google Agenda

> **Astuce d'or :** Créez d'abord un agenda secondaire dédié (ex: *"Roulement 2027"*). Cela permet de lui assigner une couleur spécifique, de l'afficher/masquer d'un clic, et de pouvoir le supprimer ou le réimporter facilement sans toucher à votre calendrier principal.

1. Rendez-vous sur votre ordinateur sur [Google Agenda](https://calendar.google.com).
2. À gauche, à côté de **Autres agendas**, cliquez sur le **`+`** puis sur **Créer un agenda**.
3. Nommez-le par exemple **Roulement SNCF 2027** et cliquez sur **Créer l'agenda**.
4. Cliquez sur la roue dentée en haut à droite ⚙️ > **Paramètres**.
5. Dans le menu à gauche, cliquez sur **Importer et exporter** > **Importer**.
6. Cliquez sur **Sélectionner un fichier sur votre ordinateur** et choisissez le fichier `roulement_2027_travail.ics` (ou `roulement_2027_complet.ics`).
7. Dans le menu déroulant **Agenda**, sélectionnez **Roulement SNCF 2027** (celui que vous venez de créer).
8. Cliquez sur le bouton **Importer**.
9. Vos postes apparaissent instantanément et se synchronisent automatiquement sur votre téléphone Android / iPhone !
