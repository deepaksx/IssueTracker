# EFI IT Issue Tracker - Internal Network Deployment Guide

This guide will help you deploy the Issue Tracker within your company network, making it accessible to all users on the internal network.

## Table of Contents
1. [Deployment Options](#deployment-options)
2. [Option 1: Windows Server Deployment (Recommended)](#option-1-windows-server-deployment-recommended)
3. [Option 2: Local Server/Desktop Deployment](#option-2-local-serverdesktop-deployment)
4. [Option 3: Docker Deployment](#option-3-docker-deployment)
5. [Network Configuration](#network-configuration)
6. [User Access Setup](#user-access-setup)
7. [Backup and Maintenance](#backup-and-maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Deployment Options

### Recommended Setup
- **Server Type**: Windows Server or dedicated Windows PC
- **Network**: Internal company network
- **Access**: Via IP address or hostname (e.g., http://server-name:8000 or http://192.168.1.100:8000)
- **Users**: All employees on company network

### Requirements
- Windows Server 2016+ or Windows 10/11 PC
- Python 3.11 or higher
- Network access for all users
- Firewall port open (default: 8000)
- Admin access to server

---

## Option 1: Windows Server Deployment (Recommended)

This is the best option for production use in a company network.

### Step 1: Prepare the Server

1. **Select a Server**
   - Dedicated Windows Server or reliable Windows PC
   - Should be always running during business hours
   - Adequate disk space (minimum 10GB recommended)

2. **Create Application Directory**
   ```powershell
   # Create directory on C: drive
   cd C:\
   mkdir IssueTracker
   cd IssueTracker
   ```

3. **Clone the Repository**
   ```powershell
   # If Git is installed
   git clone https://github.com/deepaksx/IssueTracker.git .

   # OR download as ZIP from GitHub and extract
   ```

### Step 2: Install Python and Dependencies

1. **Install Python 3.11**
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Install for all users

2. **Verify Installation**
   ```powershell
   python --version
   # Should show: Python 3.11.x or higher
   ```

3. **Install Dependencies**
   ```powershell
   cd C:\IssueTracker
   pip install -r requirements.txt
   ```

### Step 3: Configure the Application

1. **Create Configuration File**
   ```powershell
   copy .env.example .env
   notepad .env
   ```

2. **Edit .env File**
   ```env
   FLASK_ENV=production
   SECRET_KEY=your-company-secret-key-here
   DATABASE_PATH=C:\IssueTracker\issue_tracker.db
   UPLOAD_FOLDER=C:\IssueTracker\uploads
   SESSION_COOKIE_SECURE=False
   ```

   **Generate SECRET_KEY:**
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Initialize Database**
   ```powershell
   python init_db.py
   ```

### Step 4: Configure Windows Firewall

1. **Open Windows Firewall Settings**
   - Search for "Windows Defender Firewall"
   - Click "Advanced settings"

2. **Create Inbound Rule**
   - Click "Inbound Rules" → "New Rule"
   - Rule Type: **Port**
   - Protocol: **TCP**
   - Specific local ports: **8000**
   - Action: **Allow the connection**
   - Profile: Check **Domain** and **Private**
   - Name: **EFI Issue Tracker**

   **Or use PowerShell (Run as Administrator):**
   ```powershell
   New-NetFirewallRule -DisplayName "EFI Issue Tracker" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

### Step 5: Run as Windows Service

#### Method A: Using NSSM (Recommended)

1. **Download NSSM**
   - Download from [nssm.cc](https://nssm.cc/download)
   - Extract to `C:\IssueTracker\nssm`

2. **Install Service**
   ```powershell
   # Run as Administrator
   cd C:\IssueTracker\nssm

   .\nssm.exe install EFIIssueTracker
   ```

3. **Configure Service in NSSM GUI**
   - **Path**: `C:\Python311\Scripts\gunicorn.exe`
   - **Startup directory**: `C:\IssueTracker`
   - **Arguments**: `--bind 0.0.0.0:8000 --workers 4 app:app`
   - **Service name**: `EFIIssueTracker`
   - Click "Install service"

4. **Start Service**
   ```powershell
   nssm start EFIIssueTracker
   ```

5. **Verify Service**
   ```powershell
   nssm status EFIIssueTracker
   ```

#### Method B: Using Task Scheduler

1. **Create Start Script**
   Create `C:\IssueTracker\start_production.bat`:
   ```batch
   @echo off
   cd C:\IssueTracker
   C:\Python311\Scripts\gunicorn.exe --bind 0.0.0.0:8000 --workers 4 app:app
   ```

2. **Open Task Scheduler**
   - Search for "Task Scheduler"
   - Click "Create Task"

3. **Configure Task**
   - **General Tab:**
     - Name: `EFI Issue Tracker`
     - Run whether user is logged on or not
     - Run with highest privileges

   - **Triggers Tab:**
     - New → At startup

   - **Actions Tab:**
     - New → Start a program
     - Program: `C:\IssueTracker\start_production.bat`

   - **Settings Tab:**
     - ✅ Allow task to be run on demand
     - ✅ If task fails, restart every: 1 minute

4. **Start Task Manually First Time**
   - Right-click task → Run

### Step 6: Get Server Network Information

```powershell
# Get server IP address
ipconfig

# Look for "IPv4 Address" under your network adapter
# Example: 192.168.1.100

# Get server hostname
hostname
# Example: EFI-SERVER-01
```

### Step 7: Test Access

1. **Test Locally on Server**
   - Open browser: `http://localhost:8000`
   - Should see login page

2. **Test from Another Computer**
   - Open browser: `http://[SERVER-IP]:8000`
   - Example: `http://192.168.1.100:8000`
   - Should see login page

3. **Login with Default Credentials**
   - Username: `admin`
   - Password: `admin123`
   - ⚠️ **Change immediately after first login!**

### Step 8: Set Up Static IP (Recommended)

To ensure the server always has the same IP address:

1. **Open Network Settings**
   - Control Panel → Network and Sharing Center
   - Change adapter settings
   - Right-click network adapter → Properties
   - Select "Internet Protocol Version 4 (TCP/IPv4)"

2. **Configure Static IP**
   - Select "Use the following IP address"
   - IP address: (e.g., 192.168.1.100)
   - Subnet mask: (e.g., 255.255.255.0)
   - Default gateway: (your router IP, e.g., 192.168.1.1)
   - DNS servers: (your company DNS or 8.8.8.8)

---

## Option 2: Local Server/Desktop Deployment

For quick setup or testing with a local PC.

### Quick Setup

1. **Install Application**
   ```batch
   cd C:\
   git clone https://github.com/deepaksx/IssueTracker.git
   cd IssueTracker
   pip install -r requirements.txt
   python init_db.py
   ```

2. **Create Startup Script**
   Create `C:\IssueTracker\start_server.bat`:
   ```batch
   @echo off
   echo Starting EFI Issue Tracker...
   cd C:\IssueTracker
   gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
   pause
   ```

3. **Configure Auto-Start**
   - Press `Win + R`
   - Type: `shell:startup`
   - Create shortcut to `start_server.bat` in startup folder

4. **Open Firewall Port** (see Step 4 above)

5. **Share IP Address with Users**
   - Get IP: `ipconfig`
   - Share URL: `http://[YOUR-IP]:8000`

---

## Option 3: Docker Deployment

For advanced users or containerized environments.

### Step 1: Create Dockerfile

Create `C:\IssueTracker\Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Initialize database and start application
CMD python init_db.py && gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  issuetracker:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    restart: unless-stopped
```

### Step 3: Deploy

```bash
docker-compose up -d
```

---

## Network Configuration

### DNS Configuration (Optional but Recommended)

Instead of using IP addresses, set up a friendly hostname:

1. **Contact IT/Network Admin**
   - Request DNS entry
   - Example: `issuetracker.efi.local` → `192.168.1.100`

2. **Or Use hosts File (Each Client)**
   - Edit `C:\Windows\System32\drivers\etc\hosts`
   - Add line: `192.168.1.100 issuetracker.efi.local`
   - Users can access via: `http://issuetracker.efi.local:8000`

### Reverse Proxy with IIS (Advanced)

For removing port number from URL:

1. **Install IIS**
   - Server Manager → Add Roles → Web Server (IIS)

2. **Install URL Rewrite Module**
   - Download from Microsoft

3. **Configure Reverse Proxy**
   - Point IIS site to localhost:8000
   - Users access via: `http://server-name`

---

## User Access Setup

### Share with Employees

**Option 1: Email Announcement**
```
Subject: New IT Issue Tracker Available

Dear Team,

We've launched a new IT Issue Tracker system for logging and tracking IT issues.

Access URL: http://192.168.1.100:8000
(Bookmark this link for easy access)

Default Login:
- Username: Your assigned username
- Password: Provided separately

Features:
- Submit and track IT issues
- View issue status and history
- Upload supporting documents

For assistance, contact IT Support.
```

**Option 2: Intranet Portal**
- Add link to company intranet
- Create desktop shortcut for common workstations

**Option 3: Active Directory Integration**
- Create login script to add browser favorite
- Deploy shortcut via Group Policy

### Create User Accounts

**Via Web Interface:**
1. Login as admin
2. Go to "Users" menu
3. Click "Add User"
4. Create accounts for each employee

**Via Command Line:**
```powershell
cd C:\IssueTracker
python manage_users_cli.py
# Choose option 2 to create users
```

---

## Backup and Maintenance

### Automated Backup Script

Create `C:\IssueTracker\backup.bat`:
```batch
@echo off
SET BACKUP_DIR=C:\IssueTracker\Backups
SET DATE=%DATE:~-4%%DATE:~4,2%%DATE:~7,2%

:: Create backup directory
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Backup database
copy "C:\IssueTracker\issue_tracker.db" "%BACKUP_DIR%\issue_tracker_%DATE%.db"

:: Backup uploads folder
xcopy "C:\IssueTracker\uploads" "%BACKUP_DIR%\uploads_%DATE%\" /E /I /Y

:: Delete backups older than 30 days
forfiles /p "%BACKUP_DIR%" /s /m *.db /d -30 /c "cmd /c del @path"

echo Backup completed: %DATE%
```

### Schedule Backups

1. **Open Task Scheduler**
2. **Create Task**
   - Trigger: Daily at 2:00 AM
   - Action: Run `C:\IssueTracker\backup.bat`

### Manual Backup

```powershell
# Stop service first
nssm stop EFIIssueTracker

# Backup files
copy C:\IssueTracker\issue_tracker.db C:\Backups\issue_tracker_backup.db
xcopy C:\IssueTracker\uploads C:\Backups\uploads\ /E /I

# Restart service
nssm start EFIIssueTracker
```

### Update Application

```powershell
# Stop service
nssm stop EFIIssueTracker

# Backup current version
xcopy C:\IssueTracker C:\IssueTracker_backup\ /E /I

# Pull updates
cd C:\IssueTracker
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Restart service
nssm start EFIIssueTracker
```

---

## Troubleshooting

### Service Won't Start

**Check Python Path:**
```powershell
where python
where gunicorn
```

**Check Service Logs:**
```powershell
nssm status EFIIssueTracker
# Check Windows Event Viewer → Application logs
```

**Test Manually:**
```powershell
cd C:\IssueTracker
gunicorn --bind 0.0.0.0:8000 app:app
# Look for error messages
```

### Cannot Access from Other Computers

**1. Check Firewall:**
```powershell
# Test if port is open
Test-NetConnection -ComputerName [SERVER-IP] -Port 8000
```

**2. Check Service is Running:**
```powershell
netstat -an | findstr :8000
# Should show LISTENING
```

**3. Check Server IP:**
```powershell
ipconfig
# Ensure using correct IP address
```

**4. Try Disabling Firewall Temporarily:**
```powershell
# For testing only - DO NOT leave disabled
netsh advfirewall set allprofiles state off
```

### Database Locked Error

**Solution:**
```powershell
# Stop all instances
nssm stop EFIIssueTracker
taskkill /F /IM python.exe
taskkill /F /IM gunicorn.exe

# Restart
nssm start EFIIssueTracker
```

### High Memory Usage

**Reduce Workers:**
Edit service configuration:
```powershell
# Reduce from 4 to 2 workers
nssm set EFIIssueTracker AppParameters "--bind 0.0.0.0:8000 --workers 2 app:app"
nssm restart EFIIssueTracker
```

---

## Security Considerations for Internal Network

### 1. Change Default Credentials
```powershell
# After first login, immediately:
# - Change admin password
# - Create individual user accounts
# - Delete or disable default viewer account
```

### 2. Regular Updates
```powershell
# Schedule monthly checks
cd C:\IssueTracker
git fetch
git status
```

### 3. Access Control
- Create individual accounts for each user
- Use domain usernames for accountability
- Regularly review user access logs

### 4. Backup Strategy
- Daily automated backups
- Test restore procedure quarterly
- Keep 30 days of backup history

### 5. Monitoring
- Check service status daily
- Review audit logs weekly
- Monitor disk space

---

## Network Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│           Company Internal Network              │
│                                                 │
│  ┌──────────────┐         ┌──────────────┐    │
│  │ User PC #1   │         │ User PC #2   │    │
│  │ Browser      │         │ Browser      │    │
│  └──────┬───────┘         └──────┬───────┘    │
│         │                        │             │
│         └────────┬───────────────┘             │
│                  │                             │
│         ┌────────▼─────────┐                  │
│         │  Network Switch   │                  │
│         └────────┬──────────┘                  │
│                  │                             │
│         ┌────────▼──────────────┐             │
│         │  Windows Server        │             │
│         │  192.168.1.100:8000   │             │
│         │                        │             │
│         │  - Python/Flask       │             │
│         │  - Gunicorn           │             │
│         │  - SQLite Database    │             │
│         │  - PDF Uploads        │             │
│         └────────────────────────┘             │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Quick Reference

### Service Commands
```powershell
# Start service
nssm start EFIIssueTracker

# Stop service
nssm stop EFIIssueTracker

# Restart service
nssm restart EFIIssueTracker

# Check status
nssm status EFIIssueTracker

# View service logs
nssm tail EFIIssueTracker
```

### Useful URLs
- **Application**: `http://[SERVER-IP]:8000`
- **Login**: `http://[SERVER-IP]:8000/login`
- **Dashboard**: `http://[SERVER-IP]:8000/dashboard`

### Default Credentials
- **Admin**: admin / admin123 (⚠️ Change immediately!)

---

## Support Checklist

When helping users:
- [ ] Can they ping the server?
- [ ] Is the service running?
- [ ] Is firewall port open?
- [ ] Are they using correct URL?
- [ ] Have they cleared browser cache?
- [ ] Are credentials correct?

---

**For questions or issues, contact your IT department.**

---

Copyright © 2025 EFI IT - Internal Use Only
