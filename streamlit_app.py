"""
Streamlit app for interactive visualization of the Schrödinger equation solutions.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import io
from PIL import Image

from schrodinger_solver import potentials
from schrodinger_solver.solver_1d import Schrodinger1D
from schrodinger_solver.solver_2d import Schrodinger2D

# Import custom Matplotlib styling
import custom_mpl_style

# Initialize custom Matplotlib theme
custom_mpl_style.set_mpl_theme()

# Set page configuration
st.set_page_config(
    page_title="Schrödinger Equation Solver",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define translations
translations = {
    "English": {
        "app_title": "Schrödinger Equation Solver",
        "app_subtitle": "Quantum mechanics visualization tool",
        "app_description": "This app solves the time-independent Schrödinger equation and visualizes the eigenstates and time evolution of quantum states for various potentials in 1D and 2D.",
        "equation_description": "The equation being solved is:",
        "where": "where:",
        "wave_function": "is the wave function",
        "planck_constant": "is the reduced Planck constant",
        "particle_mass": "is the particle mass",
        "potential": "is the potential",
        "energy": "is the energy",
        "parameters": "Parameters",
        "how_to_use": "How to use this app",
        "welcome": "Welcome to the Schrödinger Equation Solver!",
        "app_allows": "This app allows you to visualize quantum states for various potentials in 1D and 2D.",
        "select_dimension": "Select the dimension (1D or 2D)",
        "choose_potential": "Choose a potential from the dropdown",
        "adjust_domain": "Adjust the domain and grid resolution",
        "modify_parameters": "Modify potential-specific parameters",
        "enable_time_evolution": "Enable time evolution to see animations",
        "app_will_solve": "The app will solve the Schrödinger equation and display the eigenstates and energy levels.",
        "hover_info": "Hover over any parameter for additional information!",
        "physics_parameters": "Physics Parameters",
        "reduced_planck": "Reduced Planck Constant (ħ)",
        "reduced_planck_help": "Value of ħ in natural units. Default is 1.0.",
        "particle_mass_param": "Particle Mass",
        "particle_mass_help": "Mass of the particle in natural units. Default is 1.0.",
        "solver_options": "Solver Options",
        "boundary_conditions": "Boundary Conditions",
        "boundary_conditions_help": "'dirichlet': Wave function is zero at boundaries. 'periodic': Domain wraps around.",
        "eigenvalue_selection": "Eigenvalue Selection",
        "eigenvalue_selection_help": "'SM': Smallest eigenvalues in magnitude. 'SA': Smallest eigenvalues algebraically.",
        "domain": "Domain",
        "grid_resolution": "Grid Resolution",
        "number_eigenstates": "Number of Eigenstates",
        "visualization_options": "Visualization Options",
        "figure_width": "Figure Width",
        "figure_height": "Figure Height",
        "colormap": "Colormap",
        "colormap_help": "Colormap for 2D plots",
        "plot_type": "Plot Type for Eigenfunctions",
        "plot_type_help": "Type of plot for 2D eigenfunctions",
        "potential_parameters": "Potential Parameters",
        "time_evolution": "Time Evolution",
        "animate_time_evolution": "Animate Time Evolution",
        "maximum_time": "Maximum Time",
        "number_time_steps": "Number of Time Steps",
        "animation_options": "Animation Options",
        "frame_interval": "Frame Interval (ms)",
        "frame_interval_help": "Time between frames in milliseconds",
        "animation_colormap": "Animation Colormap",
        "animation_colormap_help": "Colormap for animation",
        "initial_wave_packet": "Initial Wave Packet",
        "packet_center": "Packet Center",
        "packet_width": "Packet Width",
        "initial_momentum": "Initial Momentum",
        "energy_eigenvalues": "Energy Eigenvalues",
        "state": "State",
        "energy": "Energy",
        "eigenstates_potential": "Eigenstates and Potential",
        "time_evolution_title": "Time Evolution",
        "time_evolution_caption": "Time Evolution of Quantum State",
        "potential": "Potential",
        "about_project": "About this Project",
        "app_description_about": "This app is a numerical solver for the Schrödinger equation in 1D and 2D, featuring an enhanced UI with animations and LaTeX styling.",
        "core_technology": "Core Technology",
        "ui_features": "UI Features",
        "parameter_guide": "Parameter Guide",
        "app_provides": "The app provides extensive customization options:",
        "physics_parameters_guide": "Physics Parameters",
        "solver_options_guide": "Solver Options",
        "domain_visualization": "Domain & Visualization",
        "animation_potentials": "Animation & Potentials",
        "ui_customization_guide": "UI Customization Guide",
        "app_features_custom_ui": "This application features a custom UI with several enhancements:",
        "theme_customization": "Theme Customization",
        "custom_styling": "Custom Styling",
        "plot_styling": "Plot Styling",
        "created_with": "Created with ❤️ using Streamlit and Python",
        
        # New translations for the theory section
        "theory_section": "Quantum Theory",
        "theory_tab_definition": "Definition",
        "theory_tab_properties": "Properties",
        "theory_tab_examples": "Examples",
        "theory_tab_history": "History",
        "theory_tab_interpretation": "Interpretation",
        
        # Definition tab content
        "definition_title": "The Schrödinger Equation",
        "definition_intro": "The Schrödinger equation is a partial differential equation that governs the wave function of a non-relativistic quantum-mechanical system. Its discovery was a significant landmark in the development of quantum mechanics.",
        "time_dependent_title": "Time-Dependent Equation",
        "time_dependent_desc": "The most general form is the time-dependent Schrödinger equation, which gives a description of a system evolving with time:",
        "time_independent_title": "Time-Independent Equation",
        "time_independent_desc": "The time-dependent Schrödinger equation predicts that wave functions can form standing waves, called stationary states. These states are particularly important as their individual study later simplifies the task of solving the time-dependent Schrödinger equation for any state. Stationary states can also be described by a simpler form of the Schrödinger equation, the time-independent Schrödinger equation:",
        
        # Properties tab content
        "properties_title": "Properties of the Schrödinger Equation",
        "linearity_title": "Linearity",
        "linearity_desc": "The Schrödinger equation is a linear differential equation, meaning that if two state vectors are solutions, then so is any linear combination of the two state vectors. This property allows superpositions of quantum states to be solutions of the Schrödinger equation.",
        "unitarity_title": "Unitarity",
        "unitarity_desc": "Time evolution under the Schrödinger equation is unitary, which means it preserves the inner product between vectors in the Hilbert space. This property ensures that the total probability remains conserved over time.",
        "probability_current_title": "Probability Current",
        "probability_current_desc": "The Schrödinger equation is consistent with local probability conservation. The continuity equation for probability in non-relativistic quantum mechanics relates the time rate of change of probability density to the divergence of the probability current.",
        
        # Examples tab content
        "examples_title": "Examples of Quantum Systems",
        "particle_in_box_title": "Particle in a Box",
        "particle_in_box_desc": "The particle in a one-dimensional potential energy box is the most mathematically simple example where restraints lead to the quantization of energy levels. The box is defined as having zero potential energy inside a certain region and infinite potential energy outside.",
        "harmonic_oscillator_title": "Harmonic Oscillator",
        "harmonic_oscillator_desc": "The quantum harmonic oscillator is one of the most important model systems in quantum mechanics. It can be used to describe approximately a wide variety of other systems, including vibrating atoms, molecules, and atoms or ions in lattices.",
        "hydrogen_atom_title": "Hydrogen Atom",
        "hydrogen_atom_desc": "The Schrödinger equation for a hydrogen atom can be solved by separation of variables. This is the only atom for which the Schrödinger equation has been solved exactly. Multi-electron atoms require approximate methods.",
        
        # History tab content
        "history_title": "History of the Schrödinger Equation",
        "history_intro": "Following Max Planck's quantization of light and Louis de Broglie's hypothesis that particles have wave-like properties, Erwin Schrödinger developed his equation in 1925 and published it in 1926.",
        "history_development": "Schrödinger was guided by William Rowan Hamilton's analogy between mechanics and optics. Initially, he attempted to find a relativistic wave equation but found that the relativistic corrections disagreed with experimental data. He then published his non-relativistic version, which correctly reproduced the energy levels of hydrogen.",
        "history_interpretation": "Schrödinger initially tried to interpret the real part of the wave function as a charge density, but this approach was unsuccessful. Shortly after, Max Born successfully interpreted the modulus squared of the wave function as a probability density.",
        
        # Interpretation tab content
        "interpretation_title": "Interpretation of Quantum Mechanics",
        "copenhagen_title": "Copenhagen Interpretation",
        "copenhagen_desc": "In the views often grouped together as the Copenhagen interpretation, a system's wave function is a collection of statistical information about that system. While the time-evolution process represented by the Schrödinger equation is continuous and deterministic, wave functions can also change discontinuously during a measurement.",
        "many_worlds_title": "Many-Worlds Interpretation",
        "many_worlds_desc": "The many-worlds interpretation, formulated by Hugh Everett in 1956, holds that all the possibilities described by quantum theory simultaneously occur in a multiverse composed of mostly independent parallel universes. This interpretation removes the axiom of wave function collapse, leaving only continuous evolution under the Schrödinger equation.",
        "bohm_title": "Bohmian Mechanics",
        "bohm_desc": "Bohmian mechanics reformulates quantum mechanics to make it deterministic, at the price of adding a force due to a 'quantum potential'. It attributes to each physical system not only a wave function but in addition a real position that evolves deterministically under a nonlocal guiding equation."
    },
    "Français": {
        "app_title": "Solveur de l'Équation de Schrödinger",
        "app_subtitle": "Outil de visualisation de mécanique quantique",
        "app_description": "Cette application résout l'équation de Schrödinger indépendante du temps et visualise les états propres et l'évolution temporelle des états quantiques pour divers potentiels en 1D et 2D.",
        "equation_description": "L'équation résolue est :",
        "where": "où :",
        "wave_function": "est la fonction d'onde",
        "planck_constant": "est la constante de Planck réduite",
        "particle_mass": "est la masse de la particule",
        "potential": "est le potentiel",
        "energy": "est l'énergie",
        "parameters": "Paramètres",
        "how_to_use": "Comment utiliser cette application",
        "welcome": "Bienvenue sur le Solveur de l'Équation de Schrödinger !",
        "app_allows": "Cette application vous permet de visualiser les états quantiques pour divers potentiels en 1D et 2D.",
        "select_dimension": "Sélectionnez la dimension (1D ou 2D)",
        "choose_potential": "Choisissez un potentiel dans la liste déroulante",
        "adjust_domain": "Ajustez le domaine et la résolution de la grille",
        "modify_parameters": "Modifiez les paramètres spécifiques au potentiel",
        "enable_time_evolution": "Activez l'évolution temporelle pour voir les animations",
        "app_will_solve": "L'application résoudra l'équation de Schrödinger et affichera les états propres et les niveaux d'énergie.",
        "hover_info": "Survolez n'importe quel paramètre pour des informations supplémentaires !",
        "physics_parameters": "Paramètres Physiques",
        "reduced_planck": "Constante de Planck Réduite (ħ)",
        "reduced_planck_help": "Valeur de ħ en unités naturelles. La valeur par défaut est 1.0.",
        "particle_mass_param": "Masse de la Particule",
        "particle_mass_help": "Masse de la particule en unités naturelles. La valeur par défaut est 1.0.",
        "solver_options": "Options du Solveur",
        "boundary_conditions": "Conditions aux Limites",
        "boundary_conditions_help": "'dirichlet': La fonction d'onde est nulle aux limites. 'periodic': Le domaine s'enroule sur lui-même.",
        "eigenvalue_selection": "Sélection des Valeurs Propres",
        "eigenvalue_selection_help": "'SM': Valeurs propres les plus petites en magnitude. 'SA': Valeurs propres les plus petites algébriquement.",
        "domain": "Domaine",
        "grid_resolution": "Résolution de la Grille",
        "number_eigenstates": "Nombre d'États Propres",
        "visualization_options": "Options de Visualisation",
        "figure_width": "Largeur de la Figure",
        "figure_height": "Hauteur de la Figure",
        "colormap": "Carte de Couleurs",
        "colormap_help": "Carte de couleurs pour les graphiques 2D",
        "plot_type": "Type de Graphique pour les Fonctions Propres",
        "plot_type_help": "Type de graphique pour les fonctions propres 2D",
        "potential_parameters": "Paramètres du Potentiel",
        "time_evolution": "Évolution Temporelle",
        "animate_time_evolution": "Animer l'Évolution Temporelle",
        "maximum_time": "Temps Maximum",
        "number_time_steps": "Nombre de Pas de Temps",
        "animation_options": "Options d'Animation",
        "frame_interval": "Intervalle entre les Images (ms)",
        "frame_interval_help": "Temps entre les images en millisecondes",
        "animation_colormap": "Carte de Couleurs pour l'Animation",
        "animation_colormap_help": "Carte de couleurs pour l'animation",
        "initial_wave_packet": "Paquet d'Onde Initial",
        "packet_center": "Centre du Paquet",
        "packet_width": "Largeur du Paquet",
        "initial_momentum": "Impulsion Initiale",
        "energy_eigenvalues": "Valeurs Propres d'Énergie",
        "state": "État",
        "energy": "Énergie",
        "eigenstates_potential": "États Propres et Potentiel",
        "time_evolution_title": "Évolution Temporelle",
        "time_evolution_caption": "Évolution Temporelle de l'État Quantique",
        "potential": "Potentiel",
        "about_project": "À Propos de ce Projet",
        "app_description_about": "Cette application est un solveur numérique pour l'équation de Schrödinger en 1D et 2D, avec une interface utilisateur améliorée avec des animations et un style LaTeX.",
        "core_technology": "Technologie de Base",
        "ui_features": "Fonctionnalités de l'Interface",
        "parameter_guide": "Guide des Paramètres",
        "app_provides": "L'application offre de nombreuses options de personnalisation :",
        "physics_parameters_guide": "Paramètres Physiques",
        "solver_options_guide": "Options du Solveur",
        "domain_visualization": "Domaine & Visualisation",
        "animation_potentials": "Animation & Potentiels",
        "ui_customization_guide": "Guide de Personnalisation de l'Interface",
        "app_features_custom_ui": "Cette application dispose d'une interface utilisateur personnalisée avec plusieurs améliorations :",
        "theme_customization": "Personnalisation du Thème",
        "custom_styling": "Style Personnalisé",
        "plot_styling": "Style des Graphiques",
        "created_with": "Créé avec ❤️ en utilisant Streamlit et Python",
        
        # New translations for the theory section
        "theory_section": "Théorie Quantique",
        "theory_tab_definition": "Définition",
        "theory_tab_properties": "Propriétés",
        "theory_tab_examples": "Exemples",
        "theory_tab_history": "Histoire",
        "theory_tab_interpretation": "Interprétation",
        
        # Definition tab content
        "definition_title": "L'Équation de Schrödinger",
        "definition_intro": "L'équation de Schrödinger est une équation aux dérivées partielles qui régit la fonction d'onde d'un système quantique non relativiste. Sa découverte a été une étape importante dans le développement de la mécanique quantique.",
        "time_dependent_title": "Équation Dépendante du Temps",
        "time_dependent_desc": "La forme la plus générale est l'équation de Schrödinger dépendante du temps, qui donne une description d'un système évoluant avec le temps :",
        "time_independent_title": "Équation Indépendante du Temps",
        "time_independent_desc": "L'équation de Schrödinger dépendante du temps prédit que les fonctions d'onde peuvent former des ondes stationnaires, appelées états stationnaires. Ces états sont particulièrement importants car leur étude individuelle simplifie la tâche de résolution de l'équation de Schrödinger dépendante du temps pour n'importe quel état. Les états stationnaires peuvent également être décrits par une forme plus simple de l'équation de Schrödinger, l'équation de Schrödinger indépendante du temps :",
        
        # Properties tab content
        "properties_title": "Propriétés de l'Équation de Schrödinger",
        "linearity_title": "Linéarité",
        "linearity_desc": "L'équation de Schrödinger est une équation différentielle linéaire, ce qui signifie que si deux vecteurs d'état sont des solutions, alors toute combinaison linéaire des deux vecteurs d'état est également une solution. Cette propriété permet aux superpositions d'états quantiques d'être des solutions de l'équation de Schrödinger.",
        "unitarity_title": "Unitarité",
        "unitarity_desc": "L'évolution temporelle sous l'équation de Schrödinger est unitaire, ce qui signifie qu'elle préserve le produit scalaire entre les vecteurs dans l'espace de Hilbert. Cette propriété garantit que la probabilité totale reste conservée au fil du temps.",
        "probability_current_title": "Courant de Probabilité",
        "probability_current_desc": "L'équation de Schrödinger est cohérente avec la conservation locale de la probabilité. L'équation de continuité pour la probabilité en mécanique quantique non relativiste relie le taux de variation temporelle de la densité de probabilité à la divergence du courant de probabilité.",
        
        # Examples tab content
        "examples_title": "Exemples de Systèmes Quantiques",
        "particle_in_box_title": "Particule dans une Boîte",
        "particle_in_box_desc": "La particule dans une boîte d'énergie potentielle unidimensionnelle est l'exemple mathématiquement le plus simple où les contraintes conduisent à la quantification des niveaux d'énergie. La boîte est définie comme ayant une énergie potentielle nulle à l'intérieur d'une certaine région et une énergie potentielle infinie à l'extérieur.",
        "harmonic_oscillator_title": "Oscillateur Harmonique",
        "harmonic_oscillator_desc": "L'oscillateur harmonique quantique est l'un des systèmes modèles les plus importants en mécanique quantique. Il peut être utilisé pour décrire approximativement une grande variété d'autres systèmes, y compris les atomes vibrants, les molécules et les atomes ou ions dans les réseaux.",
        "hydrogen_atom_title": "Atome d'Hydrogène",
        "hydrogen_atom_desc": "L'équation de Schrödinger pour un atome d'hydrogène peut être résolue par séparation des variables. C'est le seul atome pour lequel l'équation de Schrödinger a été résolue exactement. Les atomes multi-électroniques nécessitent des méthodes approximatives.",
        
        # History tab content
        "history_title": "Histoire de l'Équation de Schrödinger",
        "history_intro": "Suite à la quantification de la lumière par Max Planck et à l'hypothèse de Louis de Broglie selon laquelle les particules ont des propriétés ondulatoires, Erwin Schrödinger a développé son équation en 1925 et l'a publiée en 1926.",
        "history_development": "Schrödinger a été guidé par l'analogie de William Rowan Hamilton entre la mécanique et l'optique. Initialement, il a tenté de trouver une équation d'onde relativiste mais a constaté que les corrections relativistes ne correspondaient pas aux données expérimentales. Il a ensuite publié sa version non relativiste, qui reproduisait correctement les niveaux d'énergie de l'hydrogène.",
        "history_interpretation": "Schrödinger a d'abord essayé d'interpréter la partie réelle de la fonction d'onde comme une densité de charge, mais cette approche n'a pas abouti. Peu après, Max Born a interprété avec succès le module carré de la fonction d'onde comme une densité de probabilité.",
        
        # Interpretation tab content
        "interpretation_title": "Interprétation de la Mécanique Quantique",
        "copenhagen_title": "Interprétation de Copenhague",
        "copenhagen_desc": "Dans les vues souvent regroupées sous le nom d'interprétation de Copenhague, la fonction d'onde d'un système est une collection d'informations statistiques sur ce système. Bien que le processus d'évolution temporelle représenté par l'équation de Schrödinger soit continu et déterministe, les fonctions d'onde peuvent également changer de manière discontinue lors d'une mesure.",
        "many_worlds_title": "Interprétation des Mondes Multiples",
        "many_worlds_desc": "L'interprétation des mondes multiples, formulée par Hugh Everett en 1956, soutient que toutes les possibilités décrites par la théorie quantique se produisent simultanément dans un multivers composé d'univers parallèles majoritairement indépendants. Cette interprétation supprime l'axiome de l'effondrement de la fonction d'onde, ne laissant que l'évolution continue sous l'équation de Schrödinger.",
        "bohm_title": "Mécanique Bohmienne",
        "bohm_desc": "La mécanique bohmienne reformule la mécanique quantique pour la rendre déterministe, au prix de l'ajout d'une force due à un 'potentiel quantique'. Elle attribue à chaque système physique non seulement une fonction d'onde mais en plus une position réelle qui évolue de manière déterministe sous une équation directrice non locale."
    },
    "Español": {
        "app_title": "Solucionador de la Ecuación de Schrödinger",
        "app_subtitle": "Herramienta de visualización de mecánica cuántica",
        "app_description": "Esta aplicación resuelve la ecuación de Schrödinger independiente del tiempo y visualiza los autoestados y la evolución temporal de los estados cuánticos para varios potenciales en 1D y 2D.",
        "equation_description": "La ecuación que se resuelve es:",
        "where": "donde:",
        "wave_function": "es la función de onda",
        "planck_constant": "es la constante de Planck reducida",
        "particle_mass": "es la masa de la partícula",
        "potential": "es el potencial",
        "energy": "es la energía",
        "parameters": "Parámetros",
        "how_to_use": "Cómo usar esta aplicación",
        "welcome": "¡Bienvenido al Solucionador de la Ecuación de Schrödinger!",
        "app_allows": "Esta aplicación te permite visualizar estados cuánticos para varios potenciales en 1D y 2D.",
        "select_dimension": "Selecciona la dimensión (1D o 2D)",
        "choose_potential": "Elige un potencial del menú desplegable",
        "adjust_domain": "Ajusta el dominio y la resolución de la cuadrícula",
        "modify_parameters": "Modifica los parámetros específicos del potencial",
        "enable_time_evolution": "Habilita la evolución temporal para ver animaciones",
        "app_will_solve": "La aplicación resolverá la ecuación de Schrödinger y mostrará los autoestados y niveles de energía.",
        "hover_info": "¡Pasa el cursor sobre cualquier parámetro para obtener información adicional!",
        "physics_parameters": "Parámetros Físicos",
        "reduced_planck": "Constante de Planck Reducida (ħ)",
        "reduced_planck_help": "Valor de ħ en unidades naturales. El valor predeterminado es 1.0.",
        "particle_mass_param": "Masa de la Partícula",
        "particle_mass_help": "Masa de la partícula en unidades naturales. El valor predeterminado es 1.0.",
        "solver_options": "Opciones del Solucionador",
        "boundary_conditions": "Condiciones de Contorno",
        "boundary_conditions_help": "'dirichlet': La función de onda es cero en los límites. 'periodic': El dominio se envuelve.",
        "eigenvalue_selection": "Selección de Autovalores",
        "eigenvalue_selection_help": "'SM': Autovalores más pequeños en magnitud. 'SA': Autovalores más pequeños algebraicamente.",
        "domain": "Dominio",
        "grid_resolution": "Resolución de la Cuadrícula",
        "number_eigenstates": "Número de Autoestados",
        "visualization_options": "Opciones de Visualización",
        "figure_width": "Ancho de la Figura",
        "figure_height": "Altura de la Figura",
        "colormap": "Mapa de Colores",
        "colormap_help": "Mapa de colores para gráficos 2D",
        "plot_type": "Tipo de Gráfico para Autofunciones",
        "plot_type_help": "Tipo de gráfico para autofunciones 2D",
        "potential_parameters": "Parámetros del Potencial",
        "time_evolution": "Evolución Temporal",
        "animate_time_evolution": "Animar Evolución Temporal",
        "maximum_time": "Tiempo Máximo",
        "number_time_steps": "Número de Pasos de Tiempo",
        "animation_options": "Opciones de Animación",
        "frame_interval": "Intervalo entre Fotogramas (ms)",
        "frame_interval_help": "Tiempo entre fotogramas en milisegundos",
        "animation_colormap": "Mapa de Colores para Animación",
        "animation_colormap_help": "Mapa de colores para la animación",
        "initial_wave_packet": "Paquete de Ondas Inicial",
        "packet_center": "Centro del Paquete",
        "packet_width": "Ancho del Paquete",
        "initial_momentum": "Momento Inicial",
        "energy_eigenvalues": "Autovalores de Energía",
        "state": "Estado",
        "energy": "Energía",
        "eigenstates_potential": "Autoestados y Potencial",
        "time_evolution_title": "Evolución Temporal",
        "time_evolution_caption": "Evolución Temporal del Estado Cuántico",
        "potential": "Potencial",
        "about_project": "Acerca de este Proyecto",
        "app_description_about": "Esta aplicación es un solucionador numérico para la ecuación de Schrödinger en 1D y 2D, con una interfaz de usuario mejorada con animaciones y estilo LaTeX.",
        "core_technology": "Tecnología Principal",
        "ui_features": "Características de la Interfaz",
        "parameter_guide": "Guía de Parámetros",
        "app_provides": "La aplicación proporciona amplias opciones de personalización:",
        "physics_parameters_guide": "Parámetros Físicos",
        "solver_options_guide": "Opciones del Solucionador",
        "domain_visualization": "Dominio y Visualización",
        "animation_potentials": "Animación y Potenciales",
        "ui_customization_guide": "Guía de Personalización de la Interfaz",
        "app_features_custom_ui": "Esta aplicación cuenta con una interfaz de usuario personalizada con varias mejoras:",
        "theme_customization": "Personalización del Tema",
        "custom_styling": "Estilo Personalizado",
        "plot_styling": "Estilo de Gráficos",
        "created_with": "Creado con ❤️ usando Streamlit y Python",
        
        # New translations for the theory section
        "theory_section": "Teoría Cuántica",
        "theory_tab_definition": "Definición",
        "theory_tab_properties": "Propiedades",
        "theory_tab_examples": "Ejemplos",
        "theory_tab_history": "Historia",
        "theory_tab_interpretation": "Interpretación",
        
        # Definition tab content
        "definition_title": "La Ecuación de Schrödinger",
        "definition_intro": "La ecuación de Schrödinger es una ecuación diferencial parcial que gobierna la función de onda de un sistema cuántico no relativista. Su descubrimiento fue un hito significativo en el desarrollo de la mecánica cuántica.",
        "time_dependent_title": "Ecuación Dependiente del Tiempo",
        "time_dependent_desc": "La forma más general es la ecuación de Schrödinger dependiente del tiempo, que proporciona una descripción de un sistema que evoluciona con el tiempo:",
        "time_independent_title": "Ecuación Independiente del Tiempo",
        "time_independent_desc": "La ecuación de Schrödinger dependiente del tiempo predice que las funciones de onda pueden formar ondas estacionarias, llamadas estados estacionarios. Estos estados son particularmente importantes ya que su estudio individual simplifica la tarea de resolver la ecuación de Schrödinger dependiente del tiempo para cualquier estado. Los estados estacionarios también pueden describirse mediante una forma más simple de la ecuación de Schrödinger, la ecuación de Schrödinger independiente del tiempo:",
        
        # Properties tab content
        "properties_title": "Propiedades de la Ecuación de Schrödinger",
        "linearity_title": "Linealidad",
        "linearity_desc": "La ecuación de Schrödinger es una ecuación diferencial lineal, lo que significa que si dos vectores de estado son soluciones, entonces cualquier combinación lineal de los dos vectores de estado también es una solución. Esta propiedad permite que las superposiciones de estados cuánticos sean soluciones de la ecuación de Schrödinger.",
        "unitarity_title": "Unitariedad",
        "unitarity_desc": "La evolución temporal bajo la ecuación de Schrödinger es unitaria, lo que significa que preserva el producto interno entre vectores en el espacio de Hilbert. Esta propiedad asegura que la probabilidad total se conserve a lo largo del tiempo.",
        "probability_current_title": "Corriente de Probabilidad",
        "probability_current_desc": "La ecuación de Schrödinger es consistente con la conservación local de la probabilidad. La ecuación de continuidad para la probabilidad en la mecánica cuántica no relativista relaciona la tasa de cambio temporal de la densidad de probabilidad con la divergencia de la corriente de probabilidad.",
        
        # Examples tab content
        "examples_title": "Ejemplos de Sistemas Cuánticos",
        "particle_in_box_title": "Partícula en una Caja",
        "particle_in_box_desc": "La partícula en una caja de energía potencial unidimensional es el ejemplo matemáticamente más simple donde las restricciones conducen a la cuantización de los niveles de energía. La caja se define como con energía potencial cero dentro de una región determinada y energía potencial infinita fuera.",
        "harmonic_oscillator_title": "Oscilador Armónico",
        "harmonic_oscillator_desc": "El oscilador armónico cuántico es uno de los sistemas modelo más importantes en mecánica cuántica. Puede utilizarse para describir aproximadamente una amplia variedad de otros sistemas, incluyendo átomos vibrantes, moléculas y átomos o iones en redes.",
        "hydrogen_atom_title": "Átomo de Hidrógeno",
        "hydrogen_atom_desc": "La ecuación de Schrödinger para un átomo de hidrógeno puede resolverse mediante separación de variables. Este es el único átomo para el cual la ecuación de Schrödinger ha sido resuelta exactamente. Los átomos multielectrónicos requieren métodos aproximados.",
        
        # History tab content
        "history_title": "Historia de la Ecuación de Schrödinger",
        "history_intro": "Tras la cuantización de la luz por Max Planck y la hipótesis de Louis de Broglie de que las partículas tienen propiedades ondulatorias, Erwin Schrödinger desarrolló su ecuación en 1925 y la publicó en 1926.",
        "history_development": "Schrödinger fue guiado por la analogía de William Rowan Hamilton entre la mecánica y la óptica. Inicialmente, intentó encontrar una ecuación de onda relativista pero descubrió que las correcciones relativistas no coincidían con los datos experimentales. Luego publicó su versión no relativista, que reproducía correctamente los niveles de energía del hidrógeno.",
        "history_interpretation": "Schrödinger inicialmente intentó interpretar la parte real de la función de onda como una densidad de carga, pero este enfoque no tuvo éxito. Poco después, Max Born interpretó con éxito el módulo cuadrado de la función de onda como una densidad de probabilidad.",
        
        # Interpretation tab content
        "interpretation_title": "Interpretación de la Mecánica Cuántica",
        "copenhagen_title": "Interpretación de Copenhague",
        "copenhagen_desc": "En las visiones a menudo agrupadas como la interpretación de Copenhague, la función de onda de un sistema es una colección de información estadística sobre ese sistema. Mientras que el proceso de evolución temporal representado por la ecuación de Schrödinger es continuo y determinista, las funciones de onda también pueden cambiar de manera discontinua durante una medición.",
        "many_worlds_title": "Interpretación de Muchos Mundos",
        "many_worlds_desc": "La interpretación de muchos mundos, formulada por Hugh Everett en 1956, sostiene que todas las posibilidades descritas por la teoría cuántica ocurren simultáneamente en un multiverso compuesto por universos paralelos mayormente independientes. Esta interpretación elimina el axioma del colapso de la función de onda, dejando solo la evolución continua bajo la ecuación de Schrödinger.",
        "bohm_title": "Mecánica Bohmiana",
        "bohm_desc": "La mecánica bohmiana reformula la mecánica cuántica para hacerla determinista, a costa de añadir una fuerza debida a un 'potencial cuántico'. Atribuye a cada sistema físico no solo una función de onda sino además una posición real que evoluciona determinísticamente bajo una ecuación guía no local."
    }
}

# Add language selector to the sidebar
language = st.sidebar.selectbox(
    "Language | Langue | Idioma",
    ["English", "Français", "Español"],
    index=0,
    key="language_selector_1"
)

# Get translations for the selected language
t = translations[language]

# Custom CSS with Computer Modern font and animations
st.markdown("""
<style>
    /* Import Computer Modern font with multiple sources for better compatibility */
    @import url('https://cdn.jsdelivr.net/npm/computer-modern-font@1.0.0/index.css');
    @import url('https://cdn.jsdelivr.net/npm/@fontsource/computer-modern/index.css');
    
    /* Apply font to all text with multiple fallbacks */
    html, body, [class*="css"] {
        font-family: 'Computer Modern Serif', 'CMU Serif', 'Times New Roman', Times, serif !important;
    }
    
    /* Style headers with multiple fallbacks */
    h1, h2, h3, h4 {
        font-family: 'Computer Modern Serif', 'CMU Serif', 'Times New Roman', Times, serif !important;
        color: #F5F5F5 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    
    /* Main title styling - gradient text */
    h1 {
        background: linear-gradient(45deg, #00E5FF, #00796B);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 6s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar styling - dark background with gradient */
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, #1A237E 0%, #121212 100%) !important;
        background-color: #121212 !important;
    }
    
    /* Button animations */
    button {
        transition: all 0.3s ease;
    }
    
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Slider animations */
    .stSlider {
        transition: all 0.3s ease;
    }
    
    .stSlider:hover {
        transform: scale(1.02);
    }
    
    /* Card-like sections */
    .element-container {
        background-color: rgba(26, 35, 126, 0.2);  /* Deep blue with transparency */
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0, 229, 255, 0.2);  /* Cyan glow */
        border: 1px solid rgba(0, 121, 107, 0.3);  /* Teal border */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .element-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 229, 255, 0.4);  /* Brighter cyan glow on hover */
        border: 1px solid rgba(0, 121, 107, 0.6);  /* Brighter teal border on hover */
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Computer Modern Serif', 'CMU Serif', 'Times New Roman', Times, serif !important;
        border-collapse: collapse;
        margin: 20px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);  /* Cyan glow */
        background-color: rgba(18, 18, 18, 0.7);  /* Dark background */
    }
    
    .dataframe thead th {
        background-color: #1A237E;  /* Deep blue */
        color: #F5F5F5;  /* Light text */
        font-weight: bold;
        text-align: left;
        padding: 12px 15px;
        border-bottom: 2px solid #00796B;  /* Teal border */
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid rgba(0, 121, 107, 0.3);  /* Teal border with transparency */
        transition: background-color 0.3s;
    }
    
    .dataframe tbody tr:nth-of-type(even) {
        background-color: rgba(26, 35, 126, 0.2);  /* Deep blue with transparency */
    }
    
    .dataframe tbody tr:last-of-type {
        border-bottom: 2px solid #00796B;  /* Teal border */
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(123, 31, 162, 0.3);  /* Purple with transparency on hover */
    }
    
    /* Pulsing animation for computation indicators */
    .stSpinner {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Improve LaTeX rendering */
    .katex {
        font-size: 1.1em !important;
        line-height: 1.5 !important;
        text-align: center !important;
        margin: 10px auto !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
    }
    
    /* Ensure LaTeX equations are centered and have proper spacing */
    .katex-display {
        margin: 1.2em 0 !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        padding: 5px !important;
    }
    
    /* Make sure LaTeX symbols are properly sized */
    .katex-html {
        font-size: 1.1em !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #121212;  /* Dark background */
        border-radius: 10px;
        border: 1px solid rgba(0, 121, 107, 0.2);  /* Subtle teal border */
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #1A237E, #00796B);  /* Gradient from deep blue to teal */
        border-radius: 10px;
        box-shadow: 0 0 5px rgba(0, 229, 255, 0.3);  /* Subtle cyan glow */
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #00796B, #00E5FF);  /* Gradient from teal to cyan on hover */
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.5);  /* Enhanced cyan glow on hover */
    }
