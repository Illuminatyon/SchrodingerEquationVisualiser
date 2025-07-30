"""
2D Schrödinger equation solver.

This module provides specialized functionality for solving the 2D Schrödinger equation,
building on the core functions and potential implementations.
"""

import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from schrodinger_solver.core import (
    construct_laplacian_2d,
    construct_hamiltonian,
    solve_schrodinger,
    time_evolution
)


class Schrodinger2D:
    """
    Class for solving the 2D time-independent Schrödinger equation.
    """
    
    def __init__(self, x_min, x_max, y_min, y_max, nx, ny, potential_func, 
                 hbar=1.0, mass=1.0, boundary='dirichlet', **potential_params):
        """
        Initialize the 2D Schrödinger equation solver.
        
        Parameters
        ----------
        x_min, x_max : float
            Minimum and maximum x-coordinates of the domain.
        y_min, y_max : float
            Minimum and maximum y-coordinates of the domain.
        nx, ny : int
            Number of spatial grid points in x and y directions.
        potential_func : callable
            Function that takes x_grid, y_grid and returns potential values.
        hbar : float, optional
            Reduced Planck constant. Default is 1.0 (natural units).
        mass : float, optional
            Particle mass. Default is 1.0 (natural units).
        boundary : str, optional
            Boundary condition ('dirichlet' or 'periodic'). Default is 'dirichlet'.
        **potential_params : dict
            Additional parameters to pass to the potential function.
        """
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.nx, self.ny = nx, ny
        self.potential_func = potential_func
        self.potential_params = potential_params
        self.hbar = hbar
        self.mass = mass
        self.boundary = boundary
        
        # Create the spatial grid
        self.dx = (x_max - x_min) / (nx - 1)
        self.dy = (y_max - y_min) / (ny - 1)
        
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        self.x_grid, self.y_grid = np.meshgrid(x, y)
        
        # Compute the potential values
        self.potential_values = potential_func(self.x_grid, self.y_grid, **potential_params)
        
        # Flatten the potential values for the Hamiltonian construction
        self.potential_flat = self.potential_values.flatten()
        
        # Construct the Laplacian operator
        self.laplacian = construct_laplacian_2d(nx, ny, self.dx, self.dy, boundary)
        
        # Construct the Hamiltonian
        self.hamiltonian = construct_hamiltonian(self.laplacian, self.potential_flat, hbar, mass)
        
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
        Get the nth eigenfunction (wave function) reshaped to 2D.
        
        Parameters
        ----------
        n : int
            Index of the eigenfunction to retrieve (0-based).
            
        Returns
        -------
        numpy.ndarray
            The normalized eigenfunction reshaped to 2D.
        """
        if self.eigenvectors is None:
            raise ValueError("You must call solve() first.")
        
        if n < 0 or n >= self.eigenvectors.shape[1]:
            raise ValueError(f"Invalid eigenfunction index. Must be between 0 and {self.eigenvectors.shape[1]-1}.")
        
        # Extract the eigenfunction
        psi_flat = self.eigenvectors[:, n]
        
        # Reshape to 2D
        psi_2d = psi_flat.reshape(self.ny, self.nx)
        
        # Normalize the eigenfunction
        norm = np.sqrt(np.sum(np.abs(psi_2d)**2) * self.dx * self.dy)
        psi_2d = psi_2d / norm
        
        return psi_2d
    
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
            The probability density |ψ|² reshaped to 2D.
        """
        psi_2d = self.get_eigenfunction(n)
        return np.abs(psi_2d)**2
    
    def evolve_state(self, initial_state_2d, t_max, n_steps):
        """
        Evolve an initial state in time under the Hamiltonian.
        
        Parameters
        ----------
        initial_state_2d : numpy.ndarray
            Initial wave function in 2D shape (ny, nx).
        t_max : float
            Maximum time for evolution.
        n_steps : int
            Number of time steps.
            
        Returns
        -------
        times : numpy.ndarray
            Array of time points.
        states_2d : numpy.ndarray
            Array of wave functions at each time point, reshaped to 2D.
        """
        # Flatten the initial state
        initial_state_flat = initial_state_2d.flatten()
        
        # Create time points
        times = np.linspace(0, t_max, n_steps)
        
        # Evolve the state
        states_flat = time_evolution(initial_state_flat, self.hamiltonian, times, self.hbar)
        
        # Reshape the states to 2D
        states_2d = np.zeros((n_steps, self.ny, self.nx), dtype=complex)
        for i in range(n_steps):
            states_2d[i] = states_flat[i].reshape(self.ny, self.nx)
        
        return times, states_2d
    
    def plot_potential(self, ax=None, figsize=(10, 8), cmap='viridis', **plot_kwargs):
        """
        Plot the potential function.
        
        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure is created.
        figsize : tuple, optional
            Figure size. Default is (10, 8).
        cmap : str, optional
            Colormap to use. Default is 'viridis'.
        **plot_kwargs : dict
            Additional keyword arguments to pass to the plot function.
            
        Returns
        -------
        matplotlib.axes.Axes
            The axes containing the plot.
        """
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(self.x_grid, self.y_grid, self.potential_values, 
                               cmap=cmap, **plot_kwargs)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Potential Energy')
        ax.set_title('Potential Function')
        
        plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        
        return ax
    
    def plot_eigenfunction(self, n, ax=None, figsize=(10, 8), cmap='quantum_diverging', plot_type='surface', **plot_kwargs):
        """
        Plot the nth eigenfunction.
        
        Parameters
        ----------
        n : int
            Index of the eigenfunction to plot (0-based).
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure is created.
        figsize : tuple, optional
            Figure size. Default is (10, 8).
        cmap : str, optional
            Colormap to use. Default is 'quantum_diverging' for better visualization of negative values.
        plot_type : str, optional
            Type of plot ('surface', 'contour', or 'contourf'). Default is 'surface'.
        **plot_kwargs : dict
            Additional keyword arguments to pass to the plot function.
            
        Returns
        -------
        matplotlib.axes.Axes
            The axes containing the plot.
        """
        if self.eigenvectors is None:
            raise ValueError("You must call solve() first.")
        
        # Import the formatter for negative values
        from custom_mpl_style import format_negative_values, FuncFormatter
        
        psi_2d = self.get_eigenfunction(n)
        energy = self.eigenvalues[n]
        
        # Format the energy value with a more prominent minus sign if negative
        if energy < 0:
            energy_str = f"E = −{abs(energy):.4f}"  # Unicode minus sign
        else:
            energy_str = f"E = {energy:.4f}"
        
        if ax is None:
            fig = plt.figure(figsize=figsize)
            if plot_type == 'surface':
                ax = fig.add_subplot(111, projection='3d')
            else:
                ax = fig.add_subplot(111)
        
        if plot_type == 'surface':
            surf = ax.plot_surface(self.x_grid, self.y_grid, np.real(psi_2d), 
                                  cmap=cmap, **plot_kwargs)
            ax.set_zlabel('Wave Function')
            cbar = plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_negative_values))
        elif plot_type == 'contour':
            contour = ax.contour(self.x_grid, self.y_grid, np.real(psi_2d), 
                                cmap=cmap, **plot_kwargs)
            cbar = plt.colorbar(contour, ax=ax)
            cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_negative_values))
        elif plot_type == 'contourf':
            contourf = ax.contourf(self.x_grid, self.y_grid, np.real(psi_2d), 
                                  cmap=cmap, **plot_kwargs)
            cbar = plt.colorbar(contourf, ax=ax)
            cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_negative_values))
        else:
            raise ValueError("plot_type must be 'surface', 'contour', or 'contourf'")
        
        # Make negative labels in colorbar bold
        for label in cbar.ax.get_yticklabels():
            if '−' in label.get_text():  # Unicode minus sign
                label.set_fontweight('bold')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Eigenfunction {n} ({energy_str})')
        
        return ax
    
    def plot_probability_density(self, n, ax=None, figsize=(10, 8), cmap='viridis', plot_type='contourf', **plot_kwargs):
        """
        Plot the probability density for the nth eigenstate.
        
        Parameters
        ----------
        n : int
            Index of the eigenstate (0-based).
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure is created.
        figsize : tuple, optional
            Figure size. Default is (10, 8).
        cmap : str, optional
            Colormap to use. Default is 'viridis'.
        plot_type : str, optional
            Type of plot ('surface', 'contour', or 'contourf'). Default is 'contourf'.
        **plot_kwargs : dict
            Additional keyword arguments to pass to the plot function.
            
        Returns
        -------
        matplotlib.axes.Axes
            The axes containing the plot.
        """
        if self.eigenvectors is None:
            raise ValueError("You must call solve() first.")
        
        # Import the formatter for negative values
        from custom_mpl_style import format_negative_values, FuncFormatter
        
        prob_density = self.get_probability_density(n)
        energy = self.eigenvalues[n]
        
        # Format the energy value with a more prominent minus sign if negative
        if energy < 0:
            energy_str = f"E = −{abs(energy):.4f}"  # Unicode minus sign
        else:
            energy_str = f"E = {energy:.4f}"
        
        if ax is None:
            fig = plt.figure(figsize=figsize)
            if plot_type == 'surface':
                ax = fig.add_subplot(111, projection='3d')
            else:
                ax = fig.add_subplot(111)
        
        if plot_type == 'surface':
            surf = ax.plot_surface(self.x_grid, self.y_grid, prob_density, 
                                  cmap=cmap, **plot_kwargs)
            ax.set_zlabel('Probability Density')
            cbar = plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            # No need for negative value formatting for probability density (always positive)
        elif plot_type == 'contour':
            contour = ax.contour(self.x_grid, self.y_grid, prob_density, 
                                cmap=cmap, **plot_kwargs)
            cbar = plt.colorbar(contour, ax=ax)
        elif plot_type == 'contourf':
            contourf = ax.contourf(self.x_grid, self.y_grid, prob_density, 
                                  cmap=cmap, **plot_kwargs)
            cbar = plt.colorbar(contourf, ax=ax)
        else:
            raise ValueError("plot_type must be 'surface', 'contour', or 'contourf'")
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Probability Density for State {n} ({energy_str})')
        
        return ax
    
    def plot_eigenstates_grid(self, n_states=None, figsize=(15, 10), cmap='quantum_diverging', plot_type='contourf'):
        """
        Plot multiple eigenstates in a grid.
        
        Parameters
        ----------
        n_states : int, optional
            Number of eigenstates to plot. If None, all computed states are plotted.
        figsize : tuple, optional
            Figure size. Default is (15, 10).
        cmap : str, optional
            Colormap to use. Default is 'quantum_diverging' for better visualization of negative values.
        plot_type : str, optional
            Type of plot ('contour' or 'contourf'). Default is 'contourf'.
            
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
        
        # Determine grid layout
        n_cols = int(np.ceil(np.sqrt(n_states)))
        n_rows = int(np.ceil(n_states / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        
        # Flatten axes array for easy indexing
        if n_rows > 1 and n_cols > 1:
            axes = axes.flatten()
        
        for i in range(n_states):
            # Get the current axis
            if n_states == 1:
                ax = axes
            else:
                ax = axes[i]
            
            # Plot the eigenstate
            if plot_type == 'contour':
                self.plot_eigenfunction(i, ax=ax, cmap=cmap, plot_type='contour')
            else:
                self.plot_eigenfunction(i, ax=ax, cmap=cmap, plot_type='contourf')
        
        # Hide any unused subplots
        if n_states < n_rows * n_cols:
            for i in range(n_states, n_rows * n_cols):
                if n_states > 1:
                    axes[i].axis('off')
        
        plt.tight_layout()
        return fig
    
    def animate_time_evolution(self, initial_state_2d, t_max, n_steps, interval=50, figsize=(10, 8), cmap='viridis'):
        """
        Create an animation of the time evolution of a quantum state.
        
        Parameters
        ----------
        initial_state_2d : numpy.ndarray
            Initial wave function in 2D shape (ny, nx).
        t_max : float
            Maximum time for evolution.
        n_steps : int
            Number of time steps.
        interval : int, optional
            Interval between frames in milliseconds. Default is 50.
        figsize : tuple, optional
            Figure size. Default is (10, 8).
        cmap : str, optional
            Colormap to use. Default is 'viridis'.
            
        Returns
        -------
        matplotlib.animation.FuncAnimation
            Animation of the time evolution.
        """
        import matplotlib.animation as animation
        from custom_mpl_style import format_negative_values, FuncFormatter
        
        # Evolve the state
        times, states_2d = self.evolve_state(initial_state_2d, t_max, n_steps)
        
        # Create the figure and axes
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Plot the potential on the first axis
        contourf_pot = axes[0].contourf(self.x_grid, self.y_grid, self.potential_values, cmap='quantum_diverging')
        axes[0].set_xlabel('X')
        axes[0].set_ylabel('Y')
        axes[0].set_title('Potential')
        cbar_pot = plt.colorbar(contourf_pot, ax=axes[0])
        
        # Apply special formatting for negative values in the potential colorbar
        cbar_pot.ax.yaxis.set_major_formatter(FuncFormatter(format_negative_values))
        
        # Make negative labels in colorbar bold
        for label in cbar_pot.ax.get_yticklabels():
            if '−' in label.get_text():  # Unicode minus sign
                label.set_fontweight('bold')
        
        # Initialize the probability density plot on the second axis
        prob_density = np.abs(initial_state_2d)**2
        contourf_prob = axes[1].contourf(self.x_grid, self.y_grid, prob_density, cmap=cmap)
        axes[1].set_xlabel('X')
        axes[1].set_ylabel('Y')
        axes[1].set_title('Probability Density')
        plt.colorbar(contourf_prob, ax=axes[1])
        
        # Add a text annotation for the time
        time_text = axes[1].text(0.02, 0.95, '', transform=axes[1].transAxes)
        
        # Define the update function for the animation
        def update(frame):
            # Clear the second axis
            axes[1].clear()
            
            # Update the probability density
            psi = states_2d[frame]
            prob_density = np.abs(psi)**2
            
            # Plot the new probability density
            contourf_prob = axes[1].contourf(self.x_grid, self.y_grid, prob_density, cmap=cmap)
            axes[1].set_xlabel('X')
            axes[1].set_ylabel('Y')
            axes[1].set_title('Probability Density')
            
            # Update the time text
            time_text = axes[1].text(0.02, 0.95, f'Time: {times[frame]:.2f}', transform=axes[1].transAxes)
            
            return contourf_prob, time_text
        
        # Create the animation
        anim = animation.FuncAnimation(
            fig, update, frames=n_steps, interval=interval, blit=False
        )
        
        return anim