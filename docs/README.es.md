# Solucionador de la Ecuación de Schrödinger 🔬

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20+-green.svg)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.7+-yellow.svg)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

## 🇪🇸 Español

Esta aplicación interactiva resuelve la ecuación de Schrödinger independiente del tiempo y visualiza los autoestados y la evolución temporal de los estados cuánticos para varios potenciales en 1D y 2D.

![Captura de pantalla de la aplicación](../test_colormap_registration.png)

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
git clone https://github.com/Illuminatyon/SchrodingerEquationVisualiser.git
cd SchrodingerEquationVisualiser

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

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](../LICENSE) para más detalles.

---

Creado con ❤️ usando Python y Streamlit