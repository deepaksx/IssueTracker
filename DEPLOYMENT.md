# EFI IT Issue Tracker - Deployment Guide

This guide will help you deploy the EFI IT Issue Tracker as a web application accessible to multiple users.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Production Setup](#local-production-setup)
3. [Deploy to Cloud Platforms](#deploy-to-cloud-platforms)
4. [Configuration](#configuration)
5. [Security Considerations](#security-considerations)
6. [Maintenance](#maintenance)

---

## Prerequisites

- Python 3.11 or higher
- Git
- A cloud platform account (Render, Heroku, PythonAnywhere, or similar)
- Domain name (optional, but recommended for production)

---

## Local Production Setup

### 1. Clone the Repository

```bash
git clone https://github.com/deepaksx/IssueTracker.git
cd IssueTracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```env
FLASK_ENV=production
SECRET_KEY=your-randomly-generated-secret-key-here
DATABASE_PATH=issue_tracker.db
SESSION_COOKIE_SECURE=True
```

**Generate a secure SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Initialize Database

```bash
python init_db.py
```

### 6. Run in Production Mode

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

---

## Deploy to Cloud Platforms

### Option 1: Deploy to Render.com (Recommended - Free Tier Available)

1. **Create a Render Account**
   - Go to [render.com](https://render.com) and sign up

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `IssueTracker` repository

3. **Configure the Service**
   - **Name**: `efi-issue-tracker`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or paid for better performance)

4. **Set Environment Variables**
   Go to "Environment" tab and add:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-secret-key>
   SESSION_COOKIE_SECURE=True
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application
   - Your app will be available at: `https://efi-issue-tracker.onrender.com`

6. **Initialize Database** (First time only)
   - Go to "Shell" tab in Render dashboard
   - Run: `python init_db.py`

### Option 2: Deploy to Heroku

1. **Install Heroku CLI**
   - Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create efi-issue-tracker
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   heroku config:set SESSION_COOKIE_SECURE=True
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Initialize Database**
   ```bash
   heroku run python init_db.py
   ```

7. **Open Your App**
   ```bash
   heroku open
   ```

### Option 3: Deploy to PythonAnywhere

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for free or paid account

2. **Upload Code**
   - Use Git to clone repository:
   ```bash
   cd ~
   git clone https://github.com/deepaksx/IssueTracker.git
   ```

3. **Create Virtual Environment**
   ```bash
   cd IssueTracker
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.11
   - Set source code directory: `/home/yourusername/IssueTracker`
   - Set virtualenv: `/home/yourusername/IssueTracker/venv`

5. **Configure WSGI File**
   Edit the WSGI configuration file:
   ```python
   import sys
   import os

   # Add your project directory
   project_home = '/home/yourusername/IssueTracker'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   # Load environment variables
   os.environ['FLASK_ENV'] = 'production'
   os.environ['SECRET_KEY'] = 'your-secret-key-here'
   os.environ['SESSION_COOKIE_SECURE'] = 'True'

   # Import Flask app
   from app import app as application
   ```

6. **Initialize Database**
   - Open Bash console
   - Run: `python init_db.py`

7. **Reload Web App**
   - Click "Reload" button in Web tab

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment mode (development/production) | development | Yes |
| `SECRET_KEY` | Secret key for sessions | - | Yes (production) |
| `DATABASE_PATH` | Path to SQLite database file | issue_tracker.db | No |
| `UPLOAD_FOLDER` | Path to uploads directory | uploads | No |
| `SESSION_COOKIE_SECURE` | Enable secure cookies (HTTPS only) | False | Yes (production) |

### Database Configuration

The application uses SQLite by default. For production with multiple concurrent users, consider:

1. **Keep SQLite for small teams** (< 50 users)
2. **Migrate to PostgreSQL** for larger deployments

---

## Security Considerations

### 1. Secret Key
- **NEVER** use the default secret key in production
- Generate a random secret key: `python -c "import secrets; print(secrets.token_hex(32))"`
- Store it securely in environment variables

### 2. HTTPS/SSL
- Always use HTTPS in production
- Set `SESSION_COOKIE_SECURE=True` when using HTTPS
- Most cloud platforms provide free SSL certificates

### 3. Database Security
- Keep `issue_tracker.db` outside the web root
- Set proper file permissions (600 or 640)
- Regular backups

### 4. File Uploads
- Only PDF files are allowed
- Maximum file size: 16MB
- Files are stored with random UUIDs

### 5. Access Control
- Default admin credentials should be changed immediately
- Implement strong password policies
- Regular user access reviews

---

## Maintenance

### Backup Database

```bash
# Create backup
cp issue_tracker.db issue_tracker_backup_$(date +%Y%m%d).db

# Restore backup
cp issue_tracker_backup_20250114.db issue_tracker.db
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart application (method depends on hosting platform)
# For Render: Automatic on git push
# For Heroku: git push heroku main
# For local: Restart gunicorn process
```

### Monitor Logs

- **Render**: Check "Logs" tab in dashboard
- **Heroku**: `heroku logs --tail`
- **Local**: Check gunicorn output

### Database Maintenance

```bash
# Check database size
ls -lh issue_tracker.db

# Vacuum database (optimize)
sqlite3 issue_tracker.db "VACUUM;"
```

---

## Troubleshooting

### Issue: Application won't start

**Solution:**
- Check environment variables are set correctly
- Verify SECRET_KEY is set in production
- Check logs for error messages

### Issue: Database errors

**Solution:**
- Ensure database file exists: `python init_db.py`
- Check file permissions
- Verify DATABASE_PATH environment variable

### Issue: File uploads fail

**Solution:**
- Ensure uploads directory exists
- Check file permissions on uploads folder
- Verify MAX_CONTENT_LENGTH setting

### Issue: Users can't login

**Solution:**
- Verify database contains users
- Check password is correct
- Review session configuration

---

## Default Credentials

**⚠️ CHANGE IMMEDIATELY AFTER FIRST LOGIN**

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/deepaksx/IssueTracker/issues
- Documentation: See README.md

---

## License

Copyright © 2025 EFI IT - All Rights Reserved
