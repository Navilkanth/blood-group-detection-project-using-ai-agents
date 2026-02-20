@echo off
setlocal enabledelayedexpansion

echo ================================
echo Backend Test Suite Runner
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt
pip install -q -r requirements-dev.txt

echo Running tests...
python tests/run_tests.py

echo.
echo Tests complete. Coverage report available in htmlcov\index.html

pause
