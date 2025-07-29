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
)

# Custom CSS with Computer Modern font and animations
st.markdown("""
<style>
    /* Import Computer Modern font */
    @import url('https://cdn.jsdelivr.net/npm/computer-modern-font@1.0.0/index.css');
    
    /* Apply Computer Modern font to all text */
    html, body, [class*="css"] {
        font-family: 'Computer Modern Serif', serif !important;
    }
    
    /* Style headers */
    h1, h2, h3, h4 {
        font-family: 'Computer Modern Serif', serif !important;
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Main title animation */
    h1 {
        background: linear-gradient(45deg, #4B8BBE, #306998, #FFE873);
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
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, #162B4D 10%, #0E1E3E 90%) !important;
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
        background-color: rgba(22, 43, 77, 0.7);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .element-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Computer Modern Serif', serif !important;
        border-collapse: collapse;
        margin: 20px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    
    .dataframe thead th {
        background-color: #4B8BBE;
        color: white;
        font-weight: bold;
        text-align: left;
        padding: 12px 15px;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #dddddd;
        transition: background-color 0.3s;
    }
    
    .dataframe tbody tr:nth-of-type(even) {
        background-color: rgba(22, 43, 77, 0.7);
    }
    
    .dataframe tbody tr:last-of-type {
        border-bottom: 2px solid #4B8BBE;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(75, 139, 190, 0.3);
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
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0E1E3E;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4B8BBE;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #306998;
    }
</style>
""", unsafe_allow_html=True)

# Custom header with logo and title
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 20px; background: linear-gradient(90deg, rgba(14,30,62,0.8) 0%, rgba(22,43,77,0.9) 100%); padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <div style="font-size: 42px; margin-right: 20px; animation: pulse 2s infinite;">🔬</div>
    <div>
        <h1 style="margin: 0; background: linear-gradient(45deg, #4B8BBE, #306998, #FFE873); background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradient 6s ease infinite;">Schrödinger Equation Solver</h1>
        <p style="margin: 0; font-style: italic; color: #FFFFFF;">Quantum mechanics visualization tool</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Description with animated border
st.markdown("""
<div style="border: 2px solid #4B8BBE; border-radius: 10px; padding: 20px; margin-bottom: 20px; position: relative; overflow: hidden; animation: borderPulse 4s infinite;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #FFE873, transparent); animation: borderFlow 2s infinite linear;"></div>
    <p>This app solves the time-independent Schrödinger equation and visualizes the eigenstates
    and time evolution of quantum states for various potentials in 1D and 2D.</p>
    
    <p>The equation being solved is:</p>
    
    $$-\\frac{\\hbar^2}{2m}\\nabla^2\\psi + V(\\mathbf{r})\\psi = E\\psi$$
    
    <p>where:</p>
    <ul>
        <li>$\\psi$ is the wave function</li>
        <li>$\\hbar$ is the reduced Planck constant</li>
        <li>$m$ is the particle mass</li>
        <li>$V(\\mathbf{r})$ is the potential</li>
        <li>$E$ is the energy</li>
    </ul>
    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #FFE873, transparent); animation: borderFlow 2s infinite linear reverse;"></div>
</div>

<style>
@keyframes borderFlow {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
@keyframes borderPulse {
    0% { box-shadow: 0 0 5px rgba(75, 139, 190, 0.5); }
    50% { box-shadow: 0 0 20px rgba(75, 139, 190, 0.8); }
    100% { box-shadow: 0 0 5px rgba(75, 139, 190, 0.5); }
}
</style>
""", unsafe_allow_html=True)

# Sidebar for parameters with custom styling
st.sidebar.markdown("""
<div style="background: linear-gradient(45deg, #0E1E3E, #162B4D); padding: 10px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h2 style="margin: 0; color: white; text-align: center; font-family: 'Computer Modern Serif', serif;">
        <span style="background: linear-gradient(45deg, #4B8BBE, #FFE873); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Parameters
        </span>
    </h2>
</div>
""", unsafe_allow_html=True)

