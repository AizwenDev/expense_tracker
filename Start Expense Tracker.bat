@echo off
REM ============================================
REM EXPENSE TRACKER - PORTABLE LAUNCHER
REM ============================================
REM Just double-click to run!
REM Works on ANY Windows PC - No Python needed!
REM ============================================

title Expense Tracker

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo.
    echo  ERROR: Portable environment not set up!
    echo.
    echo  Please run "SETUP_USB_PORTABLE.bat" first
    echo  on a computer with Python installed.
    echo.
    pause
    exit /b 1
)

REM Create charts directory if not exists
if not exist "static\charts" mkdir static\charts

echo.
echo  ============================================
echo   EXPENSE TRACKER WITH AI PREDICTION
echo  ============================================
echo.
echo   Starting server...
echo.
echo   Open your browser to:
echo.
echo      http://127.0.0.1:8000
echo.
echo   Press Ctrl+C to stop.
echo  ============================================
echo.

REM Open browser
start "" "http://127.0.0.1:8000"

REM Activate venv and run server
call venv\Scripts\activate.bat
python manage.py runserver 127.0.0.1:8000

echo.
echo  Server stopped.
pause