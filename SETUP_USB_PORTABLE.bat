@echo off
REM ============================================
REM EXPENSE TRACKER - USB PORTABLE SETUP
REM ============================================
REM Run this ONCE on a computer with internet
REM to set up the portable environment
REM ============================================

title Expense Tracker - USB Portable Setup
color 0E

echo.
echo  ============================================
echo   EXPENSE TRACKER - USB PORTABLE SETUP
echo  ============================================
echo.
echo  This script will set up a fully portable
echo  environment that works on ANY Windows PC
echo  without needing Python installed!
echo.
echo  ============================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if Python is available for setup
echo [STEP 1/5] Checking for Python to create portable setup...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python is needed to CREATE the portable setup.
    echo.
    echo  Please install Python temporarily from:
    echo  https://www.python.org/downloads/
    echo.
    echo  After setup is complete, the USB will work
    echo  on any PC WITHOUT Python installed!
    echo.
    pause
    exit /b 1
)
echo       Python found!

REM Create virtual environment
echo [STEP 2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo  ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)
echo       Virtual environment created!

REM Activate and install packages
echo [STEP 3/5] Installing Django and dependencies...
call venv\Scripts\activate.bat
pip install django matplotlib scikit-learn joblib numpy --quiet
if errorlevel 1 (
    echo  ERROR: Failed to install packages!
    pause
    exit /b 1
)
echo       Packages installed!

REM Run migrations
echo [STEP 4/5] Setting up database...
python manage.py migrate --run-syncdb >nul 2>&1
echo       Database ready!

REM Create directories
echo [STEP 5/5] Creating directories...
if not exist "static\charts" mkdir static\charts
echo       Directories created!

echo.
echo  ============================================
echo   SETUP COMPLETE!
echo  ============================================
echo.
echo   Your USB is now fully portable!
echo.
echo   To run on ANY Windows PC:
echo   1. Plug in the USB
echo   2. Double-click "Start Expense Tracker.bat"
echo   3. Browser opens automatically
echo.
echo   NO Python installation needed on target PC!
echo   NO internet needed!
echo   NO admin rights needed!
echo.
echo  ============================================
echo.
pause