"""
Potential functions for the Schrödinger equation.

This module provides implementations of various potential functions commonly used
in quantum mechanics problems, such as infinite well, harmonic oscillator, barrier
potential, and double well.
"""

import numpy as np


def infinite_well_1d(x_grid, width=1.0, offset=0.0, depth=0.0, wall_value=1e6):
    """
    Create a 1D infinite potential well (particle in a box).
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        Array of x-coordinates.
    width : float, optional
        Width of the well. Default is 1.0.
    offset : float, optional
        Position offset of the well center. Default is 0.0.
    depth : float, optional
        Potential value inside the well. Default is 0.0.
    wall_value : float, optional
        Potential value outside the well (should be very large). Default is 1e6.
        
    Returns
    -------
    numpy.ndarray
        Array of potential values at each grid point.
    """
    potential = np.ones_like(x_grid) * wall_value
    
    # Define the well region
    well_min = offset - width/2
    well_max = offset + width/2
    
    # Set the potential inside the well
    mask = (x_grid >= well_min) & (x_grid <= well_max)
    potential[mask] = depth
    
    return potential


def harmonic_oscillator_1d(x_grid, k=1.0, mass=1.0, center=0.0):
    """
    Create a 1D harmonic oscillator potential: V(x) = 0.5 * k * (x - center)^2.
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        Array of x-coordinates.
    k : float, optional
        Spring constant. Default is 1.0.
    mass : float, optional
        Particle mass. Default is 1.0.
    center : float, optional
        Center position of the oscillator. Default is 0.0.
        
    Returns
    -------
    numpy.ndarray
        Array of potential values at each grid point.
    """
    return 0.5 * k * (x_grid - center)**2


def barrier_potential_1d(x_grid, height=1.0, width=0.1, position=0.0):
    """
    Create a 1D potential barrier.
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        Array of x-coordinates.
    height : float, optional
        Height of the barrier. Default is 1.0.
    width : float, optional
        Width of the barrier. Default is 0.1.
    position : float, optional
        Position of the barrier center. Default is 0.0.
        
    Returns
    -------
    numpy.ndarray
        Array of potential values at each grid point.
    """
    potential = np.zeros_like(x_grid)
    
    # Define the barrier region
    barrier_min = position - width/2
    barrier_max = position + width/2
    
    # Set the potential at the barrier
    mask = (x_grid >= barrier_min) & (x_grid <= barrier_max)
    potential[mask] = height
    
    return potential


def double_well_1d(x_grid, height=1.0, width=2.0, barrier_width=0.5, barrier_height=2.0):
    """
    Create a 1D double well potential (two wells separated by a barrier).
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        Array of x-coordinates.
    height : float, optional
        Base height of the potential. Default is 1.0.
    width : float, optional
        Total width of the double well. Default is 2.0.
    barrier_width : float, optional
        Width of the central barrier. Default is 0.5.
    barrier_height : float, optional
        Height of the central barrier. Default is 2.0.
        
    Returns
    -------
    numpy.ndarray
        Array of potential values at each grid point.
    """
    potential = np.ones_like(x_grid) * height
    
    # Define the wells and barrier regions
    well_width = (width - barrier_width) / 2
    left_well_min = -width/2
    left_well_max = left_well_min + well_width
    right_well_min = width/2 - well_width
    right_well_max = width/2
    
    # Set the potential in the wells
    left_mask = (x_grid >= left_well_min) & (x_grid <= left_well_max)
    right_mask = (x_grid >= right_well_min) & (x_grid <= right_well_max)
    potential[left_mask | right_mask] = 0.0
    
    # Set the potential at the barrier
    barrier_min = left_well_max
    barrier_max = right_well_min
    barrier_mask = (x_grid > barrier_min) & (x_grid < barrier_max)
    potential[barrier_mask] = barrier_height
    
    return potential


def morse_potential_1d(x_grid, D=1.0, a=1.0, r_e=0.0):
    """
    Create a 1D Morse potential: V(x) = D * (1 - exp(-a*(x-r_e)))^2.
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        Array of x-coordinates.
    D : float, optional
        Dissociation energy. Default is 1.0.
    a : float, optional
        Controls the width of the potential well. Default is 1.0.
    r_e : float, optional
        Equilibrium position. Default is 0.0.
        
    Returns
    -------
    numpy.ndarray
        Array of potential values at each grid point.
    """
    return D * (1.0 - np.exp(-a * (x_grid - r_e)))**2


# 2D Potentials