</style>
""", unsafe_allow_html=True)

# Custom header with logo and title
app_title = t["app_title"]
app_subtitle = t["app_subtitle"]

st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 20px; background: #121212; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,229,255,0.3); border: 1px solid #00796B;">
    <div style="font-size: 42px; margin-right: 20px; animation: pulse 2s infinite;">🔬</div>
    <div>
        <h1 style="margin: 0; background: linear-gradient(45deg, #00E5FF, #00796B); background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradient 6s ease infinite;">{app_title}</h1>
        <p style="margin: 0; font-style: italic; color: #F5F5F5;">{app_subtitle}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Description with simple border
st.markdown("""
<div style="border: 2px solid #00796B; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: rgba(26, 35, 126, 0.2); box-shadow: 0 0 15px rgba(0, 229, 255, 0.2); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; right: 0; width: 100px; height: 100px; background: radial-gradient(circle, rgba(0,229,255,0.2) 0%, rgba(26,35,126,0) 70%); border-radius: 50%; transform: translate(30%, -30%);"></div>
    <p style="color: #F5F5F5; position: relative; z-index: 1;">This app solves the time-independent Schrödinger equation and visualizes the eigenstates
    and time evolution of quantum states for various potentials in 1D and 2D.</p>
    <div style="position: absolute; bottom: 0; left: 0; width: 100px; height: 100px; background: radial-gradient(circle, rgba(123,31,162,0.2) 0%, rgba(26,35,126,0) 70%); border-radius: 50%; transform: translate(-30%, 30%);"></div>
