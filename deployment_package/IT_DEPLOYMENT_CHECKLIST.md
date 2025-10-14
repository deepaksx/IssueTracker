# IT Deployment Checklist - EFI Issue Tracker v2.0.0

**Print this checklist and check off each step as you complete it.**

---

## 📋 Pre-Deployment Planning

### ☐ 1. Review Requirements
- [ ] Read `IT_DEPLOYMENT_PACKAGE.md`
- [ ] Review system requirements
- [ ] Confirm server availability (or plan to provision)
- [ ] Verify Python 3.8+ is available
- [ ] Check network/firewall policies

### ☐ 2. Choose Deployment Option
- [ ] **Option A**: Internal Windows Server
- [ ] **Option B**: Internal Linux Server
- [ ] **Option C**: Cloud Platform (Render, Heroku, etc.)

**Selected Option**: _______________

### ☐ 3. Prepare Server
- [ ] Server OS installed and updated
- [ ] Network connectivity verified
- [ ] Static IP assigned (or DHCP reservation)
- [ ] Administrative access confirmed
- [ ] Backup system in place (optional but recommended)

---

## 📥 Download and Setup

### ☐ 4. Download Application
**Choose one method:**

#### Method A: Git Clone (Recommended)
```bash
git clone https://github.com/deepaksx/IssueTracker.git
cd IssueTracker
```
- [ ] Repository cloned successfully
- [ ] Changed to IssueTracker directory

#### Method B: ZIP Download
```
Download from: https://github.com/deepaksx/IssueTracker/archive/refs/tags/v2.0.0.zip
```
- [ ] ZIP file downloaded
- [ ] ZIP file extracted to appropriate directory
- [ ] Changed to extracted directory

### ☐ 5. Verify Files
- [ ] `app.py` exists
- [ ] `models.py` exists
- [ ] `requirements.txt` exists
- [ ] `templates/` folder exists
- [ ] `static/` folder exists
- [ ] `README.md` exists

---

## 🔧 Installation

### ☐ 6. Install Python Dependencies
**Windows:**
```cmd
pip install -r requirements.txt
```

**Linux:**
```bash
pip3 install -r requirements.txt
```

- [ ] Flask installed successfully
- [ ] Flask-Login installed successfully
- [ ] All dependencies installed without errors

### ☐ 7. Initialize Database
```bash
python init_db.py
```

- [ ] Command executed successfully
- [ ] `issue_tracker.db` file created
- [ ] Default admin user created
- [ ] No error messages displayed

---

## ⚙️ Configuration

### ☐ 8. Configure Application
Edit `config.py` or create `.env` file:

- [ ] Set `SECRET_KEY` (generate new random key)
- [ ] Set `FLASK_ENV=production`
- [ ] Configure `UPLOAD_FOLDER` path (if needed)
- [ ] Set `MAX_CONTENT_LENGTH` (default 16MB for PDFs)

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Secret Key Generated**: ________________________________

### ☐ 9. Network Configuration
- [ ] Firewall rule created for port 8000 (or chosen port)
- [ ] Port forwarding configured (if needed)
- [ ] DNS entry created (optional): _______________

**Server IP Address**: _______________
**Access URL**: http://_______________:8000

---

## 🧪 Testing

### ☐ 10. Start Application (Test Mode)
```bash
python app.py
```

- [ ] Application started successfully
- [ ] No error messages in console
- [ ] Port 5000 or 8000 is listening
- [ ] Server IP displayed in console

### ☐ 11. Test Local Access
Open browser on server: http://localhost:5000

- [ ] Login page loads correctly
- [ ] CSS and images load properly
- [ ] Can log in with admin credentials (admin/admin123)
- [ ] Dashboard displays correctly
- [ ] Can create a test issue
- [ ] Can upload a test PDF
- [ ] Can view audit log
- [ ] No console errors in browser developer tools

### ☐ 12. Test Network Access
From another computer on the network: http://[server-ip]:5000

- [ ] Application accessible from network
- [ ] Login page loads correctly
- [ ] Can log in successfully
- [ ] All features work as expected
- [ ] PDF upload and viewing work
- [ ] Mobile device access works (if applicable)

---

## 🔒 Security Hardening

### ☐ 13. Change Default Credentials
- [ ] Logged in as admin
- [ ] Navigate to Users → Edit admin
- [ ] Changed admin password to strong password
- [ ] New password documented in password manager

**New Admin Password stored in**: _______________

### ☐ 14. Configure HTTPS (Production Only)
**Skip this step for internal testing**

