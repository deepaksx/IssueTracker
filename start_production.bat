@echo off
REM EFI IT Issue Tracker - Production Startup Script
REM This script starts the application in production mode

echo =====================================
echo EFI IT Issue Tracker - Starting...
echo =====================================
echo.

REM Change to application directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if database exists
if not exist "issue_tracker.db" (
    echo Database not found. Initializing...
    python init_db.py
    if errorlevel 1 (
        echo ERROR: Failed to initialize database
        pause
        exit /b 1
    )
)

REM Create uploads directory if it doesn't exist
if not exist "uploads" mkdir uploads

REM Get server IP address
echo.
echo Server Information:
echo -------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo IP Address: !IP!
)
echo Port: 8000
echo.

REM Start the application
echo Starting server...
echo.
echo Application will be accessible at:
echo   - Local:    http://localhost:8000
echo   - Network:  http://!IP!:8000
echo.
echo Press CTRL+C to stop the server
echo =====================================
echo.

REM Start with gunicorn (production) or Flask (development fallback)
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
if errorlevel 1 (
    echo.
    echo Gunicorn not found, starting with Flask development server...
    echo WARNING: For production use, install gunicorn: pip install gunicorn
    echo.
    set FLASK_ENV=production
    python app.py
)

pause
