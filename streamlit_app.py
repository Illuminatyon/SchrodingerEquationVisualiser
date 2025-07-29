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


# Set page configuration
st.set_page_config(
    page_title="Schrödinger Equation Solver",
    page_icon="🔬",
    layout="wide",
)

# Title and description
st.title("Schrödinger Equation Solver")
st.markdown("""
This app solves the time-independent Schrödinger equation and visualizes the eigenstates
and time evolution of quantum states for various potentials in 1D and 2D.

The equation being solved is:

$$-\\frac{\\hbar^2}{2m}\\nabla^2\\psi + V(\\mathbf{r})\\psi = E\\psi$$

where:
- $\\psi$ is the wave function
- $\\hbar$ is the reduced Planck constant
- $m$ is the particle mass
- $V(\\mathbf{r})$ is the potential
- $E$ is the energy
""")

# Sidebar for parameters
st.sidebar.header("Parameters")

# Dimension selection
dimension = st.sidebar.radio("Dimension", [1, 2], index=0)

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
domain_min = st.sidebar.slider("Domain Minimum", -10.0, 0.0, -5.0)
domain_max = st.sidebar.slider("Domain Maximum", 0.0, 10.0, 5.0)

# Grid resolution
if dimension == 1:
    n_points = st.sidebar.slider("Number of Grid Points", 100, 2000, 1000)
else:  # dimension == 2
    n_points = st.sidebar.slider("Number of Grid Points per Dimension", 50, 200, 100)

# Number of eigenstates
n_states = st.sidebar.slider("Number of Eigenstates", 1, 10, 6)

# Potential-specific parameters
st.sidebar.subheader("Potential Parameters")

if potential_name == "Infinite Well":
    if dimension == 1:
        width = st.sidebar.slider("Width", 0.1, domain_max - domain_min, 5.0)
        offset = st.sidebar.slider("Offset", domain_min, domain_max, 0.0)
        potential_params = {"width": width, "offset": offset, "depth": 0.0, "wall_value": 1e6}
    else:  # dimension == 2
        width_x = st.sidebar.slider("Width X", 0.1, domain_max - domain_min, 5.0)
        width_y = st.sidebar.slider("Width Y", 0.1, domain_max - domain_min, 5.0)
        offset_x = st.sidebar.slider("Offset X", domain_min, domain_max, 0.0)
        offset_y = st.sidebar.slider("Offset Y", domain_min, domain_max, 0.0)
        potential_params = {
            "width_x": width_x, "width_y": width_y, 
            "offset_x": offset_x, "offset_y": offset_y, 
            "depth": 0.0, "wall_value": 1e6
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
    potential_params = {
        "radius": radius, "center_x": center_x, "center_y": center_y, 
        "depth": 0.0, "wall_value": 1e6
    }

# Time evolution parameters
st.sidebar.subheader("Time Evolution")
animate = st.sidebar.checkbox("Animate Time Evolution", value=False)

if animate:
    t_max = st.sidebar.slider("Maximum Time", 1.0, 50.0, 10.0)
    n_steps = st.sidebar.slider("Number of Time Steps", 50, 200, 100)
    
    # Wave packet parameters
    st.sidebar.subheader("Initial Wave Packet")
    if dimension == 1:
        packet_center = st.sidebar.slider(
            "Packet Center", domain_min, domain_max, (domain_min + domain_max)/2
        )
        packet_width = st.sidebar.slider(
            "Packet Width", 0.1, (domain_max - domain_min)/5, (domain_max - domain_min)/10
        )
        packet_k0 = st.sidebar.slider("Initial Momentum", -5.0, 5.0, 2.0)
    else:  # dimension == 2
        packet_center_x = st.sidebar.slider(
            "Packet Center X", domain_min, domain_max, (domain_min + domain_max)/2
        )
        packet_center_y = st.sidebar.slider(
            "Packet Center Y", domain_min, domain_max, (domain_min + domain_max)/2
        )
        packet_width_x = st.sidebar.slider(
            "Packet Width X", 0.1, (domain_max - domain_min)/5, (domain_max - domain_min)/10
        )
        packet_width_y = st.sidebar.slider(
            "Packet Width Y", 0.1, (domain_max - domain_min)/5, (domain_max - domain_min)/10
        )
        packet_k0_x = st.sidebar.slider("Initial Momentum X", -5.0, 5.0, 2.0)
        packet_k0_y = st.sidebar.slider("Initial Momentum Y", -5.0, 5.0, 0.0)


# Function to create a Gaussian wave packet
def create_gaussian_wave_packet(x_grid, center, width, k0):
    """Create a Gaussian wave packet."""
    return np.exp(-0.5 * ((x_grid - center) / width)**2) * np.exp(1j * k0 * x_grid)


def create_gaussian_wave_packet_2d(x_grid, y_grid, center_x, center_y, width_x, width_y, k0_x, k0_y):
    """Create a 2D Gaussian wave packet."""
    return (np.exp(-0.5 * ((x_grid - center_x) / width_x)**2 - 0.5 * ((y_grid - center_y) / width_y)**2) 
            * np.exp(1j * (k0_x * x_grid + k0_y * y_grid)))


# Function to convert matplotlib animation to a GIF for Streamlit
def anim_to_gif(anim):
    """Convert a matplotlib animation to a GIF."""
    frames = []
    for i in range(anim._fig._framecount):
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
        **potential_params
    )
    
    # Solve for eigenstates
    with st.spinner("Solving the Schrödinger equation..."):
        eigenvalues, eigenvectors = solver.solve(n_eigenstates=n_states)
    
    # Display eigenvalues
    st.subheader("Energy Eigenvalues")
    eigenvalues_df = {"State": list(range(n_states)), "Energy": eigenvalues}
    st.dataframe(eigenvalues_df)
    
    # Plot eigenstates
    st.subheader("Eigenstates and Potential")
    fig = solver.plot_eigenstates(n_states=n_states)
    st.pyplot(fig)
    
    # Animate time evolution if requested
    if animate:
        st.subheader("Time Evolution")
        
        # Create initial wave packet
        initial_state = create_gaussian_wave_packet(
            solver.x_grid, packet_center, packet_width, packet_k0
        )
        
        # Normalize the initial state
        norm = np.sqrt(np.trapz(np.abs(initial_state)**2, x=solver.x_grid))
        initial_state = initial_state / norm
        
        with st.spinner("Creating animation..."):
            # Create the animation
            anim = solver.animate_time_evolution(initial_state, t_max, n_steps)
            
            # Convert to GIF and display
            gif_buf = anim_to_gif(anim)
            st.image(gif_buf, caption="Time Evolution of Quantum State")

