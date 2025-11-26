@echo off
REM ============================================
REM EXPENSE TRACKER - PORTABLE LAUNCHER
REM ============================================
REM This script runs the Expense Tracker from a USB drive
REM No installation required - just double-click to run!
REM ============================================

title Expense Tracker - Portable Launcher
color 0A

echo.
echo  ============================================
echo   EXPENSE TRACKER WITH AI PREDICTION
echo   Portable Django Application
echo  ============================================
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
echo [1/6] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python is not installed or not in PATH!
    echo.
    echo  Please install Python from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
echo       Python found!

REM Check if virtual environment exists, create if not
echo [2/6] Setting up virtual environment...
if not exist "venv" (
    echo       Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo  ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)
echo       Virtual environment ready!

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo  ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo       Virtual environment activated!

REM Install requirements
echo [4/6] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  WARNING: Some dependencies may not have installed correctly.
    echo  The application may still work with existing packages.
)
echo       Dependencies installed!

REM Run migrations
echo [5/6] Setting up database...
python manage.py migrate --run-syncdb >nul 2>&1
if errorlevel 1 (
    echo  WARNING: Database migration had issues.
    echo  Trying to continue anyway...
)
echo       Database ready!

REM Create static directories if they don't exist
if not exist "static\charts" mkdir static\charts

echo [6/6] Starting server...
echo.
echo  ============================================
echo   SERVER STARTING!
echo  ============================================
echo.
echo   Open your browser and go to:
echo.
echo      http://127.0.0.1:8000
echo.
echo   Press Ctrl+C to stop the server.
echo  ============================================
echo.

REM Open browser after a short delay
start "" "http://127.0.0.1:8000"

REM Start the Django development server
python manage.py runserver 127.0.0.1:8000

REM Deactivate virtual environment when done
call venv\Scripts\deactivate.bat 2>nul

echo.
echo  Server stopped. Goodbye!
pause