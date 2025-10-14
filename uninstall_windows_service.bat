@echo off
REM EFI IT Issue Tracker - Windows Service Uninstaller

echo =====================================
echo EFI IT Issue Tracker
echo Windows Service Uninstallation
echo =====================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Change to application directory
cd /d "%~dp0"

REM Check if NSSM exists
if not exist "nssm\nssm.exe" (
    echo ERROR: NSSM not found
    echo Service may have been installed with NSSM, but nssm.exe is missing
    echo.
    echo You can manually remove the service with:
    echo sc delete EFIIssueTracker
    echo.
    pause
    exit /b 1
)

REM Check if service exists
sc query EFIIssueTracker >nul 2>&1
if %errorLevel% neq 0 (
    echo Service 'EFIIssueTracker' not found
    echo Nothing to uninstall
    pause
    exit /b 0
)

echo Stopping service...
nssm\nssm.exe stop EFIIssueTracker

echo Removing service...
nssm\nssm.exe remove EFIIssueTracker confirm

echo Removing firewall rule...
netsh advfirewall firewall delete rule name="EFI Issue Tracker"

echo.
echo =====================================
echo Service Uninstalled Successfully
echo =====================================
echo.
echo The application files have NOT been deleted.
echo Database and uploads are still intact.
echo.
echo To completely remove the application:
echo 1. Delete this directory: %~dp0
echo 2. Remove any scheduled backup tasks
echo.
pause
