@echo off
REM EFI IT Issue Tracker - Backup Script
REM Creates timestamped backups of database and uploads

setlocal enabledelayedexpansion

REM Configuration
SET APP_DIR=%~dp0
SET BACKUP_DIR=%APP_DIR%Backups
SET DATE_STAMP=%DATE:~-4%%DATE:~4,2%%DATE:~7,2%
SET TIME_STAMP=%TIME:~0,2%%TIME:~3,2%
SET TIME_STAMP=%TIME_STAMP: =0%
SET BACKUP_NAME=backup_%DATE_STAMP%_%TIME_STAMP%

echo =====================================
echo EFI IT Issue Tracker - Backup
echo =====================================
echo.
echo Backup Location: %BACKUP_DIR%\%BACKUP_NAME%
echo Starting backup at %DATE% %TIME%
echo.

REM Create backup directory structure
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if not exist "%BACKUP_DIR%\%BACKUP_NAME%" mkdir "%BACKUP_DIR%\%BACKUP_NAME%"

REM Stop service if running
echo Checking if service is running...
sc query EFIIssueTracker | find "RUNNING" >nul 2>&1
if %errorLevel% equ 0 (
    echo Stopping service for safe backup...
    if exist "nssm\nssm.exe" (
        nssm\nssm.exe stop EFIIssueTracker
    ) else (
        sc stop EFIIssueTracker
    )
    timeout /t 3 >nul
    set SERVICE_WAS_RUNNING=1
) else (
    echo Service is not running
    set SERVICE_WAS_RUNNING=0
)

REM Backup database
echo.
echo [1/3] Backing up database...
if exist "%APP_DIR%issue_tracker.db" (
    copy "%APP_DIR%issue_tracker.db" "%BACKUP_DIR%\%BACKUP_NAME%\issue_tracker.db" >nul
    if errorlevel 1 (
        echo ERROR: Failed to backup database
    ) else (
        echo Database backed up successfully
    )
) else (
    echo WARNING: Database file not found
)

REM Backup uploads folder
echo.
echo [2/3] Backing up uploads...
if exist "%APP_DIR%uploads" (
    xcopy "%APP_DIR%uploads" "%BACKUP_DIR%\%BACKUP_NAME%\uploads\" /E /I /Y >nul
    if errorlevel 1 (
        echo ERROR: Failed to backup uploads
    ) else (
        echo Uploads backed up successfully
    )
) else (
    echo WARNING: Uploads folder not found
)

REM Backup configuration
echo.
echo [3/3] Backing up configuration...
if exist "%APP_DIR%.env" (
    copy "%APP_DIR%.env" "%BACKUP_DIR%\%BACKUP_NAME%\.env" >nul
    echo Configuration backed up successfully
)

REM Create backup info file
echo Backup Information > "%BACKUP_DIR%\%BACKUP_NAME%\backup_info.txt"
echo. >> "%BACKUP_DIR%\%BACKUP_NAME%\backup_info.txt"
echo Date: %DATE% >> "%BACKUP_DIR%\%BACKUP_NAME%\backup_info.txt"
echo Time: %TIME% >> "%BACKUP_DIR%\%BACKUP_NAME%\backup_info.txt"
echo Location: %BACKUP_DIR%\%BACKUP_NAME% >> "%BACKUP_DIR%\%BACKUP_NAME%\backup_info.txt"

REM Restart service if it was running
if %SERVICE_WAS_RUNNING% equ 1 (
    echo.
    echo Restarting service...
    if exist "nssm\nssm.exe" (
        nssm\nssm.exe start EFIIssueTracker
    ) else (
        sc start EFIIssueTracker
    )
)

REM Calculate backup size
for /f "tokens=3" %%a in ('dir "%BACKUP_DIR%\%BACKUP_NAME%" /s /-c ^| find "bytes"') do set BACKUP_SIZE=%%a

echo.
echo =====================================
echo Backup Complete!
echo =====================================
echo.
echo Backup Name: %BACKUP_NAME%
echo Location: %BACKUP_DIR%\%BACKUP_NAME%
echo Size: %BACKUP_SIZE% bytes
echo.

REM Cleanup old backups (keep last 30 days)
echo Cleaning up old backups (older than 30 days)...
forfiles /p "%BACKUP_DIR%" /m backup_* /d -30 /c "cmd /c if @isdir==TRUE rmdir /s /q @path" 2>nul
if errorlevel 1 (
    echo No old backups to clean up
) else (
    echo Old backups cleaned up
)

echo.
echo To restore from this backup:
echo 1. Stop the service
echo 2. Copy files from backup folder to application folder
echo 3. Restart the service
echo.

endlocal
