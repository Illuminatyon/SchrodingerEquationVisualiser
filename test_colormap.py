"""
Test script to verify that the colormap registration works correctly.
"""

import matplotlib.pyplot as plt
import numpy as np
from custom_mpl_style import set_mpl_theme

def test_colormap_registration():
    """Test that the quantum colormap is registered correctly."""
    # Set the custom theme which registers the quantum colormap
    set_mpl_theme()
    
    # Check if 'quantum' is in the available colormaps
    available_cmaps = plt.colormaps()
    if 'quantum' in available_cmaps:
        print("SUCCESS: 'quantum' colormap is registered correctly!")
    else:
        print("ERROR: 'quantum' colormap is not registered.")
        print("Available colormaps:", available_cmaps)
    
    # Create a simple plot using the quantum colormap
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Generate some data
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)
    
    # Plot with the quantum colormap
    im = ax.pcolormesh(X, Y, Z, cmap='quantum')
    plt.colorbar(im, ax=ax, label='Value')
    ax.set_title('Test of quantum colormap')
    
    # Save the figure
    plt.savefig('test_colormap_registration.png')
    print("Test plot saved as 'test_colormap_registration.png'")
    
    return 'quantum' in available_cmaps

if __name__ == "__main__":
    test_colormap_registration()