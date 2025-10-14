# EFI IT Issue Tracker - Easy Setup Guide
## For People Who Are Not Tech Experts

**Time Required:** 30-45 minutes
**Difficulty:** Easy - No technical knowledge required
**You'll need:** A Windows computer/server and administrator password

---

## What This Application Does

This is a website that helps your company track IT problems. Once installed:
- Employees can report IT issues through a web page
- You can see all issues in one place
- Track which issues are fixed
- Store documents related to issues
- See history of all changes

---

## Before You Start - Checklist

**Things you need:**

- [ ] A Windows computer that will stay on during work hours
  - Can be a dedicated server OR a desktop PC
  - Windows 10 or Windows Server

- [ ] Administrator password for this computer

- [ ] This computer must be connected to your company network
  - Other employees' computers can see it

- [ ] 30-45 minutes of time

**That's it! Let's begin.**

---

## Part 1: Install Python (10 minutes)

Python is the "engine" that runs this application. Think of it like installing Microsoft Office.

### Step 1.1: Download Python

1. Open your web browser (Chrome, Edge, Firefox)
2. Go to: **https://www.python.org/downloads/**
3. You'll see a big yellow button that says **"Download Python 3.11.x"**
4. Click that button
5. Wait for the download to finish (it's about 25 MB)

### Step 1.2: Install Python

1. Find the downloaded file (probably in your Downloads folder)
   - It's named something like: `python-3.11.9-amd64.exe`

2. **Double-click** the file to start installation

3. **⚠️ IMPORTANT - READ THIS FIRST:**
   Before clicking anything, look at the bottom of the window

   You'll see two checkboxes:
   - ☐ Install launcher for all users (recommended)
   - ☐ Add Python 3.11 to PATH

   **You MUST check both boxes!** ✅✅

4. Now click the big button that says **"Install Now"**

5. Wait for installation (2-3 minutes)

6. When it says "Setup was successful", click **Close**

### Step 1.3: Verify Python is Installed

1. Click the Windows Start button (bottom left)
2. Type: **cmd**
3. Press **Enter** (a black window will open - this is normal)
4. In the black window, type exactly:
   ```
   python --version
   ```
5. Press **Enter**
6. You should see something like: `Python 3.11.9`
   - If you see this, SUCCESS! Move to Part 2.
   - If you see an error, Python didn't install correctly. Try Part 1 again.

---

## Part 2: Download the Application (5 minutes)

### Option A: Download as ZIP (Easiest)

1. Go to: **https://github.com/deepaksx/IssueTracker**
2. Look for a green button that says **"Code"**
3. Click it
4. Click **"Download ZIP"**
5. Wait for download to finish
6. Go to your Downloads folder
7. **Right-click** on `IssueTracker-main.zip`
8. Click **"Extract All..."**
9. Change the location to: **C:\**
10. Click **Extract**
11. Rename the folder from `IssueTracker-main` to just `IssueTracker`

**Final result:** You should have a folder at `C:\IssueTracker`

### Option B: Using Git (If you have Git installed)

1. Click Windows Start button
2. Type: **cmd**
3. Press **Enter**
4. Type these commands one at a time, pressing Enter after each:
   ```
   cd C:\
   git clone https://github.com/deepaksx/IssueTracker.git
   ```

---

## Part 3: Install Application Requirements (5 minutes)

The application needs some extra pieces to work. Let's install them.

1. Click Windows Start button
2. Type: **cmd**
3. Press **Enter** (black window opens)
4. Type this command and press **Enter**:
   ```
   cd C:\IssueTracker
   ```
5. Now type this and press **Enter**:
   ```
   pip install -r requirements.txt
   ```
6. You'll see lots of text scrolling (this is normal)
7. Wait 2-3 minutes for it to finish
8. When you see the C:\IssueTracker> prompt again, you're done

---

## Part 4: Set Up the Database (2 minutes)

This creates the database where all issues will be stored.

1. In the same black window from Part 3, type:
   ```
   python init_db.py
   ```
2. Press **Enter**
3. You'll see messages about creating tables
4. When done, you'll see:
   - "Database initialized successfully"
   - "Default users created"

**That's it! Database is ready.**

---

## Part 5: Download NSSM (Service Manager) (5 minutes)

NSSM makes the application run automatically like a service.

1. Open your web browser
2. Go to: **https://nssm.cc/download**
3. Click on **"Download nssm 2.24"** (or whatever version is shown)
4. Save the file (it's a .zip file)
5. Go to your Downloads folder
6. **Right-click** on the `nssm-2.24.zip` file
7. Click **"Extract All..."**
8. Extract it anywhere (Desktop is fine)
9. Open the extracted folder
10. You'll see folders: `win32` and `win64`
11. Open the `win64` folder (use win32 if you have old 32-bit Windows)
12. You'll see a file: **`nssm.exe`**
13. **Copy** this file
14. Go to: **C:\IssueTracker**
15. Create a new folder inside called: **nssm**
16. **Paste** the nssm.exe file into this new folder

**Final result:** You should have `C:\IssueTracker\nssm\nssm.exe`

---

## Part 6: Install as Windows Service (5 minutes)

This makes the application start automatically.

### Step 6.1: Run the Installer

1. Open File Explorer
2. Go to: **C:\IssueTracker**
3. Find the file: **`install_windows_service.bat`**
4. **Right-click** on it
5. Click **"Run as administrator"**
6. If you see a security warning, click **Yes**

### Step 6.2: Watch the Installation

You'll see a window with lots of text. This is what's happening:
- ✅ Checking Python
- ✅ Checking Gunicorn
- ✅ Installing Windows service
- ✅ Opening firewall port
- ✅ Starting the service

When you see:
```
=====================================
Installation Complete!
=====================================
```

**SUCCESS!** The application is now running.

### Step 6.3: Note Your Server Information

The window will show something like:
```
Access the application at:
  http://localhost:8000
  http://192.168.1.100:8000
```

**Write down that second address (the one with numbers)!**
This is how other people will access the system.

Example: `192.168.1.100:8000`

---

## Part 7: Test the Application (3 minutes)

Let's make sure it works!

### Test 1: On the Server Computer

1. Open your web browser
2. In the address bar, type: **http://localhost:8000**
3. Press **Enter**
4. You should see a login page with:
   - EFI IT Issue Tracker logo
   - Username field
   - Password field
   - Login button

**If you see this login page, it's working!** ✅

### Test 2: From Another Computer

1. Go to a different computer on your network
2. Open a web browser
3. Type: **http://[THE-IP-YOU-WROTE-DOWN]:8000**
   - Example: `http://192.168.1.100:8000`
4. Press **Enter**
5. You should see the same login page

**If you see the login page from another computer, PERFECT!** ✅

### Test 3: Login

1. On the login page, enter:
   - **Username:** admin
   - **Password:** admin123
2. Click **Login**
3. You should see the dashboard with a list of issues (empty at first)

**If you can login and see the dashboard, EVERYTHING IS WORKING!** 🎉

---

## Part 8: Create User Accounts (10 minutes)

Now let's create accounts for your employees.

### Step 8.1: Login as Admin (if not already)

1. Go to: `http://localhost:8000` (or your IP address)
2. Login with:
   - Username: **admin**
   - Password: **admin123**

### Step 8.2: Change Admin Password (IMPORTANT!)

1. Click **"Users"** in the left menu
2. You'll see a list of users
3. Find "admin" in the list
4. Click the **pencil icon** (Edit button) next to it
5. Enter a new password (something secure!)
6. Enter it again to confirm
7. Click **"Update User"**

**Remember this new password!** Write it down somewhere safe.

### Step 8.3: Create User Accounts

For each employee who needs access:

1. Click **"Users"** in the left menu (if not already there)
2. Click the **"Add User"** button (top right)
3. Fill in the form:
   - **Username:** Employee's name or email (e.g., "john.smith" or "john@company.com")
   - **Password:** A temporary password (they can change it later)
   - **Confirm Password:** Same password again
   - **Role:** Choose "User" (not admin)
4. Click **"Create User"**
5. Repeat for each employee

---

## Part 9: Share with Employees (5 minutes)

Now tell your employees how to access it!

### Create an Email

Here's a template you can copy:

```
Subject: New IT Issue Tracker System - Please Read

Dear Team,

We have a new system for reporting IT issues.

🌐 TO ACCESS:
Open your web browser and go to:
http://[YOUR-SERVER-IP]:8000

Example: http://192.168.1.100:8000

📋 YOUR LOGIN:
Username: [their username]
Password: [temporary password]
Please change your password after first login.

❓ HOW TO USE:
1. Login with your credentials
2. Click "Add Issue" to report a problem
3. Fill in the details
4. Click "Create Issue"
5. You can track your issues from the dashboard

Questions? Reply to this email.

Thank you!
IT Department
```

**Replace [YOUR-SERVER-IP] with the actual IP address from Part 6!**

---

## Part 10: Set Up Automatic Backups (5 minutes)

Let's make sure your data is backed up daily.

### Step 10.1: Open Task Scheduler

1. Click Windows Start button
2. Type: **Task Scheduler**
3. Click on **Task Scheduler** when it appears

### Step 10.2: Create a Backup Task

1. On the right side, click **"Create Basic Task..."**
2. Name: **EFI Issue Tracker Backup**
3. Click **Next**
4. When to start: Select **Daily**
5. Click **Next**
6. Time: Choose **2:00 AM** (or whenever you want)
7. Click **Next**
8. Action: Select **"Start a program"**
9. Click **Next**
10. Program/script: Click **Browse**
11. Navigate to: **C:\IssueTracker**
12. Select: **backup.bat**
13. Click **Open**
14. Click **Next**
15. Check the box: ☑ **"Open the Properties dialog..."**
16. Click **Finish**

### Step 10.3: Configure Backup Task

A properties window will open:

1. Click the **"General"** tab
2. Check: ☑ **"Run whether user is logged on or not"**
3. Check: ☑ **"Run with highest privileges"**
4. Click **OK**
5. Enter your administrator password if asked

**Done! Backups will run automatically every day at 2 AM.**

Backups are saved to: `C:\IssueTracker\Backups`

---

## 🎉 CONGRATULATIONS! You're Done!

### What You've Accomplished:

✅ Installed Python
✅ Downloaded the application
✅ Installed all requirements
✅ Set up the database
✅ Installed as Windows service
✅ Opened firewall
✅ Tested the application
✅ Created user accounts
✅ Set up automatic backups

### The application is now:

- ✅ Running 24/7 as a Windows service
- ✅ Accessible to all employees on your network
- ✅ Backing up automatically every day
- ✅ Ready to track IT issues

---

## Quick Reference Card

**📍 Application Address:**
`http://[YOUR-SERVER-IP]:8000`

**👤 Admin Login:**
Username: admin
Password: [the new password you set]

**📁 Important Folders:**
- Application: `C:\IssueTracker`
- Database: `C:\IssueTracker\issue_tracker.db`
- Backups: `C:\IssueTracker\Backups`
- Logs: `C:\IssueTracker\logs`

**🔧 Service Management:**

To manage the service, open Command Prompt **as Administrator** and use:

```
Start:   nssm start EFIIssueTracker
Stop:    nssm stop EFIIssueTracker
Restart: nssm restart EFIIssueTracker
Status:  nssm status EFIIssueTracker
```

---

## Common Problems and Solutions

### Problem: Can't access from other computers

**Solution:**
1. Make sure the server computer is on
2. Check Windows Firewall:
   - Open Control Panel → Windows Defender Firewall
   - Click "Allow an app through firewall"
   - Look for "EFI Issue Tracker"
   - Make sure both Private and Public are checked
3. Try pinging the server from another computer:
   - Open Command Prompt
   - Type: `ping [server-ip]`
   - You should see replies

### Problem: Service won't start

**Solution:**
1. Restart the computer
2. After restart, check if it's running:
   - Open Command Prompt as Administrator
   - Type: `nssm status EFIIssueTracker`
3. If still not working, try:
   ```
   nssm restart EFIIssueTracker
   ```

### Problem: Forgot admin password

**Solution:**
1. Open Command Prompt as Administrator
2. Navigate to application:
   ```
   cd C:\IssueTracker
   ```
3. Run user management:
   ```
   python manage_users_cli.py
   ```
4. Choose option 4 to change password
5. Select admin user and set new password

### Problem: Service is running but can't login

**Solution:**
1. Clear your browser cache (Ctrl+Shift+Delete)
2. Try a different browser
3. Check if you're using the correct username/password
4. Make sure Caps Lock is off

---

## Need More Help?

### Check the Logs

If something isn't working, check the log files:

1. Open File Explorer
2. Go to: `C:\IssueTracker\logs`
3. Open: `service.log` (double-click it)
4. Look at the end of the file for any errors

### Contact Support

- Email: [Your IT support email]
- Phone: [Your IT support phone]

### Documentation

More detailed guides are available:
- Full guide: `C:\IssueTracker\INTERNAL_DEPLOYMENT.md`
- Quick guide: `C:\IssueTracker\QUICKSTART_INTERNAL.md`

---

## Daily Checklist (For IT Admin)

**Every Morning:**
- [ ] Check if service is running (see Quick Reference above)
- [ ] Verify you can access the website

**Once a Week:**
- [ ] Check backup folder has new backups
- [ ] Check disk space on server

**Once a Month:**
- [ ] Test restoring from a backup
- [ ] Review user accounts (remove any who left)

---

**You did it! The system is now ready for your company to use.** 🎉

If you followed all the steps, your Issue Tracker is:
- Running
- Accessible to all employees
- Backing up daily
- Ready to track issues

**Welcome to easier IT issue management!**

---

**Questions?** Keep this guide handy and refer back to it anytime!
