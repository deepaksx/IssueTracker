@echo off
REM IT Issue Tracker - Database Migration Script
REM This script adds company, department, and application fields to existing database

echo ============================================================
echo IT Issue Tracker - Database Migration
echo ============================================================
echo.
echo This script will add new fields to your existing database:
echo   - Company
echo   - Department
echo   - Application
echo.
echo Your existing data will be preserved.
echo.

pause

echo.
echo Running migration...
echo.

python migrate_db.py

echo.

if errorlevel 1 (
    echo.
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Migration completed successfully!
echo ============================================================
echo.
echo You can now restart the application and use the new fields.
echo.

pause
