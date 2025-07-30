"""
Test script to verify that negative values are properly displayed in plots.
"""

import matplotlib.pyplot as plt
import numpy as np
from custom_mpl_style import set_mpl_theme, format_negative_values
from matplotlib.ticker import FuncFormatter

def test_negative_value_display():
    """Test that negative values are properly displayed in plots."""
    # Set the custom theme which registers the quantum colormap
    set_mpl_theme()
    
    # Create a simple plot with positive and negative values
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Generate some data with positive and negative values
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = X * np.exp(-X**2 - Y**2)  # This will have positive and negative values
    
    # Plot with the standard viridis colormap
    im1 = axes[0].contourf(X, Y, Z, cmap='viridis')
    axes[0].set_title('Standard Colormap (viridis)')
    cbar1 = plt.colorbar(im1, ax=axes[0])
    
    # Plot with the quantum_diverging colormap and enhanced negative value display
    im2 = axes[1].contourf(X, Y, Z, cmap='quantum_diverging')
    axes[1].set_title('Quantum Diverging Colormap with Enhanced Negative Values')
    cbar2 = plt.colorbar(im2, ax=axes[1])
    cbar2.ax.yaxis.set_major_formatter(FuncFormatter(format_negative_values))
    
    # Make negative labels in colorbar bold
    for label in cbar2.ax.get_yticklabels():
        if '−' in label.get_text():  # Unicode minus sign
            label.set_fontweight('bold')
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('test_negative_values.png')
    print("Test plot saved as 'test_negative_values.png'")
    
    return True

if __name__ == "__main__":
    test_negative_value_display()