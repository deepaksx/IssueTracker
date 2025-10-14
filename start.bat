@echo off
REM IT Issue Tracker - Startup Script
REM This script starts the Flask application

echo ============================================================
echo IT Issue Tracker - Starting Application
echo ============================================================
echo.

REM Check if database exists
if not exist issue_tracker.db (
    echo WARNING: Database not found!
    echo.
    echo Initializing database...
    python init_db.py
    echo.
)

REM Start the Flask application
echo Starting Flask server...
echo.
echo Application will be available at: http://127.0.0.1:5000
echo.
echo SECURITY NOTICE: Default credentials available in README.md
echo Please change default passwords after first login.
echo.
echo Press CTRL+C to stop the server
echo ============================================================
echo.

python app.py

pause
