@echo off
REM Batch file to run the Streamlit application with warning filtering
REM This script redirects the output through a filter that removes the ScriptRunContext warnings

echo Starting Streamlit application with warning filtering...

REM Run the Streamlit application and pipe its output through findstr to filter out warnings
python -m streamlit run streamlit_app.py 2>&1 | findstr /V "missing ScriptRunContext"

echo Streamlit application has been stopped.