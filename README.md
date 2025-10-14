# IT Issue Tracker

A secure, browser-based web application for managing IT issues with role-based access control and comprehensive audit logging.

## Features

- **User Authentication**: Secure login with username/password
- **Role-Based Access Control**:
  - Admin users: Can create, edit, and delete issues
  - Viewer users: Can view issues and reports (read-only)
- **Issue Management**: Track IT issues with comprehensive details
- **Audit Logging**: Complete change history for all issues with immutable logs
- **Filtering & Search**: Filter by status, priority, category, company, department, and search by keywords
- **CSV Export**: Export all issues to CSV format
- **Responsive Design**: Works on desktop and tablet devices

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

Before deploying to production:

1. **Change Default Passwords**: Update or remove default user accounts
2. **Change Secret Key**: Use a strong, random secret key
3. **Disable Debug Mode**: Set `debug=False` in `app.py`
4. **Use Production Server**: Deploy with Gunicorn or uWSGI instead of Flask's dev server
5. **Enable HTTPS**: Use SSL/TLS certificates
6. **Set Up Backups**: Regularly backup the SQLite database file
7. **Implement Session Timeout**: Configure appropriate session expiration
8. **Add Rate Limiting**: Protect against brute force attacks

Example production command with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Support

For issues, questions, or contributions, please contact your IT administrator.

## License

This application is provided as-is for internal use. All rights reserved.

---

**Built with Flask** | **Secure Issue Management** | **Complete Audit Trail**
