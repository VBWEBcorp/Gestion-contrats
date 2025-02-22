# Gestion de Contrats

Application web de gestion de contrats clients développée avec Flask.

## Fonctionnalités

- Gestion des clients actifs et archivés
- Suivi des contrats et dates d'échéance
- Calcul automatique du CA mensuel
- Statistiques et exports (CSV/Excel)
- Archivage automatique des contrats expirés
- Système de commentaires pour les clients archivés

## Technologies

- Backend : Flask (Python)
- Base de données : SQLite (dev) / PostgreSQL (prod)
- Frontend : Bootstrap 5, Chart.js
- Déploiement : Render

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/VBWEBcorp/Gestion-contrats.git
cd Gestion-contrats
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancer l'application :
```bash
python app.py
```

## Déploiement

L'application est configurée pour être déployée sur Render avec une base de données PostgreSQL.
