# Solveur d'Équation de Schrödinger 🔬

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20+-green.svg)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.7+-yellow.svg)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

## 🇫🇷 Français

Cette application interactive résout l'équation de Schrödinger indépendante du temps et visualise les états propres et l'évolution temporelle des états quantiques pour divers potentiels en 1D et 2D.

![Capture d'écran de l'application](../test_colormap_registration.png)

## 📊 Exemples de Visualisation

### Visualisation 1D
![Exemple de visualisation 1D](../images/1d_example.png)
*Visualisation des états propres et du potentiel pour un oscillateur harmonique en 1D, montrant plusieurs niveaux d'énergie avec leurs fonctions d'onde correspondantes.*

### Visualisation 2D
![Exemple de visualisation 2D](../images/9888097c23b8e5c2824aec468539287b3be3600a0f74890234bf1e8a.png)
*Visualisation des états propres pour un puits infini en 2D, montrant des tracés de contour de la densité de probabilité pour différents niveaux d'énergie.*

### Évolution Temporelle
![Animation de l'évolution temporelle](../images/3ba05eaee105a4f7fee19dbd21bac133cc509da45857f0770930fb9c.gif)
*Animation d'un paquet d'onde gaussien évoluant dans un puits de potentiel, démontrant la dynamique quantique au fil du temps.*

### Tracé de Surface 3D
![Tracé de surface 3D](../images/e33246c98d78151748bf603b55ee3b883396913540876c53241adc4e.png)
*Tracé de surface 3D d'une fonction de potentiel 2D, montrant la forme de la surface d'énergie potentielle.*

### ✨ Fonctionnalités

- **Solveur complet** : Résout l'équation de Schrödinger indépendante du temps en 1D et 2D
- **Visualisation interactive** : Affiche les fonctions d'onde, les densités de probabilité et les niveaux d'énergie
- **Évolution temporelle** : Anime l'évolution des états quantiques dans le temps
- **Potentiels multiples** :
  - Puits infini
  - Barrière de potentiel
  - Oscillateur harmonique
  - Double puits (effet tunnel)
  - Potentiel de Morse (1D uniquement)
  - Puits circulaire (2D uniquement)
- **Interface conviviale** : Interface utilisateur basée sur Streamlit pour l'ajustement interactif des paramètres
- **Support multilingue** : Disponible en anglais, français et espagnol

### 🔧 Installation

```bash
# Cloner le dépôt
git clone https://github.com/Illuminatyon/SchrodingerEquationVisualiser.git
cd SchrodingerEquationVisualiser

# Créer un environnement virtuel
python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
# source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 📋 Prérequis

- Python 3.7+
- NumPy
- SciPy
- Matplotlib
- Streamlit

Consultez `requirements.txt` pour la liste complète des dépendances.

### 🚀 Utilisation

#### Interface Streamlit (Recommandée)

```bash
# Exécuter avec suppression des avertissements
python run_streamlit.py

# Ou directement avec Streamlit
streamlit run streamlit_app.py
```

#### Ligne de commande

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

### 📁 Structure du projet

- `schrodinger_solver/` - Package principal
  - `core.py` - Fonctions de base pour la résolution de l'équation
  - `potentials.py` - Implémentation des différents potentiels
  - `solver_1d.py` - Solveur pour l'équation en 1D
  - `solver_2d.py` - Solveur pour l'équation en 2D
  - `main.py` - Point d'entrée principal
- `streamlit_app.py` - Application Streamlit
- `run_streamlit.py` - Script d'encapsulation pour exécuter l'application Streamlit avec suppression des avertissements
- `custom_mpl_style.py` - Style Matplotlib personnalisé
- `requirements.txt` - Dépendances du projet

### 📚 Fondements théoriques

L'équation de Schrödinger indépendante du temps est une équation fondamentale en mécanique quantique qui décrit la fonction d'onde d'un système quantique :

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(\mathbf{r})\psi = E\psi$$

où :
- $\psi$ est la fonction d'onde
- $\hbar$ est la constante de Planck réduite
- $m$ est la masse de la particule
- $V(\mathbf{r})$ est l'énergie potentielle
- $E$ est la valeur propre d'énergie
- $\nabla^2$ est l'opérateur laplacien

En une dimension, l'équation se simplifie en :

$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi$$

Cette application utilise des méthodes numériques pour résoudre cette équation pour diverses fonctions potentielles et visualiser les états propres résultants.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](../LICENSE) pour plus de détails.

---

Créé avec ❤️ en utilisant Python et Streamlit