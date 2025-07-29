"""
Test script to verify that the 'quantum' colormap is properly registered with matplotlib.

This script tests that the colormap can be referenced by name after it's registered.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import custom_mpl_style

def test_colormap_registration():
    """Test that the 'quantum' colormap is properly registered."""
    print("Testing colormap registration...")
    
    # Call set_mpl_theme() to create and register the colormap
    style_dict, quantum_cmap = custom_mpl_style.set_mpl_theme()
    
    # Check if 'quantum' is in the list of available colormaps
    available_cmaps = plt.colormaps()
    if 'quantum' in available_cmaps:
        print("Success! 'quantum' colormap is registered and available.")
        print(f"Available colormaps: {len(available_cmaps)}")
        print(f"Some example colormaps: {available_cmaps[:5]}...")
    else:
        print("Error: 'quantum' colormap is not registered.")
        print(f"Available colormaps: {available_cmaps}")
        return False
    
    # Try to get the colormap by name
    try:
        cmap = plt.get_cmap('quantum')
        print(f"Successfully retrieved 'quantum' colormap by name.")
        print(f"Colormap name: {cmap.name}")
        return True
    except Exception as e:
        print(f"Error retrieving 'quantum' colormap by name: {e}")
        return False

def test_colormap_usage():
    """Test using the 'quantum' colormap by name in a plot."""
    print("\nTesting colormap usage...")
    
    try:
        # Create a simple 2D array to visualize with the colormap
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        
        # Create a figure and plot using the 'quantum' colormap by name
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.pcolormesh(X, Y, Z, cmap='quantum')
        fig.colorbar(im, ax=ax, label='Value')
        ax.set_title('Test of quantum colormap')
        
        # Save the figure to verify it works
        fig.savefig('test_colormap_registration.png')
        print("Success! Created and saved a plot using the 'quantum' colormap by name.")
        return True
    except Exception as e:
        print(f"Error in colormap usage test: {e}")
        return False

if __name__ == "__main__":
    # Test the colormap registration
    registration_success = test_colormap_registration()
    
    # If registration succeeded, test using the colormap
    if registration_success:
        usage_success = test_colormap_usage()
    else:
        usage_success = False
    
    print("\nTest summary:")
    print(f"- Colormap registration: {'SUCCESS' if registration_success else 'FAILED'}")
    print(f"- Colormap usage: {'SUCCESS' if usage_success else 'FAILED'}")