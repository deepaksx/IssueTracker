# Quick Start Guide - Internal Network Deployment

## For IT Administrators

This guide will get your Issue Tracker running on your company network in **under 30 minutes**.

---

## Prerequisites

- [ ] Windows Server or Windows 10/11 PC (will act as server)
- [ ] Python 3.11+ installed
- [ ] Network access from all user computers
- [ ] Administrator rights on server

---

## Step-by-Step Setup

### Step 1: Download and Extract (2 minutes)

1. Download the application:
   ```powershell
   cd C:\
   git clone https://github.com/deepaksx/IssueTracker.git
   ```

   **Or** download ZIP from GitHub and extract to `C:\IssueTracker`

### Step 2: Install Dependencies (5 minutes)

```powershell
cd C:\IssueTracker
pip install -r requirements.txt
```

### Step 3: Initialize Database (1 minute)

```powershell
python init_db.py
```

This creates the database with default admin account.

### Step 4: Install as Windows Service (5 minutes)

1. Download NSSM:
   - Go to https://nssm.cc/download
   - Extract `nssm.exe` to `C:\IssueTracker\nssm\`

2. Run installer as Administrator:
   ```powershell
   Right-click: install_windows_service.bat → Run as administrator
   ```

3. The script will:
   - ✅ Install Windows service
   - ✅ Configure firewall
   - ✅ Start the application
   - ✅ Display server URL

### Step 5: Get Server Information (1 minute)

```powershell
ipconfig
```

Look for "IPv4 Address" (example: `192.168.1.100`)

### Step 6: Test Access (2 minutes)

1. **On the server:**
   - Open browser: `http://localhost:8000`
   - You should see the login page

2. **From another computer:**
   - Open browser: `http://[SERVER-IP]:8000`
   - Example: `http://192.168.1.100:8000`
   - You should see the login page

3. **Login:**
   - Username: `admin`
   - Password: `admin123`
   - ⚠️ **Change immediately!**

---

## Share with Employees

### Email Template

```
Subject: New IT Issue Tracker System

Dear Team,

We have launched a new IT Issue Tracker system.

🌐 Access URL: http://192.168.1.100:8000
📱 Bookmark this link for easy access

📋 Your credentials will be provided separately.

Features:
• Submit IT issues
• Track issue status
• View history
• Upload documents

Questions? Contact IT Support.
```

---

## Create User Accounts (5 minutes)

### Method 1: Web Interface (Recommended)

1. Login as admin
2. Click "Users" in menu
3. Click "Add User"
4. Fill in details:
   - Username (use employee name or email)
   - Password (temporary - user should change)
   - Role (Admin or User)
5. Repeat for each employee

### Method 2: Command Line (Faster for bulk)

```powershell
cd C:\IssueTracker
python manage_users_cli.py
```

Choose option 2 (Create user) and enter details for each employee.

---

## Daily Operations

### Start/Stop Service

```powershell
# Start
nssm start EFIIssueTracker

# Stop
nssm stop EFIIssueTracker

# Restart
nssm restart EFIIssueTracker

# Check status
nssm status EFIIssueTracker
```

### View Logs

```powershell
# Service logs
type C:\IssueTracker\logs\service.log

# Error logs
type C:\IssueTracker\logs\service_error.log
```

### Backup Database

```powershell
# Manual backup
C:\IssueTracker\backup.bat

# Or copy manually
copy C:\IssueTracker\issue_tracker.db C:\Backups\
```

### Schedule Automatic Backups

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2:00 AM
4. Action: Start a program
5. Program: `C:\IssueTracker\backup.bat`
6. Finish

---

## Troubleshooting

### Cannot access from other computers

1. **Check service is running:**
   ```powershell
   nssm status EFIIssueTracker
   ```

2. **Check firewall:**
   ```powershell
   netsh advfirewall firewall show rule name="EFI Issue Tracker"
   ```

   If not found:
   ```powershell
   netsh advfirewall firewall add rule name="EFI Issue Tracker" dir=in action=allow protocol=TCP localport=8000
   ```

3. **Verify port is listening:**
   ```powershell
   netstat -an | findstr :8000
   ```
   Should show: `0.0.0.0:8000  LISTENING`

4. **Test from client:**
   ```powershell
   Test-NetConnection -ComputerName [SERVER-IP] -Port 8000
   ```

### Service won't start

1. **Check if port is in use:**
   ```powershell
   netstat -ano | findstr :8000
   ```

2. **Restart service:**
   ```powershell
   nssm restart EFIIssueTracker
   ```

3. **Check error logs:**
   ```powershell
   type C:\IssueTracker\logs\service_error.log
   ```

### Users can't login

1. **Verify account exists:**
   ```powershell
   python manage_users_cli.py
   # Choose option 1 to list all users
   ```

2. **Reset password:**
   ```powershell
   python manage_users_cli.py
   # Choose option 4 to change password
   ```

---

## Maintenance Checklist

### Daily
- [ ] Verify service is running
- [ ] Check application is accessible

### Weekly
- [ ] Review audit logs for any issues
- [ ] Check disk space

### Monthly
- [ ] Test backup restoration
- [ ] Review user accounts
- [ ] Update application if new version available

---

## Security Best Practices

1. **Change default admin password immediately**
2. **Create individual user accounts** (don't share admin)
3. **Set up daily automated backups**
4. **Keep server physically secure**
5. **Update regularly** (check GitHub for updates)
6. **Review audit logs** for suspicious activity

---

## Getting Help

### Check Logs First
```powershell
# Service logs
type C:\IssueTracker\logs\service.log

# Application logs
type C:\IssueTracker\logs\service_error.log
```

### Common Solutions
- **Restart service:** `nssm restart EFIIssueTracker`
- **Check firewall:** See troubleshooting section above
- **Database locked:** Stop service, restart
- **Users can't access:** Verify IP address hasn't changed

### Documentation
- **Full Internal Guide:** [INTERNAL_DEPLOYMENT.md](INTERNAL_DEPLOYMENT.md)
- **Cloud Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **User Manual:** [README.md](README.md)

### Support
- **GitHub Issues:** https://github.com/deepaksx/IssueTracker/issues
- **Email:** Your IT department

---

## Success Checklist

After setup, verify:

- [ ] Service is installed and running
- [ ] Firewall port 8000 is open
- [ ] Can access from server: `http://localhost:8000`
- [ ] Can access from client: `http://[server-ip]:8000`
- [ ] Admin login works
- [ ] Created user accounts for team
- [ ] Changed default admin password
- [ ] Set up automated backups
- [ ] Shared URL with employees
- [ ] Bookmarked management commands

---

🎉 **Congratulations!** Your Issue Tracker is now live on your company network!

Users can now:
- Access via: `http://[your-server-ip]:8000`
- Login with their credentials
- Submit and track IT issues
- Upload documents
- View issue history

---

**Need more detailed instructions?** See [INTERNAL_DEPLOYMENT.md](INTERNAL_DEPLOYMENT.md)