else:  # dimension == 2
    # Create 2D solver
    solver = Schrodinger2D(
        x_min=domain_min,
        x_max=domain_max,
        y_min=domain_min,
        y_max=domain_max,
        nx=n_points,
        ny=n_points,
        potential_func=potential_func,
        **potential_params
    )
    
    # Solve for eigenstates
    with st.spinner("Solving the Schrödinger equation..."):
        eigenvalues, eigenvectors = solver.solve(n_eigenstates=n_states)
    
    # Display eigenvalues
    st.subheader("Energy Eigenvalues")
    eigenvalues_df = {"State": list(range(n_states)), "Energy": eigenvalues}
    st.dataframe(eigenvalues_df)
    
    # Plot potential
    st.subheader("Potential")
    fig_potential = plt.figure(figsize=(8, 6))
    ax = fig_potential.add_subplot(111, projection='3d')
    solver.plot_potential(ax=ax)
    st.pyplot(fig_potential)
    
    # Plot eigenstates
    st.subheader("Eigenstates")
    fig_eigenstates = solver.plot_eigenstates_grid(n_states=n_states)
    st.pyplot(fig_eigenstates)
    
    # Animate time evolution if requested
    if animate:
        st.subheader("Time Evolution")
        
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
            anim = solver.animate_time_evolution(initial_state, t_max, n_steps)
            
            # Convert to GIF and display
            gif_buf = anim_to_gif(anim)
            st.image(gif_buf, caption="Time Evolution of Quantum State")

# Add information about the project
st.markdown("""
---
### About this Project

This app is a numerical solver for the Schrödinger equation in 1D and 2D. It uses:

- Finite difference method for spatial discretization
- Sparse matrix eigenvalue solver for finding energy levels and wave functions
- Matplotlib for visualization
- Streamlit for the interactive interface

The code is available on GitHub: [schrodinger-solver](https://github.com/your-username/schrodinger-solver)
""")