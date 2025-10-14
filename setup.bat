@echo off
REM IT Issue Tracker - Setup Script
REM This script installs dependencies and initializes the database

echo ============================================================
echo IT Issue Tracker - Setup and Installation
echo ============================================================
echo.

echo Step 1: Installing Python dependencies...
echo.
pip install -r requirements.txt
echo.

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Please make sure Python and pip are installed correctly.
    pause
    exit /b 1
)

echo ============================================================
echo Step 2: Initializing database...
echo.
python init_db.py
echo.

if errorlevel 1 (
    echo.
    echo ERROR: Failed to initialize database!
    pause
    exit /b 1
)

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo You can now start the application by running: start.bat
echo Or manually with: python app.py
echo.
echo The application will be available at: http://127.0.0.1:5000
echo.
echo IMPORTANT SECURITY NOTICE:
echo Default users have been created with standard credentials.
echo Please refer to README.md for initial login information.
echo Change all default passwords immediately after first login!
echo ============================================================
echo.

pause
