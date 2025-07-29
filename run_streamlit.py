"""
Wrapper script to run the Streamlit application with suppressed warnings.

This script configures the logging module to filter out specific warnings
before launching the Streamlit application.
"""

import os
import sys
import logging
import subprocess

# Configure logging to filter out the "missing ScriptRunContext" warning
class WarningFilter(logging.Filter):
    def filter(self, record):
        # Return False to filter out messages containing "missing ScriptRunContext"
        return "missing ScriptRunContext" not in record.getMessage()

# Apply the filter to the root logger
root_logger = logging.getLogger()
root_logger.addFilter(WarningFilter())

# Set the logging level to INFO to suppress less important messages
logging.basicConfig(level=logging.INFO)

# Get the path to the streamlit_app.py file
script_dir = os.path.dirname(os.path.abspath(__file__))
streamlit_app_path = os.path.join(script_dir, "streamlit_app.py")

# Run the Streamlit application
if __name__ == "__main__":
    # Prepare the command to run Streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", streamlit_app_path]
    
    # Add any additional command-line arguments
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    # Print a message to indicate we're starting Streamlit
    print(f"Starting Streamlit application: {' '.join(cmd)}")
    
    try:
        # Run Streamlit as a subprocess
        process = subprocess.run(cmd)
        sys.exit(process.returncode)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nStreamlit application stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)