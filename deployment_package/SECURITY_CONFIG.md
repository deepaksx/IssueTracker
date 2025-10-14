# Security Configuration Guide - EFI Issue Tracker v2.0.0

This document provides security configuration guidelines for IT administrators deploying the EFI Issue Tracker.

---

## 🔒 Security Overview

The EFI Issue Tracker includes multiple security layers:
- Password hashing (Werkzeug PBKDF2)
- Session management (Flask-Login with secure cookies)
- SQL injection protection (parameterized queries)
- Role-based access control (RBAC)
- Complete audit logging
- CSRF protection (Flask built-in)

---

## 🛡️ Pre-Deployment Security Checklist

### ☐ 1. Change Default Credentials

**CRITICAL**: The default admin credentials MUST be changed before deployment.

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

**Steps:**
1. Log in as admin
2. Navigate to **Users** → Edit admin user
3. Change password to a strong password (12+ characters, mixed case, numbers, symbols)
4. Store new password in password manager
5. Document password change in deployment log

**Password Requirements:**
- Minimum 12 characters
- Mix of uppercase and lowercase
- Include numbers
- Include special characters
- Not based on dictionary words
- Not previously used

### ☐ 2. Generate Secure SECRET_KEY

The SECRET_KEY is used for session encryption and MUST be unique and random.

**Generate a New Secret Key:**

**Windows:**
```cmd
python -c "import secrets; print(secrets.token_hex(32))"
```

**Linux:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Configure SECRET_KEY:**

**Option A: Environment Variable (Recommended)**
```bash
# Windows
set SECRET_KEY=your-generated-secret-key-here

# Linux
export SECRET_KEY=your-generated-secret-key-here
```

**Option B: .env File**
Create `.env` file in application root:
```env
SECRET_KEY=your-generated-secret-key-here
FLASK_ENV=production
```

**Option C: Direct Configuration**
Edit `config.py`:
```python
class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-generated-secret-key-here'
```

**⚠️ NEVER commit SECRET_KEY to version control!**

---

## 🌐 Network Security

### ☐ 3. Configure Firewall Rules

**Windows Firewall:**
```cmd
# Allow inbound on port 8000 (adjust port as needed)
netsh advfirewall firewall add rule name="EFI Issue Tracker" dir=in action=allow protocol=TCP localport=8000

# Restrict to internal network (optional)
# Replace 192.168.1.0/24 with your network
netsh advfirewall firewall set rule name="EFI Issue Tracker" new remoteip=192.168.1.0/24
```

**Linux (iptables):**
```bash
# Allow port 8000 from internal network only
sudo iptables -A INPUT -p tcp --dport 8000 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j DROP

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

**Linux (ufw):**
```bash
# Simple allow (all sources)
sudo ufw allow 8000/tcp

# Or restrict to internal network
sudo ufw allow from 192.168.1.0/24 to any port 8000
```

### ☐ 4. Network Isolation

**Recommendations:**
- Deploy on internal network only (no internet exposure)
- Use VPN for remote access instead of exposing to internet
- Implement network segmentation (separate VLAN for applications)
- Monitor network traffic for anomalies

---

## 🔐 HTTPS Configuration (Production)

### ☐ 5. SSL/TLS Certificate

**Option A: Internal CA (For internal networks)**
1. Use your organization's internal Certificate Authority
2. Generate CSR from server
3. Get certificate signed by CA
4. Distribute CA certificate to all client computers

**Option B: Let's Encrypt (For internet-accessible deployments)**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx  # For Nginx

# Generate certificate
sudo certbot --nginx -d issuetracker.yourdomain.com
```

**Option C: Self-Signed Certificate (Development/Testing Only)**
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### ☐ 6. Configure Reverse Proxy with HTTPS

**Nginx Configuration:**

Create `/etc/nginx/sites-available/issuetracker`:
```nginx
server {
    listen 80;
    server_name issuetracker.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name issuetracker.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Strong SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Increase upload size for PDFs
    client_max_body_size 16M;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/issuetracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Apache Configuration:**

Create `/etc/apache2/sites-available/issuetracker.conf`:
```apache
<VirtualHost *:80>
    ServerName issuetracker.yourdomain.com
    Redirect permanent / https://issuetracker.yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName issuetracker.yourdomain.com

    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem

    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    LimitRequestBody 16777216
