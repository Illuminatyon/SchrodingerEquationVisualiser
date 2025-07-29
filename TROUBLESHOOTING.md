# Troubleshooting Guide for Streamlit Application

## Problem: Nothing is displayed in the Streamlit application

If you're running the Streamlit application but nothing is being displayed, here are several troubleshooting steps to help resolve the issue.

## Step 1: Verify Streamlit Installation

First, make sure Streamlit is correctly installed:

```bash
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
```

If this command fails, reinstall Streamlit:

```bash
pip install streamlit>=1.13.0
```

## Step 2: Test with a Minimal Streamlit App

Try running the provided test application to check if Streamlit works in general:

```bash
streamlit run test_streamlit_app.py
```

If the test app displays correctly but the main app doesn't, the issue is specific to the Schrödinger solver application.

## Step 3: Check Browser Compatibility

Streamlit works best with modern browsers. Try the following:

1. **Use a different browser**: Chrome and Firefox are recommended for Streamlit apps.
2. **Clear browser cache**: Sometimes cached data can cause display issues.
3. **Disable browser extensions**: Some extensions might interfere with Streamlit.
4. **Check for JavaScript errors**: Open your browser's developer console (F12) to see if there are any errors.

## Step 4: Check Network Access

Streamlit runs as a local web server:

1. **Check firewall settings**: Make sure your firewall isn't blocking the Streamlit server.
2. **Try a different port**: If port 8501 is blocked, specify a different port:
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```
3. **Check localhost access**: Make sure you can access other localhost services.

## Step 5: Verify Dependencies

The Schrödinger solver requires several dependencies:

```bash
pip install -r requirements.txt
```

You can also check individual packages:

```bash
python -c "import numpy; import scipy; import matplotlib; import PIL; print('All dependencies successfully imported!')"
```

## Step 6: Check for Import Errors

If the application starts but shows an error, it might be due to import issues:

1. Make sure the `schrodinger_solver` package is in your Python path.
2. Check that all required modules are installed.

## Step 7: Run with Verbose Logging

Run Streamlit with debug logging to see detailed error messages:

```bash
streamlit run streamlit_app.py --logger.level=debug
```

## Step 8: Check System Resources

The Schrödinger solver performs complex calculations that require significant resources:

1. **Memory usage**: Make sure your system has enough RAM.
2. **CPU usage**: The calculations might take time on slower systems.

## Step 9: Try a Different Environment

If possible, try running the application in a different environment:

1. **Create a new virtual environment**:
   ```bash
   python -m venv new_venv
   new_venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

2. **Try a different Python version**: The application is designed to work with Python 3.11, but you might try Python 3.9 or 3.10.

## Step 10: Simplify the Application

Try running the application with simpler parameters:

1. Choose the 1D dimension instead of 2D
2. Reduce the number of grid points
3. Select a simpler potential like "Harmonic Oscillator"

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [NumPy Documentation](https://numpy.org/doc/)