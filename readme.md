# Dashboard COVID-19 dans les hopitaux en France

Visualisation interactive des données COVID-19 en France avec cartes choroplèthes, graphiques temporels et filtres dynamiques.

![Python](https://img.shields.io/badge/python-3.13.7-blue)
![Dash](https://img.shields.io/badge/dash-3.2.0-green)
![Plotly](https://img.shields.io/badge/plotly-6.3.0-orange)

---

## Auteurs
- @abdelrkb : REKKAB Abdelnour
- @djambaxx : ZEROUAL Ilyes

---

## User Guide

### Prérequis
- Python 3.13.7
- pip

### Installation
```bash
git clone https://github.com/abdelrkb/DataProject
cd DataProject
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux
pip install -r requirements.txt
```

### Lancement
```bash
python main.py
```
Accessible sur **http://127.0.0.1:8050**

### Utilisation
**Interface :**
- Sidebar gauche : filtres géographiques, type de statistiques, graphiques
- Zone centrale : cartes interactives (France métropolitaine + DROM-COM)

**Filtres disponibles :**
- Niveau géographique : France entière / Région / Département
- Type de statistiques : Hospitalisations / Réanimations / Décès
- Période : DatePicker pour sélectionner les dates

---

## Data

### Source
Données de **Santé publique France** (1er avril 2020 au 30 juin 2023)
Source : [data.gouv.fr](https://www.data.gouv.fr/datasets/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19)

### Colonnes principales
| Colonne | Description |
|---------|-------------|
| `dep` | Code département |
| `date` | Date d'observation |
| `hosp` | Patients hospitalisés |
| `rea` | Patients en réanimation |
| `incid_hosp` | Nouvelles hospitalisations |
| `incid_rea` | Nouvelles entrées en réa |
| `incid_dchosp` | Nouveaux décès |

### GeoJSON
Contours géographiques : [france-geojson.gregoiredavid.fr](https://france-geojson.gregoiredavid.fr)

---

## Developer Guide

### Architecture
```
├── __init__.py
├── assets
│   └── global.css
├── config.py
├── contributing.md
├── data
│   ├── cleaned
│   │   └── covid_clean.csv
│   ├── geo
│   │   ├── departements.geojson
│   │   ├── guadeloupe.geojson
│   │   ├── guyane.geojson
│   │   ├── martinique.geojson
│   │   ├── mayotte.geojson
│   │   ├── regions.geojson
│   │   └── reunion.geojson
│   └── raw
│       └── covid_dataset.csv
├── images
├── main.py
├── pyproject.toml
├── readme.md
├── render.yaml
├── requirements-dev.txt
├── requirements.txt
└── src
    ├── __init__.py
    ├── components # Composants UI (sidebar, cartes)
    │   ├── __init__.py
    │   ├── base
    │   │   └── base_component.py
    │   ├── dashboard_map_component.py
    │   └── sidebar_component.py
    ├── pages # Pages Dash
    │   ├── __init__.py
    │   ├── base
    │   │   └── base_page.py
    │   └── home_page.py
    ├── services  # Logique métier (graphs, histogrammes, cartes)
    │   ├── base
    │   │   ├── base_service.py
    │   │   └── datastore.py
    │   ├── graphs_service.py
    │   ├── histogram_service.py
    │   ├── map_service.py
    │   ├── reference_service.py
    │   └── stats_service.py
    └── utils  # Utilitaires (filtres, nettoyage données)
        ├── __init__.py
        ├── clean_data.py
        ├── data_filter.py
        └── get_data.py
```

### Diagramme d'architecture Mermaid
<img width="754" height="724" alt="image" src="https://github.com/user-attachments/assets/10605e74-aeaf-4290-b4f4-a46ee757f612" />


### Diagramme des classes
<img width="1100" height="625" alt="image" src="https://github.com/user-attachments/assets/63c7a3ec-19c7-469d-a3b7-2e0711dae295" />

### Ajouter une statistique
1. Créer la méthode dans `src/services/graphs_service.py` ou ``src/services/histogramme_service.py`
2. Ajouter à `stat_types` dans `src/components/sidebar_component.py`
3. Créer la carte correspondante dans `map_service.py``

### Principes
- Séparation des responsabilités (MVC-like)
- DataStore centralisé (chargement unique)
- Callbacks modulaires par component


### Qualité de code

Le projet utilise **Ruff** pour garantir la qualité et la cohérence du code.

#### Installation des outils de développement
```bash
pip install -r requirements-dev.txt
```

#### Ruff - Linter et formateur

**Ruff** est un linter Python ultra-rapide qui remplace flake8, isort et black.

**Vérifier le code :**
```bash
ruff check .
```

**Corriger automatiquement :**
```bash
ruff check . --fix
```

**Formater le code :**
```bash
ruff format .
```

#### Pre-commit hooks

Le projet utilise **pre-commit** pour vérifier automatiquement le code avant chaque commit.

**Installer les hooks :**
```bash
pre-commit install
```

Les hooks s'exécuteront automatiquement à chaque `git commit` et bloqueront le commit si le code ne respecte pas les standards.

#### Configuration

La configuration de Ruff se trouve dans `pyproject.toml` :
- **Target** : Python 3.13
- **Line length** : 88 caractères (standard Black)
- **Rules** : Erreurs de syntaxe (E4, E7, E9) et erreurs Python (F)

#### CI/CD

Une GitHub Action (`/.github/workflows/ci.yml`) vérifie automatiquement le code sur chaque Pull Request vers `main`.

Voir le Contributing.MD pour plus d'informations sur la qualité de code.

---

## Analyse des données

**Evolution temporelle**
- 3 vagues principales entre 2020 et 2021
- Décroissance progressive grâce aux mesures sanitaires et vaccination

**Disparités régionales**
- Île-de-France, Auvergne-Rhône-Alpes et Hauts-de-France les plus touchées
- Corrélation avec la densité de population

**Taux de létalité**
- Forte baisse : 18-20% (première vague) → 2-5% (post-vaccination)
- Amélioration de la prise en charge

**Limites**
- Données hospitalières uniquement
- Période jusqu'à juin 2023

---

## Copyright

**Déclaration d'originalité**
Nous, REKKAB Abdelnour et ZEROUAL Ilyes, déclarons sur l'honneur que le code fourni a été produit par nous-même.

**Bibliothèques utilisées**
- Dash, Plotly, Folium, Pandas, GeoPandas (voir `requirements.txt`)