# Add a help button at the top of the sidebar
with st.sidebar.expander("ℹ️ How to use this app", expanded=False):
    st.markdown("""
    <div style="font-family: 'Computer Modern Serif', serif;">
        <p><strong>Welcome to the Schrödinger Equation Solver!</strong></p>
        <p>This app allows you to visualize quantum states for various potentials in 1D and 2D.</p>
        <ol>
            <li>Select the <strong>dimension</strong> (1D or 2D)</li>
            <li>Choose a <strong>potential</strong> from the dropdown</li>
            <li>Adjust the <strong>domain</strong> and <strong>grid resolution</strong></li>
            <li>Modify <strong>potential-specific parameters</strong></li>
            <li>Enable <strong>time evolution</strong> to see animations</li>
        </ol>
        <p>The app will solve the Schrödinger equation and display the eigenstates and energy levels.</p>
        <p><em>Hover over any parameter for additional information!</em></p>
    </div>
    """, unsafe_allow_html=True)

# Dimension selection
dimension = st.sidebar.radio("Dimension", [1, 2], index=0)

# Physics parameters
st.sidebar.subheader("Physics Parameters")
hbar = st.sidebar.slider("Reduced Planck Constant (ħ)", 0.1, 2.0, 1.0, 
                         help="Value of ħ in natural units. Default is 1.0.")
mass = st.sidebar.slider("Particle Mass", 0.1, 10.0, 1.0,
                         help="Mass of the particle in natural units. Default is 1.0.")

# Solver options
st.sidebar.subheader("Solver Options")
boundary = st.sidebar.selectbox("Boundary Conditions", 
                               ["dirichlet", "periodic"], 
                               index=0,
                               help="'dirichlet': Wave function is zero at boundaries. 'periodic': Domain wraps around.")
which_eigenvalues = st.sidebar.selectbox("Eigenvalue Selection", 
                                        ["SM", "SA"], 
                                        index=0,
                                        help="'SM': Smallest eigenvalues in magnitude. 'SA': Smallest eigenvalues algebraically.")

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
st.sidebar.subheader("Time Evolution")
animate = st.sidebar.checkbox("Animate Time Evolution", value=False)

if animate:
    t_max = st.sidebar.slider("Maximum Time", 1.0, 50.0, 10.0)
    n_steps = st.sidebar.slider("Number of Time Steps", 50, 200, 100)
    
    # Animation options
    st.sidebar.subheader("Animation Options")
    animation_interval = st.sidebar.slider("Frame Interval (ms)", 10, 500, 50,
                                         help="Time between frames in milliseconds")
    if dimension == 2:
        animation_cmap = st.sidebar.selectbox("Animation Colormap", 
                                            ["viridis", "plasma", "inferno", "magma", "cividis", 
                                             "Blues", "Greens", "Reds", "Purples", "jet"],
                                            index=0,
                                            help="Colormap for animation")
    
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
        hbar=hbar,
        mass=mass,
        boundary=boundary,
        **potential_params
    )
    
    # Solve for eigenstates
    with st.spinner("Solving the Schrödinger equation..."):
        eigenvalues, eigenvectors = solver.solve(n_eigenstates=n_states, which=which_eigenvalues)
    
    # Display eigenvalues
    st.subheader("Energy Eigenvalues")
    eigenvalues_df = {"State": list(range(n_states)), "Energy": eigenvalues}
    st.dataframe(eigenvalues_df)
    
    # Plot eigenstates
    st.subheader("Eigenstates and Potential")
    fig = solver.plot_eigenstates(n_states=n_states, figsize=figsize)
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
            anim = solver.animate_time_evolution(
                initial_state, 
                t_max, 
                n_steps, 
                interval=animation_interval,
                figsize=figsize
            )
            
            # Convert to GIF and display
            gif_buf = anim_to_gif(anim)
            st.image(gif_buf, caption="Time Evolution of Quantum State")

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
    st.subheader("Energy Eigenvalues")
    eigenvalues_df = {"State": list(range(n_states)), "Energy": eigenvalues}
    st.dataframe(eigenvalues_df)
    
    # Plot potential
    st.subheader("Potential")
    fig_potential = plt.figure(figsize=figsize)
    ax = fig_potential.add_subplot(111, projection='3d')
    solver.plot_potential(ax=ax, cmap=colormap)
    st.pyplot(fig_potential)
    
    # Plot eigenstates
    st.subheader("Eigenstates")
    fig_eigenstates = solver.plot_eigenstates_grid(n_states=n_states, figsize=figsize, cmap=colormap, plot_type=plot_type)
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
            anim = solver.animate_time_evolution(
                initial_state, 
                t_max, 
                n_steps, 
                interval=animation_interval,
                figsize=figsize,
                cmap=animation_cmap
            )
            
            # Convert to GIF and display
            gif_buf = anim_to_gif(anim)
            st.image(gif_buf, caption="Time Evolution of Quantum State")

