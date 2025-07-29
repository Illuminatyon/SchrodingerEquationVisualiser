# Dependency Update for Python 3.11 Compatibility

## Changes Made

The `requirements.txt` file has been updated to ensure compatibility with Python 3.11. The following changes were made:

| Package | Original Version | Updated Version | Reason |
|---------|-----------------|-----------------|--------|
| numpy | >=1.20.0 | >=1.23.0 | NumPy 1.23.0 was the first version to officially support Python 3.11 |
| scipy | >=1.7.0 | >=1.9.0 | SciPy 1.9.0 was the first version to officially support Python 3.11 |
| matplotlib | >=3.4.0 | >=3.6.0 | Matplotlib 3.6.0 was the first version to officially support Python 3.11 |
| streamlit | >=1.10.0 | >=1.13.0 | Streamlit 1.13.0 and later support Python 3.11 |
| pillow | >=8.0.0 | >=9.2.0 | Pillow 9.2.0 was the first version to officially support Python 3.11 |

## Why These Changes Were Necessary

The original error occurred because NumPy 1.20.0 is not compatible with Python 3.11. When pip tried to install this version, it attempted to compile from source, which failed due to missing Microsoft Visual C++ 14.0 build tools.

The error message included:
```
error: Microsoft Visual C++ 14.0 is required. Get it with "Build Tools for Visual Studio": https://visualstudio.microsoft.com/downloads/
```

And a warning:
```
NumPy 1.20.0 may not yet support Python 3.11.
```

By updating to versions that officially support Python 3.11, we ensure that:
1. Pre-built wheels are available, eliminating the need for compilation
2. The packages are fully compatible with Python 3.11
3. Installation can proceed without requiring additional build tools

## How to Test the Updated Requirements

To test the updated requirements, follow these steps:

1. Make sure you're in your project's virtual environment:
   ```
   # On Windows
   .venv\Scripts\activate
   ```

2. Install the updated dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Verify the installation was successful:
   ```
   python -c "import numpy; import scipy; import matplotlib; import streamlit; import PIL; print('All dependencies successfully imported!')"
   ```

## Alternative Solutions

If you still encounter issues, you have these alternatives:

1. **Install Visual C++ Build Tools**: If you prefer to use the original versions, you can install Microsoft Visual C++ Build Tools from: https://visualstudio.microsoft.com/downloads/

2. **Use a Different Python Version**: The original dependencies are compatible with Python 3.8, 3.9, and 3.10.

3. **Use Conda**: Anaconda/Miniconda often provides pre-built packages that avoid compilation issues:
   ```
   conda create -n schrodinger python=3.11
   conda activate schrodinger
   conda install numpy scipy matplotlib pillow
   pip install streamlit
   ```

## Additional Resources

- [NumPy Python Support Policy](https://numpy.org/neps/nep-0029-deprecation_policy.html)
- [SciPy Python Support Policy](https://scipy.github.io/devdocs/dev/core-dev/index.html#supported-python-and-numpy-versions)
- [Matplotlib Python Support](https://matplotlib.org/stable/users/installing/index.html)
- [Streamlit Installation Guide](https://docs.streamlit.io/library/get-started/installation)
- [Pillow Installation Guide](https://pillow.readthedocs.io/en/stable/installation.html)