- [ ] SSL certificate obtained (Let's Encrypt or commercial)
- [ ] Nginx/Apache configured as reverse proxy
- [ ] HTTPS redirects configured
- [ ] Certificate auto-renewal configured

### ☐ 15. Firewall Rules
- [ ] Only required ports open
- [ ] SSH/RDP access restricted to admin IPs
- [ ] Application port accessible from company network only
- [ ] Tested firewall rules

---

## 👥 User Management

### ☐ 16. Create User Accounts
For each user/department:

**User 1:**
- [ ] Created user account
- [ ] Username: _______________
- [ ] Role: Admin / HOD / Viewer (circle one)
- [ ] Company: _______________
- [ ] Department: _______________
- [ ] Password provided to user securely

**User 2:**
- [ ] Created user account
- [ ] Username: _______________
- [ ] Role: Admin / HOD / Viewer (circle one)
- [ ] Company: _______________
- [ ] Department: _______________
- [ ] Password provided to user securely

**User 3:**
- [ ] Created user account
- [ ] Username: _______________
- [ ] Role: Admin / HOD / Viewer (circle one)
- [ ] Company: _______________
- [ ] Department: _______________
- [ ] Password provided to user securely

*(Add more users as needed)*

### ☐ 17. Configure Organizations
- [ ] Added companies in "Companies" management
- [ ] Added departments in "Departments" management
- [ ] Added applications in "Applications" management

---

## 💾 Backup Configuration

### ☐ 18. Setup Backup System
**Recommended: Daily automated backups**

- [ ] Backup location configured: _______________
- [ ] Tested manual backup via Database → Backup
- [ ] Downloaded backup ZIP successfully
- [ ] Verified backup contains database and PDFs
- [ ] Tested restore from backup (on test server)
- [ ] Scheduled automated backups (Windows Task Scheduler / cron)

**Backup Schedule**: Daily at _______________ (time)
**Backup Retention**: _______________ days

---

## 🚀 Production Deployment

### ☐ 19. Production Service Setup

**Windows: Install as Windows Service**
```cmd
# As Administrator
cd C:\IssueTracker
install_windows_service.bat
```
- [ ] Service installed successfully
- [ ] Service starts automatically on boot
- [ ] Service status: Running
- [ ] Application accessible after server reboot

**Linux: Setup Systemd Service**
```bash
# Follow INTERNAL_DEPLOYMENT.md Linux section
sudo systemctl enable issuetracker
sudo systemctl start issuetracker
```
- [ ] Service created
- [ ] Service enabled on boot
- [ ] Service status: Active
- [ ] Application accessible after server reboot

### ☐ 20. Performance Optimization
- [ ] Using Gunicorn/Waitress for production (not Flask dev server)
- [ ] Configured worker processes appropriately
- [ ] Tested under load (multiple simultaneous users)
- [ ] Response time acceptable (<2 seconds for most operations)

---

## 📢 Rollout

### ☐ 21. Documentation
- [ ] Created internal documentation (or use existing docs)
- [ ] Documented access URL
- [ ] Documented support contact
- [ ] Created user quick-start guide (if needed)

### ☐ 22. User Communication
- [ ] Email sent to users with:
  - [ ] Access URL
  - [ ] Login credentials
  - [ ] Quick start guide or video
  - [ ] Support contact
  - [ ] Password change instructions

**Example Email Template:**
```
Subject: New EFI Issue Tracker System - Now Live

Dear Team,

We've deployed a new issue tracking system to help manage and track IT issues more effectively.

Access URL: http://issuetracker.company.local:8000
Your Username: [username]
Temporary Password: [password]

Please log in and change your password immediately.

For support, contact: [IT Support Email/Phone]

User Guide: [Link to documentation]

Thank you,
IT Department
```

### ☐ 23. Training
- [ ] Admin users trained (1 hour session)
- [ ] HOD users trained (30 min session)
- [ ] End users notified of self-service resources
- [ ] Training materials distributed

---

## 📊 Post-Deployment

### ☐ 24. Monitoring (First Week)
- [ ] Day 1: Check logs for errors
- [ ] Day 1: Verify backups working
- [ ] Day 3: User feedback collected
- [ ] Day 7: Performance check
- [ ] Day 7: Storage usage check
- [ ] Day 7: Security audit

### ☐ 25. Optimization
- [ ] Reviewed user feedback
- [ ] Adjusted configurations if needed
- [ ] Documented any custom configurations
- [ ] Planned maintenance schedule

---

## ✅ Final Sign-Off

### Deployment Completed By:
- **Name**: _______________
- **Date**: _______________
- **Signature**: _______________

### Tested By:
- **Name**: _______________
- **Date**: _______________
- **Signature**: _______________

### Approved By (IT Manager):
- **Name**: _______________
- **Date**: _______________
- **Signature**: _______________

---

## 📞 Support Contacts

**Technical Issues:**
- **Contact**: _______________
- **Email**: _______________
- **Phone**: _______________

**Application Issues:**
- **GitHub Issues**: https://github.com/deepaksx/IssueTracker/issues
- **Internal Support**: _______________

---

## 🔄 Maintenance Schedule

**Regular Tasks:**
- [ ] **Daily**: Automated backups
- [ ] **Weekly**: Check logs and storage
- [ ] **Monthly**: Review user accounts and permissions
- [ ] **Quarterly**: Security updates and patches
- [ ] **Annually**: Full system audit

---

**Checklist Version**: 1.0
**Application Version**: 2.0.0
**Last Updated**: 2025-10-15

**STATUS**: ☐ In Progress  ☐ Completed  ☐ On Hold

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
