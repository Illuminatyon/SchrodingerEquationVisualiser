# Colormap Registration Fix

## Issue Description

The Streamlit application was failing with the following error:

```
ValueError: 'quantum' is not a valid value for cmap; supported values are 'Accent', 'Accent_r', 'Blues', 'Blues_r', ...
```

This error occurred when trying to use the custom 'quantum' colormap by name in the Streamlit application. The error message indicates that the 'quantum' colormap was not properly registered with matplotlib, so it couldn't be found when referenced by name.

## Root Cause

In the `custom_mpl_style.py` file, we were creating a custom colormap named 'quantum' using `LinearSegmentedColormap.from_list()`, but we were not properly registering it with matplotlib so that it could be referenced by name elsewhere in the code.

The original code was:

```python
quantum_cmap = LinearSegmentedColormap.from_list('quantum', 
                                            list(zip(positions, colors_array)))

# Set the colormap as default without explicit registration
plt.set_cmap(quantum_cmap)
```

While this code set the colormap as the default, it didn't register it with matplotlib's colormap registry, which is necessary for the colormap to be accessible by name in other parts of the code.

## Solution

The fix was to properly register the colormap with matplotlib using the appropriate registration method. Since the registration API has changed across different matplotlib versions, we implemented a version-compatible approach that tries different methods:

```python
# Register the colormap with matplotlib so it can be referenced by name
# Use the appropriate registration method based on matplotlib version
try:
    # For newer matplotlib versions
    plt.colormaps.register(quantum_cmap)
except AttributeError:
    try:
        # Alternative for newer versions
        mpl.colormaps.register(quantum_cmap)
    except AttributeError:
        # For older matplotlib versions
        plt.register_cmap(name='quantum', cmap=quantum_cmap)
```

This approach ensures that the colormap is properly registered regardless of the matplotlib version being used:

1. First, it tries `plt.colormaps.register(quantum_cmap)` for newer matplotlib versions (3.5+)
2. If that fails, it tries `mpl.colormaps.register(quantum_cmap)` as an alternative for newer versions
3. If both fail, it falls back to `plt.register_cmap(name='quantum', cmap=quantum_cmap)` for older matplotlib versions

## Technical Explanation

In matplotlib, colormaps need to be registered in the colormap registry to be accessible by name. When you reference a colormap by name (e.g., `cmap='quantum'`), matplotlib looks up the name in its registry to find the corresponding colormap object.

The registration API has changed across different matplotlib versions:

- In older versions (before 3.5), colormaps were registered using `plt.register_cmap()` or `mpl.cm.register_cmap()`
- In newer versions (3.5+), colormaps are registered using `plt.colormaps.register()` or `mpl.colormaps.register()`

Our solution handles all these cases by trying each method in a try-except block, ensuring compatibility across different matplotlib versions.

## Testing

The fix was tested using a dedicated test script (`test_colormap_registration.py`) that verifies:

1. The 'quantum' colormap is successfully registered and available in the list of colormaps
2. The colormap can be retrieved by name using `plt.get_cmap('quantum')`
3. A plot can be created and saved using the 'quantum' colormap by name

The test confirmed that the fix works correctly, and the 'quantum' colormap is now properly registered and can be referenced by name.

## Conclusion

This fix ensures that the custom 'quantum' colormap is properly registered with matplotlib, allowing it to be referenced by name in the Streamlit application and other parts of the code. The version-compatible approach ensures that the fix works across different matplotlib versions.