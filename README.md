# Schrödinger Equation Solver | Solveur de l'Équation de Schrödinger | Solucionador de la Ecuación de Schrödinger

[English](#english) | [Français](#français) | [Español](#español)

<a name="english"></a>
## English

This project implements a numerical solver for the Schrödinger equation in 1D and 2D with wave function visualization.

### Features

- Solves the time-independent Schrödinger equation in 1D and 2D
- Visualizes wave functions and probability densities
- Animates time evolution of wave functions
- Supports various potentials:
  - Infinite well
  - Potential barrier
  - Harmonic oscillator
  - Double well (tunneling effect)
  - Morse potential (1D only)
  - Circular well (2D only)
- Streamlit interface for interactive parameter adjustment
- Multi-language support (English, French, Spanish)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/schrodinger-solver.git
cd schrodinger-solver

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Command Line

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

#### Streamlit Interface

```bash
python run_streamlit.py
```
or
```bash
streamlit run streamlit_app.py
```

### Project Structure

- `schrodinger_solver/` - Main package
  - `core.py` - Core functions for solving the equation
  - `potentials.py` - Implementation of different potentials
  - `solver_1d.py` - 1D equation solver
  - `solver_2d.py` - 2D equation solver
  - `main.py` - Main entry point
- `streamlit_app.py` - Streamlit application
- `run_streamlit.py` - Wrapper script to run the Streamlit app with suppressed warnings

### Theoretical Background

The time-independent Schrödinger equation is:

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(x,y)\psi = E\psi$$

where:
- $\psi$ is the wave function
- $\hbar$ is the reduced Planck constant
- $m$ is the particle mass
- $V(x,y)$ is the potential
- $E$ is the energy

<a name="français"></a>
## Français

Ce projet implémente un solveur numérique pour l'équation de Schrödinger en 1D et 2D avec visualisation de la fonction d'onde.

### Fonctionnalités

- Résolution de l'équation de Schrödinger indépendante du temps en 1D et 2D
- Visualisation des fonctions d'onde et des densités de probabilité
- Animation de l'évolution temporelle des fonctions d'onde
- Support pour différents potentiels :
  - Puits infini
  - Barrière de potentiel
  - Oscillateur harmonique
  - Double puits (effet tunnel)
  - Potentiel de Morse (1D uniquement)
  - Puits circulaire (2D uniquement)
- Interface Streamlit pour ajuster les paramètres interactivement
- Support multilingue (anglais, français, espagnol)

### Installation

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

### Utilisation

#### Ligne de commande

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

#### Interface Streamlit

```bash
python run_streamlit.py
```
ou
```bash
streamlit run streamlit_app.py
```

### Structure du projet

- `schrodinger_solver/` - Package principal
  - `core.py` - Fonctions de base pour la résolution de l'équation
  - `potentials.py` - Implémentation des différents potentiels
  - `solver_1d.py` - Solveur pour l'équation en 1D
  - `solver_2d.py` - Solveur pour l'équation en 2D
  - `main.py` - Point d'entrée principal
- `streamlit_app.py` - Application Streamlit
- `run_streamlit.py` - Script d'encapsulation pour exécuter l'application Streamlit avec suppression des avertissements

### Fondements théoriques

L'équation de Schrödinger indépendante du temps s'écrit :

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(x,y)\psi = E\psi$$

où :
- $\psi$ est la fonction d'onde
- $\hbar$ est la constante de Planck réduite
- $m$ est la masse de la particule
- $V(x,y)$ est le potentiel
- $E$ est l'énergie

<a name="español"></a>
## Español

Este proyecto implementa un solucionador numérico para la ecuación de Schrödinger en 1D y 2D con visualización de la función de onda.

### Características

- Resuelve la ecuación de Schrödinger independiente del tiempo en 1D y 2D
- Visualiza funciones de onda y densidades de probabilidad
- Anima la evolución temporal de las funciones de onda
- Soporta varios potenciales:
  - Pozo infinito
  - Barrera de potencial
  - Oscilador armónico
  - Doble pozo (efecto túnel)
  - Potencial de Morse (solo 1D)
  - Pozo circular (solo 2D)
- Interfaz Streamlit para ajuste interactivo de parámetros
- Soporte multilingüe (inglés, francés, español)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/schrodinger-solver.git
cd schrodinger-solver

# Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Uso

#### Línea de comandos

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

#### Interfaz Streamlit

```bash
python run_streamlit.py
```
o
```bash
streamlit run streamlit_app.py
```

### Estructura del proyecto

- `schrodinger_solver/` - Paquete principal
  - `core.py` - Funciones básicas para resolver la ecuación
  - `potentials.py` - Implementación de diferentes potenciales
  - `solver_1d.py` - Solucionador de ecuaciones 1D
  - `solver_2d.py` - Solucionador de ecuaciones 2D
  - `main.py` - Punto de entrada principal
- `streamlit_app.py` - Aplicación Streamlit
- `run_streamlit.py` - Script envoltorio para ejecutar la aplicación Streamlit con supresión de advertencias

### Fundamentos teóricos

La ecuación de Schrödinger independiente del tiempo es:

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(x,y)\psi = E\psi$$

donde:
- $\psi$ es la función de onda
- $\hbar$ es la constante de Planck reducida
- $m$ es la masa de la partícula
- $V(x,y)$ es el potencial
- $E$ es la energía

## License | Licence | Licencia

MIT