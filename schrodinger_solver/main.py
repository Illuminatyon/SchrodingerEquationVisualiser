"""
Main entry point for the Schrödinger equation solver.

This module provides command-line functionality for solving the Schrödinger equation
in 1D and 2D with various potentials.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

from schrodinger_solver import potentials
from schrodinger_solver.solver_1d import Schrodinger1D
from schrodinger_solver.solver_2d import Schrodinger2D


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Solve the Schrödinger equation.')
    
    parser.add_argument('--dimension', type=int, choices=[1, 2], default=1,
                        help='Dimension of the problem (1 or 2). Default is 1.')
    
    parser.add_argument('--potential', type=str, 
                        choices=['infinite_well', 'harmonic', 'barrier', 'double_well', 'morse', 'circular'],
                        default='harmonic',
                        help='Type of potential to use. Default is "harmonic".')
    
    parser.add_argument('--n_points', type=int, default=1000,
                        help='Number of spatial grid points (per dimension). Default is 1000.')
    
    parser.add_argument('--domain_min', type=float, default=-5.0,
                        help='Minimum value of the spatial domain. Default is -5.0.')
    
    parser.add_argument('--domain_max', type=float, default=5.0,
                        help='Maximum value of the spatial domain. Default is 5.0.')
    
    parser.add_argument('--n_states', type=int, default=6,
                        help='Number of eigenstates to compute. Default is 6.')
    
    parser.add_argument('--save_plot', type=str, default=None,
                        help='Filename to save the plot. If not provided, the plot is displayed.')
    
    parser.add_argument('--animate', action='store_true',
                        help='Create an animation of time evolution.')
    
    parser.add_argument('--t_max', type=float, default=10.0,
                        help='Maximum time for evolution animation. Default is 10.0.')
    
    parser.add_argument('--n_steps', type=int, default=100,
                        help='Number of time steps for evolution animation. Default is 100.')
    
    return parser.parse_args()


def get_potential_function(potential_name, dimension):
    """Get the potential function based on the name and dimension."""
    if dimension == 1:
        if potential_name == 'infinite_well':
            return potentials.infinite_well_1d
        elif potential_name == 'harmonic':
            return potentials.harmonic_oscillator_1d
        elif potential_name == 'barrier':
            return potentials.barrier_potential_1d
        elif potential_name == 'double_well':
            return potentials.double_well_1d
        elif potential_name == 'morse':
            return potentials.morse_potential_1d
        else:
            raise ValueError(f"Unknown 1D potential: {potential_name}")
    else:  # dimension == 2
        if potential_name == 'infinite_well':
            return potentials.infinite_well_2d
        elif potential_name == 'harmonic':
            return potentials.harmonic_oscillator_2d
        elif potential_name == 'circular':
            return potentials.circular_well_2d
        elif potential_name == 'double_well':
            return potentials.double_well_2d
        else:
            raise ValueError(f"Unknown 2D potential: {potential_name}")


def get_potential_params(potential_name):
    """Get default parameters for the potential."""
    if potential_name == 'infinite_well':
        return {'width': 5.0, 'offset': 0.0, 'depth': 0.0, 'wall_value': 1e6}
    elif potential_name == 'harmonic':
        return {'k': 1.0, 'mass': 1.0, 'center': 0.0}
    elif potential_name == 'barrier':
        return {'height': 5.0, 'width': 0.5, 'position': 0.0}
    elif potential_name == 'double_well':
        return {'height': 1.0, 'width': 4.0, 'barrier_width': 0.5, 'barrier_height': 5.0}
    elif potential_name == 'morse':
        return {'D': 10.0, 'a': 1.0, 'r_e': 0.0}
    elif potential_name == 'circular':
        return {'radius': 2.0, 'center_x': 0.0, 'center_y': 0.0, 'depth': 0.0, 'wall_value': 1e6}
    else:
        return {}


def create_gaussian_wave_packet(x_grid, center, width, k0):
    """Create a Gaussian wave packet."""
    return np.exp(-0.5 * ((x_grid - center) / width)**2) * np.exp(1j * k0 * x_grid)


def create_gaussian_wave_packet_2d(x_grid, y_grid, center_x, center_y, width_x, width_y, k0_x, k0_y):
    """Create a 2D Gaussian wave packet."""
    return (np.exp(-0.5 * ((x_grid - center_x) / width_x)**2 - 0.5 * ((y_grid - center_y) / width_y)**2) 
            * np.exp(1j * (k0_x * x_grid + k0_y * y_grid)))


def solve_1d(args):
    """Solve the 1D Schrödinger equation."""
    # Get the potential function and parameters
    potential_func = get_potential_function(args.potential, 1)
    potential_params = get_potential_params(args.potential)
    
    # Create the solver
    solver = Schrodinger1D(
        x_min=args.domain_min,
        x_max=args.domain_max,
        n_points=args.n_points,
        potential_func=potential_func,
        **potential_params
    )
    
    # Solve for eigenstates
    eigenvalues, eigenvectors = solver.solve(n_eigenstates=args.n_states)
    
    # Plot the results
    fig = solver.plot_eigenstates(n_states=args.n_states)
    
    if args.animate:
        # Create an initial wave packet
        center = (args.domain_min + args.domain_max) / 2
        width = (args.domain_max - args.domain_min) / 10
        k0 = 2.0  # Initial momentum
        initial_state = create_gaussian_wave_packet(solver.x_grid, center, width, k0)
        
        # Normalize the initial state
        norm = np.sqrt(np.trapz(np.abs(initial_state)**2, x=solver.x_grid))
        initial_state = initial_state / norm
        
        # Create the animation
        anim = solver.animate_time_evolution(initial_state, args.t_max, args.n_steps)
        
        # Display or save the animation
        if args.save_plot:
            anim_filename = args.save_plot.replace('.png', '.gif')
            anim.save(anim_filename, writer='pillow', fps=15)
            print(f"Animation saved to {anim_filename}")
    
    # Display or save the plot
    if args.save_plot:
        fig.savefig(args.save_plot)
        print(f"Plot saved to {args.save_plot}")
    else:
        plt.show()


def solve_2d(args):
    """Solve the 2D Schrödinger equation."""
    # Get the potential function and parameters
    potential_func = get_potential_function(args.potential, 2)
    potential_params = get_potential_params(args.potential)
    
    # For 2D, we use fewer points per dimension to keep the computation manageable
    n_points_per_dim = min(args.n_points, 100)
    
    # Create the solver
    solver = Schrodinger2D(
        x_min=args.domain_min,
        x_max=args.domain_max,
        y_min=args.domain_min,
        y_max=args.domain_max,
        nx=n_points_per_dim,
        ny=n_points_per_dim,
        potential_func=potential_func,
        **potential_params
    )
    
    # Solve for eigenstates
    eigenvalues, eigenvectors = solver.solve(n_eigenstates=args.n_states)
    
    # Plot the results
    fig = solver.plot_eigenstates_grid(n_states=args.n_states)
    
    if args.animate:
        # Create an initial wave packet
        center_x = (args.domain_min + args.domain_max) / 2
        center_y = (args.domain_min + args.domain_max) / 2
        width_x = (args.domain_max - args.domain_min) / 10
        width_y = (args.domain_max - args.domain_min) / 10
        k0_x = 2.0  # Initial momentum in x
        k0_y = 0.0  # Initial momentum in y
        
        initial_state = create_gaussian_wave_packet_2d(
            solver.x_grid, solver.y_grid, center_x, center_y, width_x, width_y, k0_x, k0_y
        )
        
        # Normalize the initial state
        norm = np.sqrt(np.sum(np.abs(initial_state)**2) * solver.dx * solver.dy)
        initial_state = initial_state / norm
        
        # Create the animation
        anim = solver.animate_time_evolution(initial_state, args.t_max, args.n_steps)
        
        # Display or save the animation
        if args.save_plot:
            anim_filename = args.save_plot.replace('.png', '.gif')
            anim.save(anim_filename, writer='pillow', fps=15)
            print(f"Animation saved to {anim_filename}")
    
    # Display or save the plot
    if args.save_plot:
        fig.savefig(args.save_plot)
        print(f"Plot saved to {args.save_plot}")
    else:
        plt.show()


def main():
    """Main entry point."""
    args = parse_args()
    
    if args.dimension == 1:
        solve_1d(args)
    else:  # args.dimension == 2
        solve_2d(args)


if __name__ == '__main__':
    main()