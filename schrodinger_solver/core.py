"""
Core functionality for solving the Schrödinger equation.

This module provides the fundamental functions for constructing the Hamiltonian
matrix and solving the eigenvalue problem to find energy levels and wave functions.
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh


def construct_laplacian_1d(n_points, dx, boundary_condition='dirichlet'):
    """
    Construct the 1D Laplacian operator matrix using finite difference method.
    
    Parameters
    ----------
    n_points : int
        Number of spatial grid points.
    dx : float
        Spatial step size.
    boundary_condition : str, optional
        Type of boundary condition ('dirichlet' or 'periodic').
        Default is 'dirichlet' (wave function is zero at boundaries).
        
    Returns
    -------
    scipy.sparse.csr_matrix
        Sparse matrix representing the Laplacian operator.
    """
    if boundary_condition.lower() not in ['dirichlet', 'periodic']:
        raise ValueError("boundary_condition must be 'dirichlet' or 'periodic'")
    
    # Construct the second derivative operator using central difference
    diagonals = [-2.0 * np.ones(n_points), np.ones(n_points-1), np.ones(n_points-1)]
    offsets = [0, 1, -1]
    
    # Create the Laplacian matrix
    laplacian = sparse.diags(diagonals, offsets, shape=(n_points, n_points), format='csr')
    
    # Apply boundary conditions
    if boundary_condition.lower() == 'periodic':
        # Connect the first and last points
        laplacian[0, n_points-1] = 1.0
        laplacian[n_points-1, 0] = 1.0
    
    # Scale by -1/(dx^2) to get the correct Laplacian
    laplacian = -laplacian / (dx**2)
    
    return laplacian


def construct_laplacian_2d(nx, ny, dx, dy, boundary_condition='dirichlet'):
    """
    Construct the 2D Laplacian operator matrix using finite difference method.
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points in x and y directions.
    dx, dy : float
        Spatial step sizes in x and y directions.
    boundary_condition : str, optional
        Type of boundary condition ('dirichlet' or 'periodic').
        Default is 'dirichlet' (wave function is zero at boundaries).
        
    Returns
    -------
    scipy.sparse.csr_matrix
        Sparse matrix representing the Laplacian operator.
    """
    if boundary_condition.lower() not in ['dirichlet', 'periodic']:
        raise ValueError("boundary_condition must be 'dirichlet' or 'periodic'")
    
    # Total number of grid points
    n_total = nx * ny
    
    # Create 1D Laplacians for x and y directions
    laplacian_x = construct_laplacian_1d(nx, dx, boundary_condition)
    laplacian_y = construct_laplacian_1d(ny, dy, boundary_condition)
    
    # Create identity matrices
    identity_x = sparse.eye(nx, format='csr')
    identity_y = sparse.eye(ny, format='csr')
    
    # Construct 2D Laplacian using Kronecker products
    laplacian_2d = sparse.kron(identity_y, laplacian_x) + sparse.kron(laplacian_y, identity_x)
    
    return laplacian_2d


def construct_hamiltonian(laplacian, potential_values, hbar=1.0, mass=1.0):
    """
    Construct the Hamiltonian matrix for the Schrödinger equation.
    
    Parameters
    ----------
    laplacian : scipy.sparse.csr_matrix
        The Laplacian operator matrix.
    potential_values : numpy.ndarray
        Array of potential values at each grid point.
    hbar : float, optional
        Reduced Planck constant. Default is 1.0 (natural units).
    mass : float, optional
        Particle mass. Default is 1.0 (natural units).
        
    Returns
    -------
    scipy.sparse.csr_matrix
        Sparse matrix representing the Hamiltonian operator.
    """
    # Construct the kinetic energy term: -ħ²/(2m) ∇²
    kinetic = -0.5 * (hbar**2 / mass) * laplacian
    
    # Construct the potential energy term as a diagonal matrix
    potential = sparse.diags(potential_values, format='csr')
    
    # The Hamiltonian is the sum of kinetic and potential energy
    hamiltonian = kinetic + potential
    
    return hamiltonian


def solve_schrodinger(hamiltonian, n_eigenstates=6, which='SM'):
    """
    Solve the time-independent Schrödinger equation to find energy eigenvalues
    and eigenfunctions.
    
    Parameters
    ----------
    hamiltonian : scipy.sparse.csr_matrix
        The Hamiltonian operator matrix.
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
    # Solve the eigenvalue problem
    eigenvalues, eigenvectors = eigsh(hamiltonian, k=n_eigenstates, which=which)
    
    # Sort eigenvalues and eigenvectors
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return eigenvalues, eigenvectors


def time_evolution(initial_state, hamiltonian, time_points, hbar=1.0):
    """
    Compute the time evolution of a quantum state under a time-independent Hamiltonian.
    
    Parameters
    ----------
    initial_state : numpy.ndarray
        Initial wave function.
    hamiltonian : scipy.sparse.csr_matrix
        The Hamiltonian operator matrix.
    time_points : numpy.ndarray
        Array of time points at which to compute the wave function.
    hbar : float, optional
        Reduced Planck constant. Default is 1.0 (natural units).
        
    Returns
    -------
    states : numpy.ndarray
        Array of wave functions at each time point.
    """
    # Solve the eigenvalue problem for the Hamiltonian
    eigenvalues, eigenvectors = solve_schrodinger(hamiltonian, n_eigenstates=min(20, hamiltonian.shape[0]))
    
    # Express the initial state in the energy eigenbasis
    coefficients = np.dot(eigenvectors.T.conj(), initial_state)
    
    # Initialize array to store states at each time point
    states = np.zeros((len(time_points), len(initial_state)), dtype=complex)
    
    # Compute the state at each time point
    for i, t in enumerate(time_points):
        # Apply time evolution operator exp(-i*H*t/ħ) in the energy eigenbasis
        time_evolved_coeffs = coefficients * np.exp(-1j * eigenvalues * t / hbar)
        # Transform back to position basis
        states[i] = np.dot(eigenvectors, time_evolved_coeffs)
    
    return states