# Add information about the project with enhanced styling
st.markdown("""
<div style="height: 2px; background: linear-gradient(90deg, #0E1E3E, #4B8BBE, #0E1E3E); margin: 40px 0 20px 0;"></div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, rgba(14,30,62,0.8) 0%, rgba(22,43,77,0.9) 100%); 
            padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            border-left: 5px solid #4B8BBE; margin-bottom: 20px;">
    <h2 style="color: white; font-family: 'Computer Modern Serif', serif; margin-top: 0;">
        <span style="background: linear-gradient(45deg, #4B8BBE, #FFE873); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            About this Project
        </span>
    </h2>
    <p>This app is a numerical solver for the Schrödinger equation in 1D and 2D, featuring an enhanced UI with animations and LaTeX styling.</p>
    
    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0;">
        <div style="flex: 1; min-width: 200px; background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h4 style="margin-top: 0; color: #FFE873;">Core Technology</h4>
            <ul style="margin-bottom: 0;">
                <li>Finite difference method for spatial discretization</li>
                <li>Sparse matrix eigenvalue solver for energy levels</li>
                <li>Matplotlib with custom styling for visualization</li>
                <li>Streamlit for the interactive interface</li>
            </ul>
        </div>
        <div style="flex: 1; min-width: 200px; background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h4 style="margin-top: 0; color: #FFE873;">UI Features</h4>
            <ul style="margin-bottom: 0;">
                <li>Computer Modern font for LaTeX-like typography</li>
                <li>Dark blue theme with custom styling</li>
                <li>Animated elements for a dynamic interface</li>
                <li>Responsive layout for different screen sizes</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Parameter guide with enhanced styling
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(14,30,62,0.8) 0%, rgba(22,43,77,0.9) 100%); 
            padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            border-left: 5px solid #4B8BBE; margin-bottom: 20px; position: relative; overflow: hidden;">
    
    <div style="position: absolute; top: 0; right: 0; width: 150px; height: 150px; 
                background: radial-gradient(circle, rgba(75,139,190,0.2) 0%, rgba(14,30,62,0) 70%); 
                border-radius: 50%; transform: translate(50%, -50%);"></div>
    
    <h2 style="color: white; font-family: 'Computer Modern Serif', serif; margin-top: 0;">
        <span style="background: linear-gradient(45deg, #4B8BBE, #FFE873); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Parameter Guide
        </span>
    </h2>
    
    <p>The app provides extensive customization options:</p>
    
    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
        <div style="flex: 1; min-width: 200px; background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 15px rgba(0,0,0,0.2)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)';">
            <h4 style="margin-top: 0; color: #FFE873;">Physics Parameters</h4>
            <ul style="margin-bottom: 0;">
                <li><strong>Reduced Planck Constant (ħ)</strong>: Controls quantum effects. Larger values increase quantum behavior.</li>
                <li><strong>Particle Mass</strong>: Affects kinetic energy. Heavier particles have less quantum tunneling.</li>
            </ul>
        </div>
        
        <div style="flex: 1; min-width: 200px; background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 15px rgba(0,0,0,0.2)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)';">
            <h4 style="margin-top: 0; color: #FFE873;">Solver Options</h4>
            <ul style="margin-bottom: 0;">
                <li><strong>Boundary Conditions</strong>: 'dirichlet' (wave function is zero at boundaries) or 'periodic' (domain wraps around).</li>
                <li><strong>Eigenvalue Selection</strong>: 'SM' (smallest magnitude) or 'SA' (smallest algebraically).</li>
            </ul>
        </div>
    </div>
    
    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
        <div style="flex: 1; min-width: 200px; background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 15px rgba(0,0,0,0.2)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)';">
            <h4 style="margin-top: 0; color: #FFE873;">Domain & Visualization</h4>
            <ul style="margin-bottom: 0;">
                <li>For 2D problems, you can set independent X and Y domains and grid resolutions.</li>
                <li>Customize figure size, colormaps, and plot types for 2D visualizations.</li>
            </ul>
        </div>
        
        <div style="flex: 1; min-width: 200px; background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 15px rgba(0,0,0,0.2)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)';">
            <h4 style="margin-top: 0; color: #FFE873;">Animation & Potentials</h4>
            <ul style="margin-bottom: 0;">
                <li>Frame interval controls animation speed. For 2D, you can select different colormaps.</li>
                <li>Each potential has specific parameters that can be adjusted.</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# UI Customization Guide
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(14,30,62,0.8) 0%, rgba(22,43,77,0.9) 100%); 
            padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            border-left: 5px solid #4B8BBE; margin-bottom: 20px;">
    <h2 style="color: white; font-family: 'Computer Modern Serif', serif; margin-top: 0;">
        <span style="background: linear-gradient(45deg, #4B8BBE, #FFE873); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            UI Customization Guide
        </span>
    </h2>
    
    <p>This application features a custom UI with several enhancements:</p>
    
    <div style="background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; margin-top: 15px;">
        <h4 style="margin-top: 0; color: #FFE873;">Theme Customization</h4>
        <p>The dark blue theme is configured in <code>.streamlit/config.toml</code> with these settings:</p>
        <pre style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; overflow-x: auto;">
[theme]
primaryColor = "#4B8BBE"  # Python blue
backgroundColor = "#0E1E3E"  # Dark blue
secondaryBackgroundColor = "#162B4D"  # Lighter dark blue
textColor = "#FFFFFF"  # White text
font = "Computer Modern"  # LaTeX-like font
        </pre>
    </div>
    
    <div style="background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; margin-top: 15px;">
        <h4 style="margin-top: 0; color: #FFE873;">Custom Styling</h4>
        <p>Additional styling is applied through custom CSS injected via <code>st.markdown()</code> with <code>unsafe_allow_html=True</code>:</p>
        <ul>
            <li>Computer Modern font loading from CDN</li>
            <li>Gradient animations for headers</li>
            <li>Hover effects for interactive elements</li>
            <li>Custom scrollbars and card-like sections</li>
        </ul>
    </div>
    
    <div style="background: rgba(14,30,62,0.5); padding: 15px; border-radius: 8px; margin-top: 15px;">
        <h4 style="margin-top: 0; color: #FFE873;">Plot Styling</h4>
        <p>Matplotlib plots use a custom dark theme defined in <code>custom_mpl_style.py</code> that matches the application's color scheme.</p>
    </div>
    
    <p style="margin-top: 15px;">The code is available on GitHub: <a href="https://github.com/your-username/schrodinger-solver" style="color: #4B8BBE; text-decoration: none; border-bottom: 1px dotted #4B8BBE;">schrodinger-solver</a></p>
</div>

<div style="text-align: center; margin: 30px 0; font-size: 12px; color: rgba(255,255,255,0.6);">
    <p>© 2025 | Created with ❤️ using Streamlit and Python</p>
</div>
""", unsafe_allow_html=True)