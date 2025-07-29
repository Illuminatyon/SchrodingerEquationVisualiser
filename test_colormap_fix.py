"""
Test script to verify the colormap fix in custom_mpl_style.py

This script tests the modified colormap creation in the set_mpl_theme() function
to ensure it works correctly with the new implementation.
"""

import matplotlib.pyplot as plt
import numpy as np
import custom_mpl_style

def test_colormap_creation():
    """Test the colormap creation in set_mpl_theme()."""
    print("Testing colormap creation with the new implementation...")
    try:
        # Call set_mpl_theme() to create the colormap
        style_dict, quantum_cmap = custom_mpl_style.set_mpl_theme()
        print("Success! Colormap created successfully.")
        
        # Verify the colormap object is valid
        print(f"Colormap name: {quantum_cmap.name}")
        
        # Check that the colormap can be used to map values to colors
        test_values = np.linspace(0, 1, 5)
        colors = quantum_cmap(test_values)
        print(f"Sample colors from colormap: {colors.shape}")
        print(f"First color: {colors[0]}")
        
        print("Colormap validation successful!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_colormap_creation()
    print(f"\nTest result: {'SUCCESS' if success else 'FAILED'}")