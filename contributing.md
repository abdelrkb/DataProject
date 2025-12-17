# Contribuer au projet

 **règles, conventions et bonnes pratiques**

Architecture **modulaire** :

- **Une seule source de vérité pour les données**
- **Séparation stricte** entre :
  - Données (DataStore / services)
  - Logique de Traitement des Données (services)
  - Interface Utilisateur (components)
  - Orchestration (pages)
- **Aucune Logique de Traitement des Données dans le front**
- **Aucune lecture de fichier dans les services**

## 🧠 Règles fondamentales (IMPORTANT)

### ❌ Ce qui est interdit
- Lire un CSV dans un component
- Faire du Pandas dans un component
- Faire du Dash dans un service
- Charger les données plusieurs fois
- Créer des instances globales de components

### ✅ Ce qui est obligatoire
- Utiliser `DataStore` pour accéder aux données
- Mettre toute de traitement des données dans les **services**
- Les components ne font que :
  - afficher
  - gérer les callbacks
- Les pages orchestrent les components

---
# Outils de qualité de code 

## Ruff

**Ruff** est un outil rapide de qualité de code Python.  
Il remplace notamment flake8, isort et black.

### Installation

```bash
pip install ruff
```
Ou via les dependecies 
```bash
pip install -r requirements-dev.txt
```

### Utilisation
```bash
ruff check .          # Analyse du code
ruff check . --fix    # Correction automatique
ruff format .         # Formatage du code
```

## pre-commit
**pre-commit**  exécute automatiquement des vérifications avant chaque commit Git afin d’éviter l’ajout de code incorrect.

### Installation

```bash
pip install pre-commit
```
Ou via les dependecies 
```bash
pip install -r requirements-dev.txt
```

### Activer pre-commit
```bash
pre-commit install
```

## Workflow recommandé
```bash
ruff check . --fix
ruff format .
git add .
git commit -m "feat: message commit"
```
