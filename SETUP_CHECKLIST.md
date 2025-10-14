# Setup Checklist - Print This Page!

**For:** EFI IT Issue Tracker Installation
**Time:** 30-45 minutes
**Difficulty:** Easy

---

## Before You Start

**What you need:**

- [ ] Windows computer (server or desktop PC)
- [ ] Administrator password
- [ ] Internet connection
- [ ] 30-45 minutes of time

**Write down your server's IP address here:**

```
Server IP: ___.___.___.___ : 8000
Example:   192.168.1.100:8000
```

---

## Part 1: Install Python ⏱️ 10 minutes

- [ ] Go to https://www.python.org/downloads/
- [ ] Download Python 3.11
- [ ] Run the installer
- [ ] ⚠️ CHECK BOTH BOXES at bottom:
  - [ ] "Install launcher for all users"
  - [ ] "Add Python 3.11 to PATH"
- [ ] Click "Install Now"
- [ ] Wait for installation
- [ ] Test: Open Command Prompt, type `python --version`
- [ ] Should see: Python 3.11.x ✅

**Status:** ☐ Complete

---

## Part 2: Download Application ⏱️ 5 minutes

- [ ] Go to https://github.com/deepaksx/IssueTracker
- [ ] Click green "Code" button
- [ ] Click "Download ZIP"
- [ ] Extract to C:\IssueTracker

**Result:** Folder exists at C:\IssueTracker ✅

**Status:** ☐ Complete

---

## Part 3: Install Requirements ⏱️ 5 minutes

- [ ] Open Command Prompt
- [ ] Type: `cd C:\IssueTracker`
- [ ] Type: `pip install -r requirements.txt`
- [ ] Wait 2-3 minutes
- [ ] Installation completes (no errors)

**Status:** ☐ Complete

---

## Part 4: Create Database ⏱️ 2 minutes

- [ ] In Command Prompt, type: `python init_db.py`
- [ ] See message: "Database initialized successfully"
- [ ] See message: "Default users created"

**Status:** ☐ Complete

---

## Part 5: Download NSSM ⏱️ 5 minutes

- [ ] Go to https://nssm.cc/download
- [ ] Download nssm
- [ ] Extract the ZIP file
- [ ] Open win64 folder (or win32 for old systems)
- [ ] Copy nssm.exe
- [ ] Create folder: C:\IssueTracker\nssm
- [ ] Paste nssm.exe into that folder

**Result:** File exists at C:\IssueTracker\nssm\nssm.exe ✅

**Status:** ☐ Complete

---

## Part 6: Install as Service ⏱️ 5 minutes

- [ ] Go to C:\IssueTracker
- [ ] Find: install_windows_service.bat
- [ ] Right-click → "Run as administrator"
- [ ] Click "Yes" on security warning
- [ ] Wait for installation
- [ ] See: "Installation Complete!"
- [ ] **Write down the IP address shown:**

```
IP Address: ___.___.___.___ : 8000
```

**Status:** ☐ Complete

---

## Part 7: Test Application ⏱️ 3 minutes

### Test on Server

- [ ] Open web browser
- [ ] Go to: http://localhost:8000
- [ ] See login page ✅

### Test from Another Computer

- [ ] Go to different computer
- [ ] Open browser
- [ ] Go to: http://[YOUR-IP]:8000
- [ ] See login page ✅

### Test Login

- [ ] Username: admin
- [ ] Password: admin123
- [ ] Click Login
- [ ] See dashboard ✅

**Status:** ☐ Complete

---

## Part 8: Security Setup ⏱️ 5 minutes

### Change Admin Password

- [ ] Go to "Users" menu
- [ ] Click edit on "admin"
- [ ] Enter NEW password
- [ ] Confirm password
- [ ] Click "Update User"

**Write your new admin password here (keep safe!):**

```
New Admin Password: _______________
```

**Status:** ☐ Complete

---

## Part 9: Create User Accounts ⏱️ 10 minutes

For each employee:

