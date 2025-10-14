# Step-by-Step Instructions - Like Following a Recipe

**Think of this like cooking - just follow each step exactly!**

---

## 🥇 STEP 1: Install Python (The Engine)

**What is Python?** It's the software that makes this application run. Like how you need Microsoft Office to open Word documents, you need Python to run this application.

### Here's exactly what to do:

**1.1** Open your favorite web browser (Edge, Chrome, Firefox)

**1.2** Click in the address bar at the top

**1.3** Type exactly: `python.org/downloads`

**1.4** Press Enter

**1.5** Look for a BIG YELLOW BUTTON that says "Download Python 3.11" or "Download Python 3.12"

**1.6** Click that yellow button

**1.7** Wait for the download (you'll see it at the bottom of your browser)

**1.8** When download finishes, click on the downloaded file (at bottom of browser)

**1.9** A window will open. **STOP! READ THIS BEFORE CLICKING:**

Look at the BOTTOM of this window. You'll see two small checkboxes:
- One says "Install launcher for all users"
- One says "Add Python to PATH"

**1.10** Click BOTH of these checkboxes to turn them on (they'll have checkmarks ✓)

**1.11** NOW click the button that says "Install Now"

**1.12** Windows will ask "Do you want to allow this app to make changes?" Click **YES**

**1.13** Wait 2-3 minutes while it installs (you'll see a progress bar)

**1.14** When you see "Setup was successful", click **Close**

### Test if it worked:

**1.15** Click the Windows Start button (bottom left corner)

**1.16** Type: `cmd`

**1.17** Press Enter (a black window will open - don't be scared!)

**1.18** In the black window, type: `python --version`

**1.19** Press Enter

**1.20** You should see something like "Python 3.11.9"

✅ **If you see that, PERFECT! Python is installed. Close the black window.**

---

## 🥈 STEP 2: Get the Application Files

**What are we doing?** Downloading the actual Issue Tracker software to your computer.

### Download Method:

**2.1** Open your web browser

**2.2** Type in address bar: `github.com/deepaksx/IssueTracker`

**2.3** Press Enter

**2.4** Look for a GREEN BUTTON that says "Code"

**2.5** Click that green button

**2.6** A small menu will appear

**2.7** Click where it says "Download ZIP" (at the bottom of that menu)

**2.8** Wait for download to finish

**2.9** Open your File Explorer (the folder icon in your taskbar)

**2.10** Click on "Downloads" on the left side

**2.11** Find the file named "IssueTracker-main.zip"

**2.12** RIGHT-CLICK on that file (not left-click!)

**2.13** In the menu that appears, click "Extract All..."

**2.14** A window opens asking "Where do you want to extract?"

**2.15** Change the path to: `C:\`

**2.16** Click "Extract"

**2.17** Wait for extraction to finish

**2.18** A new window will open showing the extracted folder

**2.19** The folder is called "IssueTracker-main"

**2.20** RIGHT-CLICK on this folder

**2.21** Click "Rename"

**2.22** Change the name to just: `IssueTracker` (remove the "-main" part)

**2.23** Press Enter

✅ **Done! You now have C:\IssueTracker folder with all the files.**

---

## 🥉 STEP 3: Install Required Pieces

**What's happening?** The application needs some extra pieces to work. We're installing them now.

**3.1** Click Windows Start button

**3.2** Type: `cmd`

**3.3** Press Enter (black window opens again)

**3.4** In the black window, type exactly: `cd C:\IssueTracker`

**3.5** Press Enter (this "moves" you into that folder)

**3.6** Now type exactly: `pip install -r requirements.txt`

**3.7** Press Enter

**3.8** You'll see LOTS of text scrolling up - THIS IS NORMAL! Don't panic!

**3.9** Wait 2-3 minutes (go get coffee ☕)

**3.10** When the scrolling stops and you see `C:\IssueTracker>` again, it's done

✅ **All the extra pieces are installed!**

---

## 🏅 STEP 4: Create the Database

**What's happening?** Creating a "storage box" where all the issues will be saved.

**4.1** In the same black window from Step 3, type: `python init_db.py`

**4.2** Press Enter

**4.3** You'll see several messages like:
- "Creating tables..."
- "Database initialized successfully"
- "Default users created"

✅ **Database is ready!**

---

## 🎖️ STEP 5: Get NSSM (Service Manager)

**What's NSSM?** It's a helper tool that makes the application run automatically when your computer starts.

**5.1** Open web browser

**5.2** Type in address bar: `nssm.cc/download`

**5.3** Press Enter

**5.4** Click on "Download nssm 2.24" (or whatever version number is shown)

**5.5** Save the file

**5.6** Go to your Downloads folder

**5.7** Find "nssm-2.24.zip" (or similar name)

**5.8** RIGHT-CLICK on it

**5.9** Click "Extract All..."

**5.10** Click "Extract"

**5.11** A new window opens with the extracted folder

**5.12** Double-click to open the "nssm-2.24" folder

**5.13** You'll see two folders: "win32" and "win64"

**5.14** Open the "win64" folder (if you have old Windows, use win32)

**5.15** You'll see a file: "nssm.exe"

**5.16** RIGHT-CLICK on "nssm.exe"

**5.17** Click "Copy"

**5.18** Open a NEW File Explorer window

**5.19** Navigate to: C:\IssueTracker

**5.20** Inside this folder, RIGHT-CLICK in empty space

**5.21** Click "New" → "Folder"

**5.22** Name it: `nssm`

**5.23** Press Enter

**5.24** Double-click to open the new "nssm" folder

**5.25** RIGHT-CLICK in this empty folder

**5.26** Click "Paste"

✅ **NSSM is in place! You should have: C:\IssueTracker\nssm\nssm.exe**

---

## 🏆 STEP 6: Install the Service (Most Important!)

**What's happening?** Installing the application so it runs automatically.

**6.1** Open File Explorer

**6.2** Go to: C:\IssueTracker

**6.3** Find a file called: "install_windows_service.bat"

**6.4** RIGHT-CLICK on this file (very important - RIGHT-click, not left!)

**6.5** You'll see a menu

**6.6** Click "Run as administrator"

**6.7** Windows will ask "Do you want to allow this?" Click **YES**

**6.8** A black window will open with lots of text

**6.9** Watch the text scroll by (this is normal!)

**6.10** Wait about 30 seconds

**6.11** You'll see messages like:
- "Installing service..."
- "Configuring firewall..."
- "Starting service..."
- "Installation Complete!"

**6.12** Look for these lines near the end:
```
Access the application at:
  http://localhost:8000
  http://192.168.1.100:8000    ← THIS ONE IS IMPORTANT!
```

**6.13** **WRITE DOWN** that IP address (the one with numbers, not localhost)

**MY SERVER IP IS: ___.___.___.___ : 8000**

Example: 192.168.1.100:8000

**6.14** Press any key to close the window

✅ **Service is installed and running!**

---

## 🎯 STEP 7: Test It!

**Let's make sure everything works!**

### Test A: On the Server Computer

**7.1** Open your web browser (Edge, Chrome, Firefox)

**7.2** Click in the address bar at the top

**7.3** Type EXACTLY: `localhost:8000`

**7.4** Press Enter

**7.5** You should see a page with:
- "EFI IT Issue Tracker" at the top
- A username box
- A password box
- A "Login" button

✅ **If you see this login page, IT'S WORKING!**

### Test B: From Another Computer

**7.6** Go to a DIFFERENT computer on your network

**7.7** Open a web browser

**7.8** Type in address bar: `[YOUR-IP]:8000`

Replace [YOUR-IP] with the number you wrote down in step 6.13

Example: `192.168.1.100:8000`

**7.9** Press Enter

**7.10** You should see the SAME login page

✅ **If you can see it from another computer, PERFECT!**

### Test C: Login

**7.11** On the login page, type:
- Username: `admin`
- Password: `admin123`

**7.12** Click "Login"

**7.13** You should see a page with:
- Menu on the left
- "Dashboard" at the top
- An empty table (or list of issues)

✅ **If you see the dashboard, EVERYTHING IS WORKING!** 🎉

---

## 🔐 STEP 8: Change Admin Password (IMPORTANT!)

**Why?** The default password "admin123" is not secure. Let's change it!

**8.1** Make sure you're logged in (from Step 7)

**8.2** Look at the menu on the LEFT side

**8.3** Click on "Users"

**8.4** You'll see a table with users

**8.5** Find the row that says "admin"

**8.6** On that row, click the PENCIL icon (it's in the Actions column)

**8.7** A form will appear

**8.8** Look for "New Password" box

**8.9** Type a NEW secure password (one you'll remember!)

**8.10** Look for "Confirm Password" box

**8.11** Type the SAME password again

**8.12** Click "Update User" button at the bottom

**8.13** You should see a green message "User updated successfully"

**WRITE DOWN YOUR NEW PASSWORD:**

**Admin Password: _______________**

✅ **Admin password is now secure!**

---

## 👥 STEP 9: Create Users for Your Employees

**Now let's create an account for each employee.**

### For EACH employee, do this:

**9.1** Click "Users" in the left menu (if not already there)

**9.2** Click the blue "Add User" button (top right)

**9.3** Fill in the form:

- **Username:** The person's name (like "john.smith")
  Type: `_______________`

- **Password:** A temporary password they'll change later (like "Welcome123")
  Type: `_______________`

- **Confirm Password:** Same password again
  Type: `_______________`

- **Role:** Click the dropdown, select "User" (NOT admin!)

**9.4** Click "Create User" button

**9.5** You should see "User created successfully"

**9.6** WRITE DOWN the username and password for this person

**REPEAT Steps 9.1 to 9.6 for EVERY employee who needs access**

✅ **User accounts created!**

---

## 📧 STEP 10: Tell Employees How to Access

**Copy this email and send to each employee:**

```
Subject: New IT Issue Tracker - Your Access

Hi [Employee Name],

We have a new system for reporting IT issues.

TO ACCESS IT:
1. Open your web browser
2. Type this address: http://[YOUR-IP]:8000
3. Press Enter

YOUR LOGIN:
Username: [their username from step 9]
Password: [their password from step 9]

FIRST TIME LOGIN:
After you login, please change your password:
1. Click "Users" in the menu
2. Click the pencil next to your name
3. Enter a new password
4. Click Update

HOW TO REPORT AN ISSUE:
1. Login
2. Click "Add Issue" button
3. Fill in the problem details
4. Click "Create Issue"

Questions? Reply to this email.

Thanks!
IT Department
```

**IMPORTANT:** Replace [YOUR-IP] with the IP you wrote down in Step 6!

✅ **Employees can now access the system!**

---

## 💾 STEP 11: Setup Automatic Backups

**What's this?** Makes the system automatically backup your data every night.

**11.1** Click Windows Start button

**11.2** Type: `task scheduler`

**11.3** Click on "Task Scheduler" when it appears

**11.4** In Task Scheduler, on the right side, click "Create Basic Task..."

**11.5** Task name: Type `EFI Issue Tracker Backup`

**11.6** Click "Next"

**11.7** When do you want: Click "Daily"

**11.8** Click "Next"

**11.9** Start: Pick today's date

**11.10** Time: Type `2:00 AM` (or whatever time you want)

**11.11** Click "Next"

**11.12** Action: Make sure "Start a program" is selected

**11.13** Click "Next"

**11.14** Program/script: Click "Browse" button

**11.15** Navigate to: C:\IssueTracker

**11.16** Click on: backup.bat

**11.17** Click "Open"

**11.18** Click "Next"

**11.19** Check the box that says "Open the Properties dialog..."

**11.20** Click "Finish"

**11.21** A new window opens (Properties)

**11.22** Look for a checkbox: "Run whether user is logged on or not"

**11.23** CHECK that box

**11.24** Look for another checkbox: "Run with highest privileges"

**11.25** CHECK that box too

**11.26** Click "OK"

**11.27** Windows might ask for your password - type it in

**11.28** Click "OK"

✅ **Backups will run automatically every day!**

Backups are saved in: C:\IssueTracker\Backups

---

## 🎉 YOU'RE DONE! CONGRATULATIONS!

### What You've Accomplished:

✅ Installed Python
✅ Downloaded the application
✅ Installed all requirements
✅ Created the database
✅ Downloaded NSSM
✅ Installed the service
✅ Tested it works
✅ Changed admin password
✅ Created user accounts
✅ Emailed employees
✅ Setup automatic backups

### The Application Is Now:

- ✅ Running on your server
- ✅ Accessible to all employees
- ✅ Backing up automatically
- ✅ Ready to track issues

---

## Quick Reference - Keep This Handy!

**To access the system:**
```
http://___.___.___.___ : 8000
(Your IP from Step 6)
```

**Admin login:**
```
Username: admin
Password: [Your new password from Step 8]
```

**To manage the service:**

Open Command Prompt AS ADMINISTRATOR, then:
```
Check if running: nssm status EFIIssueTracker
Start:            nssm start EFIIssueTracker
Stop:             nssm stop EFIIssueTracker
Restart:          nssm restart EFIIssueTracker
```

**Important folders:**
```
Application: C:\IssueTracker
Database:    C:\IssueTracker\issue_tracker.db
Backups:     C:\IssueTracker\Backups
Logs:        C:\IssueTracker\logs
```

---

## If Something Goes Wrong

**Problem: Can't access from other computers**

Solution:
1. Make sure the server computer is turned on
2. Try turning off Windows Firewall temporarily to test
3. If it works with firewall off, you need to add a firewall rule

**Problem: Service stopped working**

Solution:
1. Restart the computer
2. After restart, open Command Prompt as Administrator
3. Type: `nssm restart EFIIssueTracker`

**Problem: Forgot admin password**

Solution:
1. Open Command Prompt as Administrator
2. Type: `cd C:\IssueTracker`
3. Type: `python manage_users_cli.py`
4. Follow the prompts to reset password

---

## Need More Help?

- **Detailed Guide:** Open EASY_SETUP.md
- **Troubleshooting:** Open INTERNAL_DEPLOYMENT.md
- **Quick Checklist:** Open SETUP_CHECKLIST.md

---

**YOU DID IT!** 🎉

**The system is ready to use. Great job!**
