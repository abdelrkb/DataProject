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
src/
├── components/      # Composants UI (sidebar, cartes)
├── pages/          # Pages Dash
├── services/       # Logique métier (graphs, histogrammes, cartes)
└── utils/          # Utilitaires (filtres, nettoyage données)
```

### Ajouter une statistique
1. Créer la méthode dans `src/services/graphs_service.py`
2. Ajouter à `stat_types` dans `src/components/sidebar_component.py`

### Principes
- Séparation des responsabilités (MVC-like)
- DataStore centralisé (chargement unique)
- Callbacks modulaires par component

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