</VirtualHost>
```

Enable modules and site:
```bash
sudo a2enmod ssl proxy proxy_http headers
sudo a2ensite issuetracker
sudo systemctl reload apache2
```

---

## 👥 User Account Security

### ☐ 7. User Password Policy

**Enforce Strong Passwords:**
- Minimum 8 characters (code already enforces this)
- Require password changes on first login
- Document password requirements for users
- Use password manager for distribution

**User Account Management:**
```python
# Example: Create users with strong passwords
# Via web interface (recommended) or CLI
python manage_users_cli.py

# Add user
# Choose strong passwords
# Assign appropriate roles (Admin/HOD/Viewer)
```

### ☐ 8. Role-Based Access Control (RBAC)

**Principle of Least Privilege:**
- **Admin**: Only for IT administrators (full access)
- **HOD**: For department heads (create/edit within their department)
- **Viewer**: For regular users (read-only within their department)

**Review User Roles Quarterly:**
```sql
-- Query to review user roles
sqlite3 issue_tracker.db "SELECT username, role, company, department FROM users;"
```

### ☐ 9. Disable Unused Accounts

**Regular Account Audits:**
1. Review user list monthly
2. Disable accounts for terminated employees
3. Remove accounts after 90 days of inactivity

**Delete User (Web Interface):**
1. Log in as admin
2. Go to **Users**
3. Click Delete for inactive users

---

## 📊 Audit Logging and Monitoring

### ☐ 10. Enable Audit Logging

Audit logging is enabled by default. All changes are logged to the database.

**Review Audit Logs:**
1. Log in as admin
2. Navigate to **Audit Log**
3. Review recent changes
4. Look for suspicious activity

**Export Audit Logs:**
```bash
# Export to CSV for external analysis
# Via web interface: Dashboard → Export CSV
# Or direct database query:
sqlite3 issue_tracker.db "SELECT * FROM audit_log ORDER BY timestamp DESC;" > audit_export.csv
```

### ☐ 11. Monitor Application Logs

**Application Logs Location:**
- **Development**: Console output
- **Production**: Log file (configure in `config.py`)

**Configure Logging:**
Edit `config.py`:
```python
import logging

# In ProductionConfig class:
LOG_FILE = '/var/log/issuetracker/app.log'
LOG_LEVEL = logging.INFO

# Create log directory
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
```

**Review Logs Regularly:**
```bash
# View recent logs
tail -f /var/log/issuetracker/app.log

# Search for errors
grep -i error /var/log/issuetracker/app.log

# Search for failed logins
grep -i "invalid" /var/log/issuetracker/app.log
```

---

## 💾 Data Protection and Backup

### ☐ 12. Configure Automated Backups

**Backup Includes:**
- SQLite database (`issue_tracker.db`)
- Uploaded PDF files (`uploads/` folder)

**Manual Backup (Via Web Interface):**
1. Log in as admin
2. Go to **Database** → **Backup Database**
3. Download ZIP file
4. Store securely off-server

**Automated Backup (Windows Task Scheduler):**
```cmd
# Create backup script: backup.bat
@echo off
cd C:\IssueTracker
python -c "from app import app; from datetime import datetime; import shutil, zipfile, os; ts=datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S'); backup_dir='backups'; os.makedirs(backup_dir, exist_ok=True); zipf=zipfile.ZipFile(f'{backup_dir}/backup_{ts}.zip', 'w', zipfile.ZIP_DEFLATED); zipf.write('issue_tracker.db'); [zipf.write(os.path.join(root, f), os.path.join('uploads', os.path.relpath(os.path.join(root, f), 'uploads'))) for root, dirs, files in os.walk('uploads') for f in files]; zipf.close(); print(f'Backup created: backup_{ts}.zip')"
```

Create scheduled task:
```
Task: Daily Backup - EFI Issue Tracker
Trigger: Daily at 2:00 AM
Action: Run backup.bat
```

**Automated Backup (Linux Cron):**
```bash
# Create backup script: /usr/local/bin/backup-issuetracker.sh
#!/bin/bash
cd /opt/IssueTracker
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/issuetracker"
mkdir -p $BACKUP_DIR