def infinite_well_2d(x_grid, y_grid, width_x=1.0, width_y=1.0, offset_x=0.0, offset_y=0.0, depth=0.0, wall_value=1e6):
    """
    Create a 2D infinite potential well (particle in a box).
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        2D array of x-coordinates.
    y_grid : numpy.ndarray
        2D array of y-coordinates.
    width_x, width_y : float, optional
        Width of the well in x and y directions. Default is 1.0.
    offset_x, offset_y : float, optional
        Position offset of the well center. Default is 0.0.
    depth : float, optional
        Potential value inside the well. Default is 0.0.
    wall_value : float, optional
        Potential value outside the well (should be very large). Default is 1e6.
        
    Returns
    -------
    numpy.ndarray
        2D array of potential values at each grid point.
    """
    potential = np.ones_like(x_grid) * wall_value
    
    # Define the well region
    well_x_min = offset_x - width_x/2
    well_x_max = offset_x + width_x/2
    well_y_min = offset_y - width_y/2
    well_y_max = offset_y + width_y/2
    
    # Set the potential inside the well
    mask = (x_grid >= well_x_min) & (x_grid <= well_x_max) & (y_grid >= well_y_min) & (y_grid <= well_y_max)
    potential[mask] = depth
    
    return potential


def harmonic_oscillator_2d(x_grid, y_grid, k_x=1.0, k_y=1.0, mass=1.0, center_x=0.0, center_y=0.0):
    """
    Create a 2D harmonic oscillator potential: V(x,y) = 0.5 * k_x * (x - center_x)^2 + 0.5 * k_y * (y - center_y)^2.
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        2D array of x-coordinates.
    y_grid : numpy.ndarray
        2D array of y-coordinates.
    k_x, k_y : float, optional
        Spring constants in x and y directions. Default is 1.0.
    mass : float, optional
        Particle mass. Default is 1.0.
    center_x, center_y : float, optional
        Center position of the oscillator. Default is 0.0.
        
    Returns
    -------
    numpy.ndarray
        2D array of potential values at each grid point.
    """
    return 0.5 * k_x * (x_grid - center_x)**2 + 0.5 * k_y * (y_grid - center_y)**2


def circular_well_2d(x_grid, y_grid, radius=1.0, center_x=0.0, center_y=0.0, depth=0.0, wall_value=1e6):
    """
    Create a 2D circular potential well.
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        2D array of x-coordinates.
    y_grid : numpy.ndarray
        2D array of y-coordinates.
    radius : float, optional
        Radius of the circular well. Default is 1.0.
    center_x, center_y : float, optional
        Center position of the well. Default is 0.0.
    depth : float, optional
        Potential value inside the well. Default is 0.0.
    wall_value : float, optional
        Potential value outside the well (should be very large). Default is 1e6.
        
    Returns
    -------
    numpy.ndarray
        2D array of potential values at each grid point.
    """
    potential = np.ones_like(x_grid) * wall_value
    
    # Calculate distance from center
    r_squared = (x_grid - center_x)**2 + (y_grid - center_y)**2
    
    # Set the potential inside the circular well
    mask = r_squared <= radius**2
    potential[mask] = depth
    
    return potential


def double_well_2d(x_grid, y_grid, height=1.0, width=2.0, barrier_width=0.5, barrier_height=2.0, direction='x'):
    """
    Create a 2D double well potential (two wells separated by a barrier).
    
    Parameters
    ----------
    x_grid : numpy.ndarray
        2D array of x-coordinates.
    y_grid : numpy.ndarray
        2D array of y-coordinates.
    height : float, optional
        Base height of the potential. Default is 1.0.
    width : float, optional
        Total width of the double well. Default is 2.0.
    barrier_width : float, optional
        Width of the central barrier. Default is 0.5.
    barrier_height : float, optional
        Height of the central barrier. Default is 2.0.
    direction : str, optional
        Direction of the double well ('x' or 'y'). Default is 'x'.
        
    Returns
    -------
    numpy.ndarray
        2D array of potential values at each grid point.
    """
    potential = np.ones_like(x_grid) * height
    
    if direction.lower() == 'x':
        grid = x_grid
    elif direction.lower() == 'y':
        grid = y_grid
    else:
        raise ValueError("direction must be 'x' or 'y'")
    
    # Define the wells and barrier regions
    well_width = (width - barrier_width) / 2
    left_well_min = -width/2
    left_well_max = left_well_min + well_width
    right_well_min = width/2 - well_width
    right_well_max = width/2
    
    # Set the potential in the wells
    left_mask = (grid >= left_well_min) & (grid <= left_well_max)
    right_mask = (grid >= right_well_min) & (grid <= right_well_max)
    potential[left_mask | right_mask] = 0.0
    
    # Set the potential at the barrier
    barrier_min = left_well_max
    barrier_max = right_well_min
    barrier_mask = (grid > barrier_min) & (grid < barrier_max)
    potential[barrier_mask] = barrier_height
    
    return potential