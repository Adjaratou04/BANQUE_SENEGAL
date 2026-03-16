# Analyse et Visualisation du Positionnement des Banques au Sénégal

> *"La data visualisation consiste à faire parler les données afin d'aider à prendre des décisions claires et éclairées."*

---

## Description du projet

Ce projet a pour objectif d'automatiser l'analyse du **positionnement des banques au Sénégal** à partir de données financières.

Il s'inscrit dans une démarche de **Data Engineering et Data Visualisation** permettant de collecter, structurer, nettoyer et visualiser des données issues de différentes sources.

Les données proviennent de deux sources principales :

* un **fichier Excel de base (BASE_SENEGAL2.xlsx)** contenant les données historiques des banques jusqu'en 2020
* les **rapports financiers publiés par la BCEAO**, permettant d'extraire les données des années suivantes

Le projet comprend plusieurs étapes :

* collecte des rapports financiers via **web scraping**
* extraction des tableaux présents dans les **PDF**
* fusion et nettoyage des datasets
* stockage des données dans **MongoDB**
* création d'un **dashboard interactif avec Dash**
* intégration dans une application **Flask multi-secteurs**

L'objectif final est de fournir un **outil interactif permettant d'analyser la performance et le positionnement des banques au Sénégal.**

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flask (Orchestrateur)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Bancaire   │  │  Energétique │  │   Assurance   │  │
│  │  (ce projet) │  │  (à venir)   │  │   (à venir)   │  │
│  └──────┬───────┘  └──────────────┘  └───────────────┘  │
│         │                                                 │
│  ┌──────▼──────────────────────────────────────────────┐ │
│  │                    MongoDB Atlas                     │ │
│  │        Collection : banques · users · rapports      │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Stack technique :**

| Composant | Technologie |
|-----------|-------------|
| Backend | Python 3.10+, Flask |
| Dashboard | Dash 2.x, Plotly |
| Base de données | MongoDB Atlas |
| Extraction PDF | pdfplumber, pytesseract (OCR) |
| Web Scraping | requests, BeautifulSoup4 |
| ML / Prévision | scikit-learn (régression linéaire) |
| Export | reportlab (PDF), openpyxl (Excel) |
| Déploiement | Render / Railway |

---

## Structure du projet

```
BANQUE_SENEGAL
│
├── .venv
│
├── dashboard
│   ├── assets
│   ├── app.py
│   ├── callbacks.py
│   └── layout.py
│
├── data
│   ├── cleaned_data
│   ├── extracted_tables
│   ├── raw_pdf
│   └── BASE_SENEGAL2.xlsx
│
├── database
│   ├── insert_mongo.py
│   └── mongo_connection.py
│
├── extraction
│   ├── merge_dataset.py
│   └── pdf_tables.py
│
├── flask_app
│   ├── templates
│   │   └── home.html
│   └── server.py
│
├── scraping
│   └── bceao_scraper.py
│
├── Procfile
├── runtime.txt
├── requirements.txt
└── README.md
```

---

##  Description des dossiers

### .venv
Environnement virtuel Python contenant les bibliothèques nécessaires au projet.

