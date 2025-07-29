# Schrödinger Equation Solver 🔬

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20+-green.svg)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.7+-yellow.svg)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [Français](#français) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

This interactive application solves the time-independent Schrödinger equation and visualizes the eigenstates and time evolution of quantum states for various potentials in 1D and 2D.

![Application Screenshot](test_colormap_registration.png)

### ✨ Features

- **Comprehensive Solver**: Solves the time-independent Schrödinger equation in 1D and 2D
- **Interactive Visualization**: Displays wave functions, probability densities, and energy levels
- **Time Evolution**: Animates quantum state evolution over time
- **Multiple Potentials**:
  - Infinite well
  - Potential barrier
  - Harmonic oscillator
  - Double well (tunneling effect)
  - Morse potential (1D only)
  - Circular well (2D only)
- **User-Friendly Interface**: Streamlit-based UI for interactive parameter adjustment
- **Multi-language Support**: Available in English, French, and Spanish

### 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/schrodinger-solver.git
cd schrodinger-solver

# Create a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 📋 Requirements

- Python 3.7+
- NumPy
- SciPy
- Matplotlib
- Streamlit

See `requirements.txt` for the complete list of dependencies.

### 🚀 Usage

#### Streamlit Interface (Recommended)

```bash
# Run with warning suppression
python run_streamlit.py

# Or directly with Streamlit
streamlit run streamlit_app.py
```

#### Command Line

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

### 📁 Project Structure

- `schrodinger_solver/` - Main package
  - `core.py` - Core functions for solving the equation
  - `potentials.py` - Implementation of different potentials
  - `solver_1d.py` - 1D equation solver
  - `solver_2d.py` - 2D equation solver
  - `main.py` - Main entry point
- `streamlit_app.py` - Streamlit application
- `run_streamlit.py` - Wrapper script to run the Streamlit app with suppressed warnings
- `custom_mpl_style.py` - Custom Matplotlib styling
- `requirements.txt` - Project dependencies

### 📚 Theoretical Background

The time-independent Schrödinger equation is a fundamental equation in quantum mechanics that describes the wave function of a quantum-mechanical system:

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(\mathbf{r})\psi = E\psi$$

where:
- $\psi$ is the wave function
- $\hbar$ is the reduced Planck constant
- $m$ is the particle mass
- $V(\mathbf{r})$ is the potential energy
- $E$ is the energy eigenvalue
- $\nabla^2$ is the Laplacian operator

In one dimension, the equation simplifies to:

$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi$$

This application uses numerical methods to solve this equation for various potential functions and visualize the resulting eigenstates.

---

<a name="français"></a>
## 🇫🇷 Français

Cette application interactive résout l'équation de Schrödinger indépendante du temps et visualise les états propres et l'évolution temporelle des états quantiques pour divers potentiels en 1D et 2D.

![Capture d'écran de l'application](test_colormap_registration.png)

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
git clone https://github.com/votre-utilisateur/schrodinger-solver.git
cd schrodinger-solver

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

---

<a name="español"></a>
## 🇪🇸 Español

Esta aplicación interactiva resuelve la ecuación de Schrödinger independiente del tiempo y visualiza los autoestados y la evolución temporal de los estados cuánticos para varios potenciales en 1D y 2D.

![Captura de pantalla de la aplicación](test_colormap_registration.png)

### ✨ Características

- **Solucionador completo**: Resuelve la ecuación de Schrödinger independiente del tiempo en 1D y 2D
- **Visualización interactiva**: Muestra funciones de onda, densidades de probabilidad y niveles de energía
- **Evolución temporal**: Anima la evolución de estados cuánticos a lo largo del tiempo
- **Múltiples potenciales**:
  - Pozo infinito
  - Barrera de potencial
  - Oscilador armónico
  - Doble pozo (efecto túnel)
  - Potencial de Morse (solo 1D)
  - Pozo circular (solo 2D)
- **Interfaz amigable**: Interfaz de usuario basada en Streamlit para ajuste interactivo de parámetros
- **Soporte multilingüe**: Disponible en inglés, francés y español

### 🔧 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/schrodinger-solver.git
cd schrodinger-solver

# Crear un entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
# source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 📋 Requisitos

- Python 3.7+
- NumPy
- SciPy
- Matplotlib
- Streamlit

Consulte `requirements.txt` para la lista completa de dependencias.

### 🚀 Uso

#### Interfaz Streamlit (Recomendado)

```bash
# Ejecutar con supresión de advertencias
python run_streamlit.py

# O directamente con Streamlit
streamlit run streamlit_app.py
```

#### Línea de comandos

```bash
python -m schrodinger_solver.main --dimension=1 --potential=harmonic --n_points=1000
```

### 📁 Estructura del proyecto

- `schrodinger_solver/` - Paquete principal
  - `core.py` - Funciones básicas para resolver la ecuación
  - `potentials.py` - Implementación de diferentes potenciales
  - `solver_1d.py` - Solucionador de ecuaciones 1D
  - `solver_2d.py` - Solucionador de ecuaciones 2D
  - `main.py` - Punto de entrada principal
- `streamlit_app.py` - Aplicación Streamlit
- `run_streamlit.py` - Script envoltorio para ejecutar la aplicación Streamlit con supresión de advertencias
- `custom_mpl_style.py` - Estilo personalizado de Matplotlib
- `requirements.txt` - Dependencias del proyecto

### 📚 Fundamentos teóricos

La ecuación de Schrödinger independiente del tiempo es una ecuación fundamental en la mecánica cuántica que describe la función de onda de un sistema cuántico:

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V(\mathbf{r})\psi = E\psi$$

donde:
- $\psi$ es la función de onda
- $\hbar$ es la constante de Planck reducida
- $m$ es la masa de la partícula
- $V(\mathbf{r})$ es la energía potencial
- $E$ es el valor propio de energía
- $\nabla^2$ es el operador laplaciano

En una dimensión, la ecuación se simplifica a:

$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi$$

Esta aplicación utiliza métodos numéricos para resolver esta ecuación para varias funciones potenciales y visualizar los autoestados resultantes.

---

## 📄 License | Licence | Licencia

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.

---

Created with ❤️ using Python and Streamlit | Créé avec ❤️ en utilisant Python et Streamlit | Creado con ❤️ usando Python y Streamlit