**Employee 1:**
- [ ] Click "Users" → "Add User"
- [ ] Username: _____________
- [ ] Password: _____________
- [ ] Role: User
- [ ] Click "Create User"

**Employee 2:**
- [ ] Click "Users" → "Add User"
- [ ] Username: _____________
- [ ] Password: _____________
- [ ] Role: User
- [ ] Click "Create User"

**Employee 3:**
- [ ] Click "Users" → "Add User"
- [ ] Username: _____________
- [ ] Password: _____________
- [ ] Role: User
- [ ] Click "Create User"

*Continue for all employees...*

**Status:** ☐ Complete

---

## Part 10: Email Employees ⏱️ 5 minutes

- [ ] Copy email template (below)
- [ ] Fill in YOUR-SERVER-IP
- [ ] Fill in each employee's username/password
- [ ] Send to all employees

**Email Template:**

```
Subject: New IT Issue Tracker - Access Information

Dear [Employee Name],

We have a new system for reporting IT issues.

ACCESS:
Go to: http://[YOUR-SERVER-IP]:8000

YOUR LOGIN:
Username: [their username]
Password: [temporary password]
Please change this after first login.

HOW TO USE:
1. Login
2. Click "Add Issue"
3. Describe your problem
4. Click "Create Issue"

Questions? Contact IT Support.
```

**Status:** ☐ Complete

---

## Part 11: Setup Backups ⏱️ 5 minutes

- [ ] Click Start → Type "Task Scheduler"
- [ ] Click "Create Basic Task..."
- [ ] Name: EFI Issue Tracker Backup
- [ ] Trigger: Daily
- [ ] Time: 2:00 AM
- [ ] Action: Start a program
- [ ] Program: C:\IssueTracker\backup.bat
- [ ] Check "Open properties dialog"
- [ ] Check "Run whether user is logged on or not"
- [ ] Check "Run with highest privileges"
- [ ] Click OK

**Status:** ☐ Complete

---

## ✅ FINAL CHECKLIST

- [ ] Python installed
- [ ] Application downloaded to C:\IssueTracker
- [ ] Requirements installed
- [ ] Database created
- [ ] NSSM downloaded
- [ ] Service installed and running
- [ ] Can access from server (localhost:8000)
- [ ] Can access from other computers
- [ ] Can login as admin
- [ ] Changed admin password
- [ ] Created user accounts
- [ ] Emailed employees
- [ ] Automatic backups scheduled

---

## 🎉 SUCCESS!

**If all boxes are checked, you're done!**

---

## Quick Reference - Write This Down!

**Server IP Address:**
```
http://___.___.___.___ : 8000
```

**Admin Credentials:**
```
Username: admin
Password: _______________
```

**Important Folders:**
```
Application: C:\IssueTracker
Database:    C:\IssueTracker\issue_tracker.db
Backups:     C:\IssueTracker\Backups
Logs:        C:\IssueTracker\logs
```

**Service Commands (Command Prompt as Admin):**
```
Start:   nssm start EFIIssueTracker
Stop:    nssm stop EFIIssueTracker
Restart: nssm restart EFIIssueTracker
Status:  nssm status EFIIssueTracker
```

---

## If Something Goes Wrong

**Service won't start?**
1. Restart the computer
2. Open Command Prompt as Administrator
3. Type: `nssm restart EFIIssueTracker`

**Can't access from other computers?**
1. Check server is on
2. Check firewall (Windows Defender Firewall)
3. Make sure "EFI Issue Tracker" is allowed

**Forgot password?**
1. Open Command Prompt as Administrator
2. Type: `cd C:\IssueTracker`
3. Type: `python manage_users_cli.py`
4. Choose option 4 to reset password

---

## Support

**Need Help?**
- See: EASY_SETUP.md (detailed instructions)
- Check logs: C:\IssueTracker\logs\service.log
- Contact: [Your IT support]

---

**Print this page and check off each item as you go!**

**Good luck! You've got this!** 💪
