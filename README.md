# Solveur Quantitatif de l'Équation de Schrödinger

Ce projet implémente un solveur numérique pour l'équation de Schrödinger en 1D et 2D avec visualisation de la fonction d'onde.

## Fonctionnalités

- Résolution de l'équation de Schrödinger indépendante du temps en 1D et 2D
- Visualisation des fonctions d'onde et des densités de probabilité
- Animation de l'évolution temporelle des fonctions d'onde
- Support pour différents potentiels :
  - Puits infini
  - Barrière de potentiel
  - Oscillateur harmonique
  - Double puits (effet tunnel)
- Interface Streamlit pour ajuster les paramètres interactivement

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/schrodinger-solver.git
cd schrodinger-solver

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

### Ligne de commande

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

### Interface Streamlit

```bash
streamlit run streamlit_app.py
```

## Structure du projet

- `schrodinger_solver/` - Package principal
  - `core.py` - Fonctions de base pour la résolution de l'équation
  - `potentials.py` - Implémentation des différents potentiels
  - `solver_1d.py` - Solveur pour l'équation en 1D
  - `solver_2d.py` - Solveur pour l'équation en 2D
  - `visualization.py` - Fonctions de visualisation
  - `main.py` - Point d'entrée principal
- `streamlit_app.py` - Application Streamlit
- `examples/` - Exemples d'utilisation
- `tests/` - Tests unitaires

## Fondements théoriques

L'équation de Schrödinger indépendante du temps s'écrit :

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(x,y)\psi = E\psi$$

où :
- $\psi$ est la fonction d'onde
- $\hbar$ est la constante de Planck réduite
- $m$ est la masse de la particule
- $V(x,y)$ est le potentiel
- $E$ est l'énergie

## Licence

MIT