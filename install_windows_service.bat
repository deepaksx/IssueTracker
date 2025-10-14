@echo off
REM EFI IT Issue Tracker - Windows Service Installer
REM This script installs the application as a Windows service using NSSM

echo =====================================
echo EFI IT Issue Tracker
echo Windows Service Installation
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
    echo ERROR: NSSM not found in nssm\ directory
    echo.
    echo Please download NSSM from: https://nssm.cc/download
    echo Extract nssm.exe to: %~dp0nssm\
    echo.
    pause
    exit /b 1
)

REM Find Python and Gunicorn paths
for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i
for /f "tokens=*" %%i in ('where gunicorn') do set GUNICORN_PATH=%%i

if "%GUNICORN_PATH%"=="" (
    echo ERROR: Gunicorn not found
    echo Installing Gunicorn...
    pip install gunicorn
    for /f "tokens=*" %%i in ('where gunicorn') do set GUNICORN_PATH=%%i
)

echo.
echo Configuration:
echo --------------
echo Application Path: %~dp0
echo Python: %PYTHON_PATH%
echo Gunicorn: %GUNICORN_PATH%
echo Service Name: EFIIssueTracker
echo.

REM Check if service already exists
sc query EFIIssueTracker >nul 2>&1
if %errorLevel% equ 0 (
    echo Service already exists. Removing old service...
    nssm\nssm.exe stop EFIIssueTracker
    nssm\nssm.exe remove EFIIssueTracker confirm
)

REM Install service
echo Installing service...
nssm\nssm.exe install EFIIssueTracker "%GUNICORN_PATH%" "--bind 0.0.0.0:8000 --workers 4 app:app"

REM Configure service
echo Configuring service...
nssm\nssm.exe set EFIIssueTracker AppDirectory "%~dp0"
nssm\nssm.exe set EFIIssueTracker DisplayName "EFI IT Issue Tracker"
nssm\nssm.exe set EFIIssueTracker Description "Web-based IT issue tracking system for EFI"
nssm\nssm.exe set EFIIssueTracker Start SERVICE_AUTO_START
nssm\nssm.exe set EFIIssueTracker AppStdout "%~dp0logs\service.log"
nssm\nssm.exe set EFIIssueTracker AppStderr "%~dp0logs\service_error.log"
nssm\nssm.exe set EFIIssueTracker AppRotateFiles 1
nssm\nssm.exe set EFIIssueTracker AppRotateOnline 1
nssm\nssm.exe set EFIIssueTracker AppRotateSeconds 86400
nssm\nssm.exe set EFIIssueTracker AppRotateBytes 1048576

REM Create logs directory
if not exist "logs" mkdir logs

REM Configure firewall
echo Configuring Windows Firewall...
netsh advfirewall firewall delete rule name="EFI Issue Tracker" >nul 2>&1
netsh advfirewall firewall add rule name="EFI Issue Tracker" dir=in action=allow protocol=TCP localport=8000

echo.
echo Service installed successfully!
echo.

REM Start service
echo Starting service...
nssm\nssm.exe start EFIIssueTracker

timeout /t 3 >nul

REM Check service status
nssm\nssm.exe status EFIIssueTracker

echo.
echo =====================================
echo Installation Complete!
echo =====================================
echo.
echo Service Name: EFIIssueTracker
echo Status: Running
echo Port: 8000
echo.
echo Access the application at:
echo   http://localhost:8000
echo   http://[YOUR-SERVER-IP]:8000
echo.
echo Service Management Commands:
echo   Start:   nssm start EFIIssueTracker
echo   Stop:    nssm stop EFIIssueTracker
echo   Restart: nssm restart EFIIssueTracker
echo   Status:  nssm status EFIIssueTracker
echo   Logs:    %~dp0logs\service.log
echo.
echo Default Login:
echo   Username: admin
echo   Password: admin123
echo   WARNING: Change this password immediately!
echo.
pause
