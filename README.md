# IT Issue Tracker

**Version 2.0.0**

A secure, browser-based web application for managing IT issues with role-based access control and comprehensive audit logging.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](VERSION)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-orange.svg)](https://flask.palletsprojects.com/)

## What's New in Version 2.0.0

### Major Features
- **Enhanced RBAC System**: Three-tier role system (Admin, HOD, Viewer) with company/department-based access control
- **Database Management**: Complete backup/restore system with ZIP archives (includes all data and PDF files)
- **Edit History Tracking**: Full text preservation of all issue description changes with timestamps
- **Document Management**: PDF upload, viewing, and download with mobile optimization
- **Organization Management**: Companies, Departments, and Applications management
- **UX Improvements**: Enhanced sidebar, auto-submit filters, and smooth transitions

📖 **[View Full Changelog](CHANGELOG.md)**

## Features

- **User Authentication**: Secure login with username/password
- **Role-Based Access Control (RBAC)**:
  - **Admin**: Full access to all features and data
  - **HOD (Head of Department)**: Can create/edit issues within their company/department
  - **Viewer**: Read-only access within their company/department
- **Issue Management**: Track IT issues with comprehensive details
- **Audit Logging**: Complete change history for all issues with immutable logs
- **Edit History**: Full text preservation of description changes
- **Document Management**: Upload, view, and download PDF attachments
- **Database Backup & Restore**: Complete backup system with ZIP archives
- **Filtering & Search**: Filter by status, priority, category, company, department, and search by keywords
- **CSV Export**: Export all issues to CSV format
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

- **Backend**: Python Flask 3.0
- **Database**: SQLite (file-based, no server required)
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Authentication**: Flask-Login with Werkzeug password hashing

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Flask-Login 0.6.3
- Werkzeug 3.0.1

### Step 2: Initialize the Database

```bash
python init_db.py
```

This script will:
- Create the SQLite database file (`issue_tracker.db`)
- Set up all required tables (users, issues, audit_log)
- Create default users

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

Open your web browser and navigate to: **http://127.0.0.1:5000**

## Default Credentials

**IMPORTANT**: Change these passwords before deploying to production!

### Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Permissions**: Full access - can create, edit, and delete issues

### Viewer User
- **Username**: `viewer`
- **Password**: `viewer123`
- **Permissions**: Read-only access - can view issues and reports

## Project Structure

```
IssueTracker/
├── app.py                  # Main Flask application with routes
├── models.py               # Database models and logic
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── issue_tracker.db        # SQLite database (created after init)
├── static/
│   ├── css/
│   │   └── style.css       # Custom CSS styling
│   └── js/
│       └── main.js         # JavaScript for dynamic features
└── templates/
    ├── base.html           # Base template with navigation
    ├── login.html          # Login page
    ├── dashboard.html      # Main dashboard with issue listing
    ├── add_issue.html      # Add new issue form
    ├── edit_issue.html     # Edit issue form
    ├── view_issue.html     # View issue details with audit trail
    └── audit_log.html      # Complete audit log viewer
```

## Usage Guide

### For All Users

1. **Login**: Navigate to the home page and log in with your credentials
2. **View Dashboard**: See all issues with filtering and search options
3. **View Issue Details**: Click on any issue to see full details and change history
4. **View Audit Log**: Access the complete audit trail from the navigation menu
5. **Export Data**: Export all issues to CSV format
6. **Logout**: Click the logout button in the navigation bar

### For Admin Users

In addition to viewer capabilities:

1. **Add Issue**: Click "Add Issue" in the navigation or dashboard
2. **Edit Issue**: Click the edit button on any issue
3. **Delete Issue**: Click the delete button on any issue (requires confirmation)
4. All changes are automatically logged in the audit trail

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password (never stored in plain text)
- `role`: User role (admin/viewer)
- `created_at`: Account creation timestamp

### Issues Table
- `id`: Primary key (issue number)
- `title`: Issue title
- `description`: Detailed description
- `company`: Company name (optional)
- `department`: Department name (optional)
- `application`: Application name (optional)
- `category`: Hardware, Software, Network, Security, Other
- `priority`: Low, Medium, High, Critical
- `status`: Open, In Progress, Resolved, Closed
- `assigned_to`: Person assigned to the issue
- `created_by`: Username of creator
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp

### Audit Log Table
- `id`: Primary key
- `timestamp`: When the change occurred
- `username`: Who made the change
- `issue_id`: Which issue was affected
- `action`: Created, Updated, Deleted
- `field_name`: Which field changed
- `old_value`: Previous value
- `new_value`: New value

## Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's secure hashing
- **Session Management**: Secure session handling with Flask-Login
- **Role-Based Access**: Admin-only routes are protected with decorators
- **SQL Injection Prevention**: Parameterized queries throughout
- **CSRF Protection**: Form submissions are protected
- **Immutable Audit Logs**: Audit logs cannot be edited or deleted
- **Session Timeout**: Configurable session expiration

## User Management

You can manage users in two ways:

### 1. Web Interface (Recommended)

Admin users can manage users through the web interface:
1. Log in as an admin user
2. Click "Users" in the navigation menu
3. Add, edit, or delete users with a user-friendly interface

Features:
- Create new users with username, password, and role
- Edit existing users (change username, password, or role)
- Delete users (cannot delete your own account)
- View all users in a table

### 2. Command-Line Interface

For quick user management without starting the web server, use the CLI tool:

```bash
manage_users.bat
```

Or directly:
```bash
python manage_users_cli.py
```

The CLI tool provides:
- List all users
- Create new users
- Delete users
- Change user passwords
- Change user roles

### 3. Programmatically

You can also add users programmatically by modifying `init_db.py`:

```python
from models import User

# Create a new user
User.create(username='newuser', password='securepassword', role='viewer')
```

Then run:
```bash
python init_db.py
```

## Customization

### Changing the Secret Key

Edit `app.py` and change this line:
```python
app.secret_key = 'your-secret-key-change-in-production'
```

Use a strong, random secret key in production!

### Changing the Port

Edit `app.py` and modify the last line:
```python
app.run(debug=True, host='127.0.0.1', port=5000)  # Change port here
```

### Database Location

By default, the SQLite database is created in the project root. To change the location, edit the `db_path` parameter in `models.py`.

## Keyboard Shortcuts

- **Alt+D**: Go to Dashboard
- **Alt+N**: Add New Issue (admin only)
- **Alt+A**: View Audit Log
- **ESC**: Close modals

## Troubleshooting

### Database Issues

If you encounter database errors, try reinitializing:
```bash
# Delete the existing database
rm issue_tracker.db  # On Windows: del issue_tracker.db

# Reinitialize
python init_db.py
```

### Port Already in Use

If port 5000 is already in use, either:
1. Stop the application using that port
2. Change the port in `app.py` (see Customization section)

### Module Not Found Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Production Deployment

🚀 **Ready to deploy as a web application!**

This application can be deployed in two ways:

### 1. Internal Company Network (Recommended for Organizations)

Deploy on your company's internal network for secure, private access.

**Best for:**
- Corporate/organizational use
- Internal IT teams
- On-premise requirements
- Complete control over data

📘 **[Complete Internal Network Deployment Guide →](INTERNAL_DEPLOYMENT.md)**

**Quick Start for Internal Network:**

**📖 Choose Your Guide:**

- **👶 [EASY_SETUP.md](EASY_SETUP.md)** - For non-technical users (step-by-step, no jargon)
- **✅ [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Printable checklist to follow
- **🎯 [STEP_BY_STEP.md](STEP_BY_STEP.md)** - Detailed walkthrough (like a recipe)
- **⚡ [QUICKSTART_INTERNAL.md](QUICKSTART_INTERNAL.md)** - For experienced IT staff
- **📚 [INTERNAL_DEPLOYMENT.md](INTERNAL_DEPLOYMENT.md)** - Complete technical documentation

**Simple Steps:**
1. Set up Windows Server or dedicated PC
2. Run `install_windows_service.bat` as Administrator
3. Configure firewall (port 8000)
4. Share URL with employees: `http://server-ip:8000`

### 2. Cloud Platform Deployment

Deploy to public cloud platforms for internet-accessible service.

**Quick Deploy Options:**

1. **Render.com** (Recommended - Free tier available)
   - Automatic deployments from GitHub
   - Free SSL certificates
   - Built-in monitoring
   - [See detailed guide →](DEPLOYMENT.md#option-1-deploy-to-rendercom-recommended---free-tier-available)

2. **Heroku**
   - Easy CLI deployment
   - Extensive add-ons
   - [See detailed guide →](DEPLOYMENT.md#option-2-deploy-to-heroku)

3. **PythonAnywhere**
   - Great for beginners
   - Free tier available
   - [See detailed guide →](DEPLOYMENT.md#option-3-deploy-to-pythonanywhere)

### Production Checklist

Before deploying:

- [ ] Set environment variables (SECRET_KEY, FLASK_ENV=production)
- [ ] Change default admin password
- [ ] Enable HTTPS (SESSION_COOKIE_SECURE=True)
- [ ] Set up database backups
- [ ] Configure monitoring/logging
- [ ] Test all features in production environment

### Environment Configuration

Create a `.env` file for production:

```env
FLASK_ENV=production
SECRET_KEY=your-randomly-generated-secret-key
SESSION_COOKIE_SECURE=True
```

**Generate secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Deploy with Gunicorn

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

📖 **For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## Support

For issues, questions, or contributions, please contact your IT administrator.

## License

This application is provided as-is for internal use. All rights reserved.

---

**Built with Flask** | **Secure Issue Management** | **Complete Audit Trail**