</div>
""", unsafe_allow_html=True)

# Use Streamlit's native LaTeX support for the equation
st.write(t["equation_description"])

# Display the equation formula separately, bold and centered
st.markdown('<div style="text-align: center; font-weight: bold;">', unsafe_allow_html=True)
st.latex(r"-\frac{\hbar^2}{2m}\nabla^2\psi + V(\mathbf{r})\psi = E\psi")
st.markdown('</div>', unsafe_allow_html=True)

# Group the explanation text together
st.markdown("""
**""" + t["where"] + """:**
- $\psi$ """ + t["wave_function"] + """
- $\hbar$ """ + t["planck_constant"] + """
- $m$ """ + t["particle_mass"] + """
- $V(\mathbf{r})$ """ + t["potential"] + """
- $E$ """ + t["energy"] + """
""")

# Add Theory Section with tabs
st.markdown(f"""
<div style="border: 2px solid #00796B; border-radius: 10px; padding: 20px; margin: 30px 0; background-color: rgba(26, 35, 126, 0.2); box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);">
    <h2 style="color: #00E5FF; text-align: center; margin-bottom: 20px; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{t["theory_section"]}</h2>
</div>
""", unsafe_allow_html=True)

# Create tabs for different aspects of the theory
theory_tabs = st.tabs([
    t["theory_tab_definition"], 
    t["theory_tab_properties"], 
    t["theory_tab_examples"], 
    t["theory_tab_history"], 
    t["theory_tab_interpretation"]
])

# Definition Tab
with theory_tabs[0]:
    st.markdown(f"## {t['definition_title']}")
    st.markdown(t["definition_intro"])
    
    # Time-dependent equation
    st.markdown(f"### {t['time_dependent_title']}")
    st.markdown(t["time_dependent_desc"])
    st.latex(r"i\hbar\frac{d}{dt}|\Psi(t)\rangle = \hat{H}|\Psi(t)\rangle")
    
    # Time-independent equation
    st.markdown(f"### {t['time_independent_title']}")
    st.markdown(t["time_independent_desc"])
    st.latex(r"\hat{H}|\Psi\rangle = E|\Psi\rangle")

# Properties Tab
with theory_tabs[1]:
    st.markdown(f"## {t['properties_title']}")
    
    # Linearity
    st.markdown(f"### {t['linearity_title']}")
    st.markdown(t["linearity_desc"])
    st.latex(r"|\psi\rangle = a|\psi_1\rangle + b|\psi_2\rangle")
    
    # Unitarity
    st.markdown(f"### {t['unitarity_title']}")
    st.markdown(t["unitarity_desc"])
    st.latex(r"|\Psi(t)\rangle = e^{-i\hat{H}t/\hbar}|\Psi(0)\rangle")
    
    # Probability Current
    st.markdown(f"### {t['probability_current_title']}")
    st.markdown(t["probability_current_desc"])
    st.latex(r"\frac{\partial}{\partial t}\rho(\mathbf{r},t) + \nabla \cdot \mathbf{j} = 0")
    st.latex(r"\mathbf{j} = \frac{\hbar}{m}\text{Im}(\psi^*\nabla\psi)")

# Examples Tab
with theory_tabs[2]:
    st.markdown(f"## {t['examples_title']}")
    
    # Particle in a Box
    st.markdown(f"### {t['particle_in_box_title']}")
    st.markdown(t["particle_in_box_desc"])
    st.latex(r"E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}")
    
    # Harmonic Oscillator
    st.markdown(f"### {t['harmonic_oscillator_title']}")
    st.markdown(t["harmonic_oscillator_desc"])
    st.latex(r"E_n = \left(n+\frac{1}{2}\right)\hbar\omega")
    
    # Hydrogen Atom
    st.markdown(f"### {t['hydrogen_atom_title']}")
    st.markdown(t["hydrogen_atom_desc"])
    st.latex(r"E_n = -\frac{m_e e^4}{32\pi^2\varepsilon_0^2\hbar^2}\frac{1}{n^2} = -\frac{13.6\text{ eV}}{n^2}")

# History Tab
with theory_tabs[3]:
    st.markdown(f"## {t['history_title']}")
    
    # Add an image of Schrödinger
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Erwin_Schr%C3%B6dinger_%281933%29.jpg/330px-Erwin_Schr%C3%B6dinger_%281933%29.jpg" 
             alt="Erwin Schrödinger" 
             style="width: 200px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
    </div>
    <p style="text-align: center; font-style: italic; margin-bottom: 20px;">Erwin Schrödinger (1887-1961)</p>
    """, unsafe_allow_html=True)
    
    st.markdown(t["history_intro"])
    st.markdown(t["history_development"])
    st.markdown(t["history_interpretation"])

