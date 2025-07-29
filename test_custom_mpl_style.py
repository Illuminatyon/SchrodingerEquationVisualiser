"""
Test script for the custom_mpl_style module.

This script tests the colormap creation in the set_mpl_theme() function
without launching the full Streamlit application.
"""

import matplotlib.pyplot as plt
import numpy as np
import custom_mpl_style

def test_set_mpl_theme():
    """Test the set_mpl_theme function."""
    print("Testing set_mpl_theme()...")
    try:
        style_dict, quantum_cmap = custom_mpl_style.set_mpl_theme()
        print("Success! set_mpl_theme() executed without errors.")
        return True
    except Exception as e:
        print(f"Error in set_mpl_theme(): {e}")
        return False

def test_colormap():
    """Test the quantum colormap by creating a simple plot."""
    print("\nTesting colormap with a simple plot...")
    try:
        # Create a simple 2D array to visualize with the colormap
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        
        # Create a figure and plot using the quantum colormap
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.pcolormesh(X, Y, Z, cmap='quantum')
        fig.colorbar(im, ax=ax, label='Value')
        ax.set_title('Test of quantum colormap')
        
        # Save the figure to verify it works
        fig.savefig('test_colormap.png')
        print("Success! Colormap test plot created and saved as 'test_colormap.png'.")
        return True
    except Exception as e:
        print(f"Error in colormap test: {e}")
        return False

if __name__ == "__main__":
    # Test the set_mpl_theme function
    theme_success = test_set_mpl_theme()
    
    # If set_mpl_theme succeeded, test the colormap
    if theme_success:
        colormap_success = test_colormap()
        
    print("\nTest summary:")
    print(f"- set_mpl_theme(): {'SUCCESS' if theme_success else 'FAILED'}")
    if theme_success:
        print(f"- colormap test: {'SUCCESS' if colormap_success else 'FAILED'}")