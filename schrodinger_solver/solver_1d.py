"""
1D Schrödinger equation solver.

This module provides specialized functionality for solving the 1D Schrödinger equation,
building on the core functions and potential implementations.
"""

import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt

from schrodinger_solver.core import (
    construct_laplacian_1d,
    construct_hamiltonian,
    solve_schrodinger,
    time_evolution
)


class Schrodinger1D:
    """
    Class for solving the 1D time-independent Schrödinger equation.
    """
    
    def __init__(self, x_min, x_max, n_points, potential_func, hbar=1.0, mass=1.0, boundary='dirichlet', **potential_params):
        """
        Initialize the 1D Schrödinger equation solver.
        
        Parameters
        ----------
        x_min, x_max : float
            Minimum and maximum x-coordinates of the domain.
        n_points : int
            Number of spatial grid points.
        potential_func : callable
            Function that takes x_grid and returns potential values.
        hbar : float, optional
            Reduced Planck constant. Default is 1.0 (natural units).
        mass : float, optional
            Particle mass. Default is 1.0 (natural units).
        boundary : str, optional
            Boundary condition ('dirichlet' or 'periodic'). Default is 'dirichlet'.
        **potential_params : dict
            Additional parameters to pass to the potential function.
        """
        self.x_min = x_min
        self.x_max = x_max
        self.n_points = n_points
        self.potential_func = potential_func
        self.potential_params = potential_params
        self.hbar = hbar
        self.mass = mass
        self.boundary = boundary
        
        # Create the spatial grid
        self.dx = (x_max - x_min) / (n_points - 1)
        self.x_grid = np.linspace(x_min, x_max, n_points)
        
        # Compute the potential values
        self.potential_values = potential_func(self.x_grid, **potential_params)
        
        # Construct the Laplacian operator
        self.laplacian = construct_laplacian_1d(n_points, self.dx, boundary)
        
        # Construct the Hamiltonian
        self.hamiltonian = construct_hamiltonian(self.laplacian, self.potential_values, hbar, mass)
        
        # Initialize attributes for eigenvalues and eigenvectors
        self.eigenvalues = None
        self.eigenvectors = None
    
    def solve(self, n_eigenstates=6, which='SM'):
        """
        Solve the time-independent Schrödinger equation to find energy eigenvalues
        and eigenfunctions.
        
        Parameters
        ----------
        n_eigenstates : int, optional
            Number of eigenstates to compute. Default is 6.
        which : str, optional
            Which eigenvalues to find:
            - 'SM': Smallest eigenvalues in magnitude (default)
            - 'SA': Smallest eigenvalues algebraically
            
        Returns
        -------
        eigenvalues : numpy.ndarray
            Array of energy eigenvalues.
        eigenvectors : numpy.ndarray
            Array of eigenvectors (wave functions).
        """
        self.eigenvalues, self.eigenvectors = solve_schrodinger(
            self.hamiltonian, n_eigenstates, which
        )
        return self.eigenvalues, self.eigenvectors
    
    def get_eigenfunction(self, n):
        """
        Get the nth eigenfunction (wave function).
        
        Parameters
        ----------
        n : int
            Index of the eigenfunction to retrieve (0-based).
            
        Returns
        -------
        numpy.ndarray
            The normalized eigenfunction.
        """
        if self.eigenvectors is None:
            raise ValueError("You must call solve() first.")
        
        if n < 0 or n >= self.eigenvectors.shape[1]:
            raise ValueError(f"Invalid eigenfunction index. Must be between 0 and {self.eigenvectors.shape[1]-1}.")
        
        # Extract the eigenfunction
        psi = self.eigenvectors[:, n]
        
        # Normalize the eigenfunction
        norm = np.sqrt(np.trapz(np.abs(psi)**2, x=self.x_grid))
        psi = psi / norm
        
        return psi
    
    def get_probability_density(self, n):
        """
        Get the probability density for the nth eigenstate.
        
        Parameters
        ----------
        n : int
            Index of the eigenstate (0-based).
            
        Returns
        -------
        numpy.ndarray
            The probability density |ψ|².
        """
        psi = self.get_eigenfunction(n)
        return np.abs(psi)**2
    
    def evolve_state(self, initial_state, t_max, n_steps):
        """
        Evolve an initial state in time under the Hamiltonian.
        
        Parameters
        ----------
        initial_state : numpy.ndarray
            Initial wave function.
        t_max : float
            Maximum time for evolution.
        n_steps : int
            Number of time steps.
            
        Returns
        -------
        times : numpy.ndarray
            Array of time points.
        states : numpy.ndarray
            Array of wave functions at each time point.
        """
        # Create time points
        times = np.linspace(0, t_max, n_steps)
        
        # Evolve the state
        states = time_evolution(initial_state, self.hamiltonian, times, self.hbar)
        
        return times, states
    
    def plot_potential(self, ax=None, **plot_kwargs):
        """
        Plot the potential function.
        
        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure is created.
        **plot_kwargs : dict
            Additional keyword arguments to pass to the plot function.
            
        Returns
        -------
        matplotlib.axes.Axes
            The axes containing the plot.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(self.x_grid, self.potential_values, **plot_kwargs)
        ax.set_xlabel('Position')
        ax.set_ylabel('Potential Energy')
        ax.set_title('Potential Function')
        
        return ax
    
    def plot_eigenfunction(self, n, ax=None, **plot_kwargs):
        """
        Plot the nth eigenfunction.
        
        Parameters
        ----------
        n : int
            Index of the eigenfunction to plot (0-based).
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure is created.
        **plot_kwargs : dict
            Additional keyword arguments to pass to the plot function.
            
        Returns
        -------
        matplotlib.axes.Axes
            The axes containing the plot.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        psi = self.get_eigenfunction(n)
        energy = self.eigenvalues[n]
        
        ax.plot(self.x_grid, psi, **plot_kwargs)
        ax.set_xlabel('Position')
        ax.set_ylabel('Wave Function')
        ax.set_title(f'Eigenfunction {n} (E = {energy:.4f})')
        
        return ax
    
    def plot_probability_density(self, n, ax=None, **plot_kwargs):
        """
        Plot the probability density for the nth eigenstate.
        
        Parameters
        ----------
        n : int
            Index of the eigenstate (0-based).
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure is created.
        **plot_kwargs : dict
            Additional keyword arguments to pass to the plot function.
            
        Returns
        -------
        matplotlib.axes.Axes
            The axes containing the plot.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        prob_density = self.get_probability_density(n)
        energy = self.eigenvalues[n]
        
        ax.plot(self.x_grid, prob_density, **plot_kwargs)
        ax.set_xlabel('Position')
        ax.set_ylabel('Probability Density')
        ax.set_title(f'Probability Density for State {n} (E = {energy:.4f})')
        
        return ax
    
    def plot_eigenstates(self, n_states=None, figsize=(12, 8)):
        """
        Plot multiple eigenfunctions and the potential.
        
        Parameters
        ----------
        n_states : int, optional
            Number of eigenstates to plot. If None, all computed states are plotted.
        figsize : tuple, optional
            Figure size. Default is (12, 8).
            
        Returns
        -------
        matplotlib.figure.Figure
            The figure containing the plots.
        """
        if self.eigenvectors is None:
            raise ValueError("You must call solve() first.")
        
        if n_states is None:
            n_states = self.eigenvectors.shape[1]
        else:
            n_states = min(n_states, self.eigenvectors.shape[1])
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot the potential
        ax.plot(self.x_grid, self.potential_values, 'k--', label='Potential')
        
        # Plot the eigenfunctions, shifted by their energy
        for n in range(n_states):
            psi = self.get_eigenfunction(n)
            energy = self.eigenvalues[n]
            
            # Scale the eigenfunction for better visualization
            scale_factor = 0.1 * (np.max(self.potential_values) - np.min(self.potential_values))
            psi_scaled = psi * scale_factor + energy
            
            ax.plot(self.x_grid, psi_scaled, label=f'E{n} = {energy:.4f}')
            
            # Add a horizontal line at the energy level
            ax.axhline(y=energy, color='gray', linestyle=':', alpha=0.5)
        
        ax.set_xlabel('Position')
        ax.set_ylabel('Energy / Wave Function')
        ax.set_title('Eigenfunctions and Potential')
        ax.legend()
        
        return fig
    
    def animate_time_evolution(self, initial_state, t_max, n_steps, interval=50, figsize=(10, 6)):
        """
        Create an animation of the time evolution of a quantum state.
        
        Parameters
        ----------
        initial_state : numpy.ndarray
            Initial wave function.
        t_max : float
            Maximum time for evolution.
        n_steps : int
            Number of time steps.
        interval : int, optional
            Interval between frames in milliseconds. Default is 50.
        figsize : tuple, optional
            Figure size. Default is (10, 6).
            
        Returns
        -------
        matplotlib.animation.FuncAnimation
            Animation of the time evolution.
        """
        import matplotlib.animation as animation
        
        # Evolve the state
        times, states = self.evolve_state(initial_state, t_max, n_steps)
        
        # Create the figure and axes
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot the potential
        ax.plot(self.x_grid, self.potential_values, 'k--', label='Potential')
        
        # Initialize the line for the wave function
        line_real, = ax.plot([], [], 'b-', label='Re(ψ)')
        line_imag, = ax.plot([], [], 'r-', label='Im(ψ)')
        line_prob, = ax.plot([], [], 'g-', label='|ψ|²')
        
        # Set up the axes
        ax.set_xlabel('Position')
        ax.set_ylabel('Wave Function / Probability')
        ax.set_title('Time Evolution of Quantum State')
        
        # Set the y-limits based on the maximum amplitude
        max_amplitude = np.max(np.abs(states))
        ax.set_ylim(-1.5 * max_amplitude, 1.5 * max_amplitude)
        ax.set_xlim(self.x_min, self.x_max)
        
        # Add a text annotation for the time
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        
        # Add legend
        ax.legend()
        
        # Define the update function for the animation
        def update(frame):
            # Update the wave function
            psi = states[frame]
            
            # Update the lines
            line_real.set_data(self.x_grid, np.real(psi))
            line_imag.set_data(self.x_grid, np.imag(psi))
            line_prob.set_data(self.x_grid, np.abs(psi)**2)
            
            # Update the time text
            time_text.set_text(f'Time: {times[frame]:.2f}')
            
            return line_real, line_imag, line_prob, time_text
        
        # Create the animation
        anim = animation.FuncAnimation(
            fig, update, frames=n_steps, interval=interval, blit=True
        )
        
        return anim