# Interpretation Tab
with theory_tabs[4]:
    st.markdown(f"## {t['interpretation_title']}")
    
    # Copenhagen Interpretation
    st.markdown(f"### {t['copenhagen_title']}")
    st.markdown(t["copenhagen_desc"])
    
    # Many-Worlds Interpretation
    st.markdown(f"### {t['many_worlds_title']}")
    st.markdown(t["many_worlds_desc"])
    
    # Bohmian Mechanics
    st.markdown(f"### {t['bohm_title']}")
    st.markdown(t["bohm_desc"])

# Use translations from the first language selector
# (The redundant second language selector has been removed)

# Sidebar for parameters with simple styling
st.sidebar.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(26,35,126,0.7) 0%, rgba(18,18,18,0.9) 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #00796B; box-shadow: 0 0 10px rgba(0,229,255,0.2);">
    <h2 style="margin: 0; background: linear-gradient(45deg, #00E5FF, #FFA000); background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradient 6s ease infinite; text-align: center; font-family: 'Computer Modern Serif', 'CMU Serif', 'Times New Roman', Times, serif;">
        {t["parameters"]}
    </h2>
</div>
""", unsafe_allow_html=True)

# Add a help button at the top of the sidebar
with st.sidebar.expander(f"ℹ️ {t['how_to_use']}", expanded=False):
    st.markdown(f"""
    <div style="font-family: 'Computer Modern Serif', 'CMU Serif', 'Times New Roman', Times, serif; color: #F5F5F5; background: rgba(26,35,126,0.3); padding: 15px; border-radius: 8px; border-left: 3px solid #00796B; box-shadow: 0 0 10px rgba(0,229,255,0.1);">
        <p><strong style="color: #00E5FF;">{t['welcome']}</strong></p>
        <p>{t['app_allows']}</p>
        <ol style="color: #F5F5F5;">
            <li><span style="color: #FFA000;">{t['select_dimension']}</span></li>
            <li><span style="color: #FFA000;">{t['choose_potential']}</span></li>
            <li><span style="color: #FFA000;">{t['adjust_domain']}</span></li>
            <li><span style="color: #FFA000;">{t['modify_parameters']}</span></li>
            <li><span style="color: #FFA000;">{t['enable_time_evolution']}</span></li>
        </ol>
        <p>{t['app_will_solve']}</p>
        <p><em style="color: #00E5FF;">{t['hover_info']}</em></p>
    </div>
    """, unsafe_allow_html=True)

# Dimension selection
dimension = st.sidebar.radio("Dimension", [1, 2], index=0)

# Physics parameters
st.sidebar.subheader(t["physics_parameters"])
hbar = st.sidebar.slider(t["reduced_planck"], 0.1, 2.0, 1.0, 
                         help=t["reduced_planck_help"])
mass = st.sidebar.slider(t["particle_mass_param"], 0.1, 10.0, 1.0,
                         help=t["particle_mass_help"])

# Solver options
st.sidebar.subheader(t["solver_options"])
boundary = st.sidebar.selectbox(t["boundary_conditions"], 
                               ["dirichlet", "periodic"], 
                               index=0,
                               help=t["boundary_conditions_help"])
which_eigenvalues = st.sidebar.selectbox(t["eigenvalue_selection"], 
                                        ["SM", "SA"], 
                                        index=0,
                                        help=t["eigenvalue_selection_help"])

# Potential selection
if dimension == 1:
    potential_options = [
        "Infinite Well", 
        "Harmonic Oscillator", 
        "Barrier", 
        "Double Well", 
        "Morse"
    ]
    potential_functions = {
        "Infinite Well": potentials.infinite_well_1d,
        "Harmonic Oscillator": potentials.harmonic_oscillator_1d,
        "Barrier": potentials.barrier_potential_1d,
        "Double Well": potentials.double_well_1d,
        "Morse": potentials.morse_potential_1d
    }
else:  # dimension == 2
    potential_options = [
        "Infinite Well", 
        "Harmonic Oscillator", 
        "Circular Well", 
        "Double Well"
    ]
    potential_functions = {
        "Infinite Well": potentials.infinite_well_2d,
        "Harmonic Oscillator": potentials.harmonic_oscillator_2d,
        "Circular Well": potentials.circular_well_2d,
        "Double Well": potentials.double_well_2d
    }

potential_name = st.sidebar.selectbox("Potential", potential_options)
potential_func = potential_functions[potential_name]

# Domain parameters
st.sidebar.subheader("Domain")
domain_min = st.sidebar.slider("X Domain Minimum", -10.0, 0.0, -5.0)
domain_max = st.sidebar.slider("X Domain Maximum", 0.0, 10.0, 5.0)

# For 2D, allow separate Y domain settings
if dimension == 2:
    use_same_domain = st.sidebar.checkbox("Use same domain for Y axis", value=True)
    if use_same_domain:
        domain_min_y = domain_min
        domain_max_y = domain_max
    else:
        domain_min_y = st.sidebar.slider("Y Domain Minimum", -10.0, 0.0, -5.0)
        domain_max_y = st.sidebar.slider("Y Domain Maximum", 0.0, 10.0, 5.0)

# Grid resolution
if dimension == 1:
    n_points = st.sidebar.slider("Number of Grid Points", 100, 2000, 1000)
else:  # dimension == 2
    use_same_grid = st.sidebar.checkbox("Use same grid resolution for both axes", value=True)
    if use_same_grid:
        n_points = st.sidebar.slider("Number of Grid Points per Dimension", 50, 200, 100)
        nx = ny = n_points
    else:
        nx = st.sidebar.slider("Number of X Grid Points", 50, 200, 100)
        ny = st.sidebar.slider("Number of Y Grid Points", 50, 200, 100)

# Number of eigenstates
n_states = st.sidebar.slider("Number of Eigenstates", 1, 10, 6)

# Visualization options
st.sidebar.subheader("Visualization Options")
figsize_width = st.sidebar.slider("Figure Width", 6, 20, 12)
figsize_height = st.sidebar.slider("Figure Height", 4, 16, 8)
figsize = (figsize_width, figsize_height)

if dimension == 2:
    colormap = st.sidebar.selectbox("Colormap", 
                                   ["viridis", "plasma", "inferno", "magma", "cividis", 
                                    "Blues", "Greens", "Reds", "Purples", "jet"],
                                   index=0,
                                   help="Colormap for 2D plots")
    plot_type = st.sidebar.selectbox("Plot Type for Eigenfunctions", 
                                    ["contourf", "contour", "surface"],
                                    index=0,
                                    help="Type of plot for 2D eigenfunctions")

# Potential-specific parameters
st.sidebar.subheader("Potential Parameters")

if potential_name == "Infinite Well":
    # Common parameters for both 1D and 2D
    depth = st.sidebar.slider("Well Depth", 0.0, 10.0, 0.0, 
                             help="Potential value inside the well")
    wall_value = st.sidebar.slider("Wall Value", 1e3, 1e7, 1e6, 
                                  format="%.1e", 
                                  help="Potential value outside the well (should be very large)")
    
    if dimension == 1:
        width = st.sidebar.slider("Width", 0.1, domain_max - domain_min, 5.0)
        offset = st.sidebar.slider("Offset", domain_min, domain_max, 0.0)
        potential_params = {"width": width, "offset": offset, "depth": depth, "wall_value": wall_value}
    else:  # dimension == 2
        width_x = st.sidebar.slider("Width X", 0.1, domain_max - domain_min, 5.0)
        width_y = st.sidebar.slider("Width Y", 0.1, domain_max - domain_min, 5.0)
        offset_x = st.sidebar.slider("Offset X", domain_min, domain_max, 0.0)
        offset_y = st.sidebar.slider("Offset Y", domain_min, domain_max, 0.0)
        potential_params = {
            "width_x": width_x, "width_y": width_y, 
            "offset_x": offset_x, "offset_y": offset_y, 
            "depth": depth, "wall_value": wall_value
        }

elif potential_name == "Harmonic Oscillator":
    if dimension == 1:
        k = st.sidebar.slider("Spring Constant", 0.1, 10.0, 1.0)
        center = st.sidebar.slider("Center", domain_min, domain_max, 0.0)
        potential_params = {"k": k, "center": center, "mass": 1.0}
    else:  # dimension == 2
        k_x = st.sidebar.slider("Spring Constant X", 0.1, 10.0, 1.0)
        k_y = st.sidebar.slider("Spring Constant Y", 0.1, 10.0, 1.0)
        center_x = st.sidebar.slider("Center X", domain_min, domain_max, 0.0)
        center_y = st.sidebar.slider("Center Y", domain_min, domain_max, 0.0)
        potential_params = {
            "k_x": k_x, "k_y": k_y, 
            "center_x": center_x, "center_y": center_y, 
            "mass": 1.0
        }

elif potential_name == "Barrier":
    height = st.sidebar.slider("Height", 0.1, 10.0, 5.0)
    width = st.sidebar.slider("Width", 0.01, 2.0, 0.5)
    position = st.sidebar.slider("Position", domain_min, domain_max, 0.0)
    potential_params = {"height": height, "width": width, "position": position}

elif potential_name == "Double Well":
    if dimension == 1:
        height = st.sidebar.slider("Base Height", 0.0, 5.0, 1.0)
        width = st.sidebar.slider("Total Width", 1.0, domain_max - domain_min, 4.0)
        barrier_width = st.sidebar.slider("Barrier Width", 0.1, width/2, 0.5)
        barrier_height = st.sidebar.slider("Barrier Height", height, 10.0, 5.0)
        potential_params = {
            "height": height, "width": width, 
            "barrier_width": barrier_width, "barrier_height": barrier_height
        }
    else:  # dimension == 2
        height = st.sidebar.slider("Base Height", 0.0, 5.0, 1.0)
        width = st.sidebar.slider("Total Width", 1.0, domain_max - domain_min, 4.0)
        barrier_width = st.sidebar.slider("Barrier Width", 0.1, width/2, 0.5)
        barrier_height = st.sidebar.slider("Barrier Height", height, 10.0, 5.0)
        direction = st.sidebar.radio("Direction", ["x", "y"], index=0)
        potential_params = {
            "height": height, "width": width, 
            "barrier_width": barrier_width, "barrier_height": barrier_height,
            "direction": direction
        }

elif potential_name == "Morse":
    D = st.sidebar.slider("Dissociation Energy", 1.0, 20.0, 10.0)
    a = st.sidebar.slider("Width Parameter", 0.1, 5.0, 1.0)
    r_e = st.sidebar.slider("Equilibrium Position", domain_min, domain_max, 0.0)
    potential_params = {"D": D, "a": a, "r_e": r_e}

elif potential_name == "Circular Well":
    radius = st.sidebar.slider("Radius", 0.1, (domain_max - domain_min)/2, 2.0)
    center_x = st.sidebar.slider("Center X", domain_min, domain_max, 0.0)
    center_y = st.sidebar.slider("Center Y", domain_min, domain_max, 0.0)
    depth = st.sidebar.slider("Well Depth", 0.0, 10.0, 0.0, 
                             help="Potential value inside the well")
    wall_value = st.sidebar.slider("Wall Value", 1e3, 1e7, 1e6, 
                                  format="%.1e", 
                                  help="Potential value outside the well (should be very large)")
    potential_params = {
        "radius": radius, "center_x": center_x, "center_y": center_y, 
        "depth": depth, "wall_value": wall_value
    }

# Time evolution parameters
st.sidebar.subheader(t["time_evolution"])
animate = st.sidebar.checkbox(t["animate_time_evolution"], value=False)

if animate:
    t_max = st.sidebar.slider(t["maximum_time"], 1.0, 50.0, 10.0)
    n_steps = st.sidebar.slider(t["number_time_steps"], 50, 200, 100)
    
    # Animation options
    st.sidebar.subheader(t["animation_options"])
    animation_interval = st.sidebar.slider(t["frame_interval"], 10, 500, 50,
                                         help=t["frame_interval_help"])
    if dimension == 2:
        animation_cmap = st.sidebar.selectbox(t["animation_colormap"], 
                                            ["viridis", "plasma", "inferno", "magma", "cividis", 
                                             "Blues", "Greens", "Reds", "Purples", "jet"],
                                            index=0,
                                            help=t["animation_colormap_help"])
    
    # Wave packet parameters
    st.sidebar.subheader(t["initial_wave_packet"])
    if dimension == 1:
        packet_center = st.sidebar.slider(
            t["packet_center"], domain_min, domain_max, (domain_min + domain_max)/2
        )
        packet_width = st.sidebar.slider(
            t["packet_width"], 0.1, (domain_max - domain_min)/5, (domain_max - domain_min)/10
        )
        packet_k0 = st.sidebar.slider(t["initial_momentum"], -5.0, 5.0, 2.0)
    else:  # dimension == 2
        packet_center_x = st.sidebar.slider(
            f"{t['packet_center']} X", domain_min, domain_max, (domain_min + domain_max)/2
        )
        packet_center_y = st.sidebar.slider(
            f"{t['packet_center']} Y", domain_min, domain_max, (domain_min + domain_max)/2
        )
        packet_width_x = st.sidebar.slider(
            f"{t['packet_width']} X", 0.1, (domain_max - domain_min)/5, (domain_max - domain_min)/10
        )
        packet_width_y = st.sidebar.slider(
            f"{t['packet_width']} Y", 0.1, (domain_max - domain_min)/5, (domain_max - domain_min)/10
        )
        packet_k0_x = st.sidebar.slider(f"{t['initial_momentum']} X", -5.0, 5.0, 2.0)
        packet_k0_y = st.sidebar.slider(f"{t['initial_momentum']} Y", -5.0, 5.0, 0.0)


# Function to create a Gaussian wave packet
def create_gaussian_wave_packet(x_grid, center, width, k0):
    """Create a Gaussian wave packet."""
    return np.exp(-0.5 * ((x_grid - center) / width)**2) * np.exp(1j * k0 * x_grid)


def create_gaussian_wave_packet_2d(x_grid, y_grid, center_x, center_y, width_x, width_y, k0_x, k0_y):
    """Create a 2D Gaussian wave packet."""
    return (np.exp(-0.5 * ((x_grid - center_x) / width_x)**2 - 0.5 * ((y_grid - center_y) / width_y)**2) 
            * np.exp(1j * (k0_x * x_grid + k0_y * y_grid)))


# Function to convert matplotlib animation to a GIF for Streamlit
def anim_to_gif(anim, n_frames=None):
    """Convert a matplotlib animation to a GIF.
    
    Parameters
    ----------
    anim : matplotlib.animation.FuncAnimation
        The animation to convert.
    n_frames : int, optional
        Number of frames in the animation. If None, will try to determine automatically.
    """
    # Use provided n_frames if available
    if n_frames is None:
        # Try to determine the number of frames from the animation
        # For FuncAnimation, we can access the frames from the _frames attribute
        # or use the number of frames passed to the animation (n_steps)
        if hasattr(anim, '_frames'):
            n_frames = len(anim._frames)
        elif hasattr(anim, '_save_seq'):
            # For newer versions of matplotlib, use _save_seq
            n_frames = len(anim._save_seq)
        elif hasattr(anim, '_iter_frames'):
            # Try to get frames from _iter_frames method if available
            n_frames = len(list(anim._iter_frames()))
        else:
            # Try to get n_frames from the animation's frames parameter
            try:
                if hasattr(anim, '_args') and len(anim._args) > 0:
                    frames_arg = anim._args[0]
                    if isinstance(frames_arg, int):
                        n_frames = frames_arg
                    elif hasattr(frames_arg, '__len__'):
                        n_frames = len(frames_arg)
                    else:
                        # Fallback to a safe default
                        n_frames = 50
                else:
                    # Fallback to a safe default - try to get frames count from the animation object
                    try:
                        n_frames = anim._fig.axes[0].texts[0].get_text().count('\n') + 1
                    except (AttributeError, IndexError):
                        # If all else fails, assume a reasonable default
                        n_frames = 50  # Default to 50 frames
            except (AttributeError, IndexError, TypeError):
                # If all else fails, assume a reasonable default
                n_frames = 50  # Default to 50 frames
    
    frames = []
    for i in range(n_frames):
        anim._fig.set_animated(True)
        anim._draw_frame(i)
        canvas = anim._fig.canvas
        canvas.draw()
        buf = io.BytesIO()
        canvas.print_rgba(buf)
        width, height = canvas.get_width_height()
        buf.seek(0)
        img_array = np.frombuffer(buf.getvalue(), dtype=np.uint8).reshape(height, width, 4)
        frames.append(Image.fromarray(img_array))
    
    # Save frames as GIF
    gif_buf = io.BytesIO()
    frames[0].save(
        gif_buf, format='GIF', save_all=True, append_images=frames[1:], 
        duration=anim._interval, loop=0
    )
    gif_buf.seek(0)
    return gif_buf


# Main content
if dimension == 1:
    # Create 1D solver
    solver = Schrodinger1D(
        x_min=domain_min,
        x_max=domain_max,
        n_points=n_points,
        potential_func=potential_func,
        hbar=hbar,
        mass=mass,
        boundary=boundary,
        **potential_params
    )
    
    # Solve for eigenstates
    with st.spinner("Solving the Schrödinger equation..."):
        eigenvalues, eigenvectors = solver.solve(n_eigenstates=n_states, which=which_eigenvalues)
    
    # Display eigenvalues
    st.subheader(t["energy_eigenvalues"])
    eigenvalues_df = {t["state"]: list(range(n_states)), t["energy"]: eigenvalues}
    st.dataframe(eigenvalues_df)
    
    # Plot eigenstates
    st.subheader(t["eigenstates_potential"])
    fig = solver.plot_eigenstates(n_states=n_states, figsize=figsize)
    st.pyplot(fig)
    
    # Animate time evolution if requested
    if animate:
        st.subheader(t["time_evolution_title"])
        
        # Create initial wave packet
        initial_state = create_gaussian_wave_packet(
            solver.x_grid, packet_center, packet_width, packet_k0
        )
        
        # Normalize the initial state
        norm = np.sqrt(np.trapz(np.abs(initial_state)**2, x=solver.x_grid))
        initial_state = initial_state / norm
        
        with st.spinner("Creating animation..."):
            # Create the animation
            anim = solver.animate_time_evolution(
                initial_state, 
                t_max, 
                n_steps, 
                interval=animation_interval,
                figsize=figsize
            )
            
            # Convert to GIF and display
            gif_buf = anim_to_gif(anim, n_frames=n_steps)
            st.image(gif_buf, caption=t["time_evolution_caption"])

else:  # dimension == 2
    # Create 2D solver
    solver = Schrodinger2D(
        x_min=domain_min,
        x_max=domain_max,
        y_min=domain_min_y,
        y_max=domain_max_y,
        nx=nx,
        ny=ny,
        potential_func=potential_func,
        hbar=hbar,
        mass=mass,
        boundary=boundary,
        **potential_params
    )
    
    # Solve for eigenstates
    with st.spinner("Solving the Schrödinger equation..."):
        eigenvalues, eigenvectors = solver.solve(n_eigenstates=n_states, which=which_eigenvalues)
    
    # Display eigenvalues
    st.subheader(t["energy_eigenvalues"])
    eigenvalues_df = {t["state"]: list(range(n_states)), t["energy"]: eigenvalues}
    st.dataframe(eigenvalues_df)
    
    # Plot potential
    st.subheader(t["potential"])
    fig_potential = plt.figure(figsize=figsize)
    ax = fig_potential.add_subplot(111, projection='3d')
    solver.plot_potential(ax=ax, cmap=colormap)
    st.pyplot(fig_potential)
    
    # Plot eigenstates
    st.subheader(t["eigenstates_potential"])
    fig_eigenstates = solver.plot_eigenstates_grid(n_states=n_states, figsize=figsize, cmap=colormap, plot_type=plot_type)
    st.pyplot(fig_eigenstates)
    
    # Animate time evolution if requested
    if animate:
        st.subheader(t["time_evolution_title"])
        
        # Create initial wave packet
        initial_state = create_gaussian_wave_packet_2d(
            solver.x_grid, solver.y_grid, 
            packet_center_x, packet_center_y, 
            packet_width_x, packet_width_y, 
            packet_k0_x, packet_k0_y
        )
        
        # Normalize the initial state
        norm = np.sqrt(np.sum(np.abs(initial_state)**2) * solver.dx * solver.dy)
        initial_state = initial_state / norm
        
        with st.spinner("Creating animation..."):
            # Create the animation
            anim = solver.animate_time_evolution(
                initial_state, 
                t_max, 
                n_steps, 
                interval=animation_interval,
                figsize=figsize,
                cmap=animation_cmap
            )
            
            # Convert to GIF and display
            gif_buf = anim_to_gif(anim, n_frames=n_steps)
            st.image(gif_buf, caption=t["time_evolution_caption"])