### dashboard
Contient l'application de **visualisation interactive développée avec Dash**.
* **app.py** : point d'entrée du dashboard
* **layout.py** : structure visuelle du dashboard (11 onglets, cartes KPI, graphiques)
* **callbacks.py** : interactions entre les graphiques, les filtres et les exports
* **assets/** : fichiers CSS ou ressources visuelles du dashboard

### data
Contient les données utilisées dans le projet.
* **BASE_SENEGAL2.xlsx** : dataset initial contenant les données des banques jusqu'en 2020
* **raw_pdf/** : rapports PDF téléchargés depuis le site de la BCEAO
* **extracted_tables/** : tableaux extraits des rapports PDF
* **cleaned_data/** : données nettoyées et prêtes pour l'analyse

### database
Contient les scripts permettant d'interagir avec **MongoDB**.
* **mongo_connection.py** : connexion à la base de données
* **insert_mongo.py** : insertion des données dans MongoDB

### extraction
Scripts permettant de transformer les données PDF en données exploitables.
* **pdf_tables.py** : extraction des tableaux financiers contenus dans les rapports PDF
* **merge_dataset.py** : fusion des données extraites avec le dataset initial

### scraping
Contient le script de **web scraping** permettant de récupérer automatiquement les rapports financiers depuis le site de la BCEAO.
* **bceao_scraper.py**

### flask_app
Application **Flask** permettant d'intégrer le dashboard dans une interface web multi-secteurs.
* **server.py** : serveur principal de l'application
* **templates/home.html** : page d'accueil de l'application

---

## Étapes pour lancer le projet

### 1- Créer un environnement virtuel

```bash
python -m venv .venv
```

### 2- Activer l'environnement virtuel

Windows :
```bash
.venv\Scripts\activate
```

Mac / Linux :
```bash
source .venv/bin/activate
```

### 3- Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4️4- Scraper les rapports BCEAO

```bash
python scraping/bceao_scraper.py
```

Les rapports PDF seront téléchargés dans `data/raw_pdf/`

### 5-Extraire les tableaux des PDF

```bash
python extraction/pdf_tables.py
```

Les tableaux extraits seront stockés dans `data/extracted_tables/`

### 6- Fusionner les datasets

```bash
python extraction/merge_dataset.py
```

Combine les données extraites avec le dataset initial.

### 7- Insérer les données dans MongoDB

```bash
python database/insert_mongo.py
```

### 8- Lancer l'application

```bash
python flask_app/server.py
```

L'application web sera accessible sur **http://localhost:8050**

---

##  Sources de données

| Source | Description | Méthode |
|--------|-------------|---------|
| `BASE_SENEGAL2.xlsx` | Données historiques jusqu'en 2020 | Import direct |
| [BCEAO — Rapports financiers](https://www.bceao.int/) | Rapports annuels des banques | Web scraping + OCR |
| Sièges sociaux | Coordonnées GPS des banques à Dakar | Base statique intégrée |

**Variables financières collectées :**

| Variable | Description |
|----------|-------------|
| `BILAN` | Total actif — taille financière de la banque |
| `EMPLOI` | Crédits, placements et investissements |
| `RESSOURCES` | Dépôts, emprunts et financements collectés |
| `FONDS.PROPRE` | Capital, réserves et fonds propres réglementaires |
| `RESULTAT.NET` | Bénéfice ou perte nette de l'exercice |
| `PRODUIT.NET.BANCAIRE` | Marge bancaire globale (PNB) |

---

##  Nettoyage et préparation des données

Les principales étapes de data engineering comprennent :

* gestion des valeurs manquantes
* suppression des doublons
* harmonisation des noms de colonnes
* conversion des types de données
* fusion des données provenant de différentes sources

L'objectif est d'obtenir un **dataset propre et cohérent** pour l'analyse.

---

##  Fonctionnalités du Dashboard

Le dashboard développé avec **Dash et Plotly** propose **11 onglets interactifs** :

| Onglet | Contenu |
|--------|---------|
| **KPI** | Indicateurs clés : bilan total, résultat net, fonds propres, PNB · Analyse automatique du secteur |
| **Bilan & Résultat** | Comparaison des tailles financières et des rentabilités par banque |
| **Évolution** | Trajectoire historique du bilan de chaque banque sur plusieurs années |
| **Classement** | Ranking par résultat net · Score global composite (bilan + résultat + fonds propres + ROA) |
| **Ratios** | ROA · Solvabilité avec norme BCEAO 8% · Emplois · Ressources |
| **Positionnement** | Cartographie concurrentielle taille × rentabilité · Matrice stratégique |
| **Parts de Marché** | Répartition du marché total par bilan (donut chart) |
| **Comparaison** | Tableau de bord multi-métriques : bilan vs résultat, ROA vs solvabilité, emplois vs ressources, score vs bilan |
| **Carte** | Géolocalisation réelle des sièges sociaux des banques à Dakar (OpenStreetMap) |
| **Prévision** | Projection à 3 ans par régression linéaire · Estimation indicative |
| **Synthèse** | Analyse narrative automatique et pédagogique de tous les indicateurs |

**Filtres disponibles :** Banque · Année

**Exports disponibles :**
* Rapport PDF personnalisé avec KPI, tableau des banques et analyse automatique
* Fichier Excel complet de toutes les données

**Interprétations automatiques** : chaque graphique est accompagné d'un texte pédagogique généré automatiquement expliquant ce que les données révèlent.

---

##  Objectif du projet

Créer un **outil interactif d'analyse du secteur bancaire sénégalais** permettant :

* d'étudier la performance financière des banques (bilan, résultat, ratios)
* d'analyser leur positionnement concurrentiel sur le marché
* de visualiser leur évolution dans le temps
* de faciliter la prise de décision basée sur les données

---

## Déploiement

### Render 

1. Connecter le dépôt GitHub sur [render.com](https://render.com)
2. **Build Command** : `pip install -r requirements.txt`
3. **Start Command** : `gunicorn app:server --bind 0.0.0.0:$PORT`
4. Ajouter les variables d'environnement : `MONGO_URI`, `SECRET_KEY`

### Variables d'environnement

| Variable | Description |
|----------|-------------|
| `MONGO_URI` | URI de connexion MongoDB Atlas |
| `MONGO_DB_NAME` | Nom de la base de données |
| `SECRET_KEY` | Clé secrète Flask |

---

##  Dépendances principales

```
dash · plotly · flask · pymongo · pandas · numpy
scikit-learn · pdfplumber · pytesseract · reportlab
requests · beautifulsoup4 · openpyxl · gunicorn
```

---

<div align="center">
  <sub>Plateforme d'Analyse Sectorielle · Secteur Bancaire Sénégalais · Données BCEAO</sub>
</div>