# Create ZIP backup
zip -r "$BACKUP_DIR/backup_$TIMESTAMP.zip" issue_tracker.db uploads/

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.zip" -mtime +30 -delete

echo "Backup completed: backup_$TIMESTAMP.zip"
```

Make executable and add to cron:
```bash
sudo chmod +x /usr/local/bin/backup-issuetracker.sh

# Edit crontab
sudo crontab -e

# Add line (runs daily at 2 AM):
0 2 * * * /usr/local/bin/backup-issuetracker.sh >> /var/log/issuetracker-backup.log 2>&1
```

### ☐ 13. Backup Storage and Retention

**Backup Strategy:**
- **Local Backups**: On-server (last 7 days)
- **Network Backups**: Network share (last 30 days)
- **Off-Site Backups**: Cloud or tape (last 12 months)

**Test Restore Regularly:**
```bash
# Test restore on separate test server
# Extract backup ZIP
unzip backup_20251015_020000.zip

# Verify database integrity
sqlite3 issue_tracker.db "PRAGMA integrity_check;"

# Test application startup
python app.py
```

---

## 🔍 Security Monitoring

### ☐ 14. Failed Login Monitoring

**Monitor for Brute Force Attacks:**
```bash
# Check for failed logins
grep "Invalid username or password" /var/log/issuetracker/app.log | wc -l

# Alert if >10 failures in 1 hour
```

**Consider implementing rate limiting** (optional enhancement)

### ☐ 15. File Integrity Monitoring

**Monitor for Unauthorized Changes:**
```bash
# Create checksum of application files
find /opt/IssueTracker -type f -name "*.py" -exec sha256sum {} \; > checksums.txt

# Verify regularly
sha256sum -c checksums.txt
```

---

## 📱 Session Security

### ☐ 16. Configure Session Security

Edit `config.py`:
```python
class ProductionConfig(Config):
    # Session configuration
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # 8-hour sessions
```

**Session Timeout:**
- Default: 8 hours
- Adjust based on security requirements
- Shorter = more secure, less convenient

---

## 🚨 Incident Response

### ☐ 17. Security Incident Plan

**If Security Breach Suspected:**

1. **Isolate**: Disconnect server from network
2. **Assess**: Review audit logs and system logs
3. **Document**: Record all findings
4. **Preserve**: Create forensic backup
5. **Notify**: Inform security team/management
6. **Remediate**: Patch vulnerability, reset passwords
7. **Restore**: From known good backup if needed
8. **Review**: Post-incident analysis

**Emergency Contacts:**
- IT Security Lead: _______________
- System Administrator: _______________
- Management: _______________

---

## ✅ Security Compliance Checklist

### Pre-Production
- [ ] Default passwords changed
- [ ] SECRET_KEY generated and secured
- [ ] Firewall configured
- [ ] SSL/TLS enabled (if applicable)
- [ ] User accounts created with strong passwords
- [ ] Roles assigned correctly (least privilege)
- [ ] Automated backups configured
- [ ] Backup restoration tested
- [ ] Audit logging verified
- [ ] Security headers configured
- [ ] Upload size limits configured
- [ ] Session timeout configured

### Post-Deployment (Ongoing)
- [ ] Weekly: Review audit logs
- [ ] Monthly: Review user accounts
- [ ] Monthly: Test backup restoration
- [ ] Quarterly: User access review
- [ ] Quarterly: Security updates applied
- [ ] Annually: Full security audit
- [ ] Annually: Penetration testing (optional)

---

## 📞 Security Support

**For Security Questions:**
- Review this guide
- Consult your organization's security team
- Contact: _______________

**Report Security Issues:**
- GitHub (for non-sensitive issues): https://github.com/deepaksx/IssueTracker/issues
- Email (for sensitive issues): _______________

---

**Document Version**: 1.0
**Application Version**: 2.0.0
**Last Updated**: 2025-10-15
**Security Review Date**: _______________ (review annually)
