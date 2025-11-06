"""
EFI IT Issue Tracker Flask Application
A secure web application for managing IT issues with role-based access control
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import csv
from io import StringIO
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from models import Database, User, Issue, AuditLog, Document, Company, Department, Application
from config import config

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize production config if needed
if env == 'production':
    config[env].init_app(app)

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize database with configured path
db = Database(app.config['DATABASE_PATH'])

# Ensure database is initialized (with auto-migration) when app starts
# This runs both in development (python app.py) and production (gunicorn)
db.init_db()


class FlaskUser(UserMixin):
    """User class for Flask-Login"""

    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.role = user_data['role']
        self.company = user_data.get('company')
        self.department = user_data.get('department')

    def is_admin(self):
        return self.role == 'admin'

    def is_hod(self):
        return self.role == 'hod'

    def is_viewer(self):
        return self.role == 'viewer'

    def can_create_issues(self):
        """Check if user can create issues"""
        return self.role in ['admin', 'hod']

    def can_edit_issues(self):
        """Check if user can edit issues"""
        return self.role in ['admin', 'hod']

    def can_access_issue(self, issue):
        """Check if user can access a specific issue"""
        if self.is_admin():
            return True
        # HOD and Viewer can only access issues in their company/department
        if issue['company'] != self.company or issue['department'] != self.department:
            return False
        return True


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    user_data = User.get_by_id(int(user_id))
    if user_data:
        return FlaskUser(user_data)
    return None


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def hod_or_admin_required(f):
    """Decorator to require HOD or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not (current_user.is_admin() or current_user.is_hod()):
            flash('You need HOD or admin privileges to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def format_file_size(size_bytes):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


@app.route('/')
def index():
    """Redirect to dashboard or login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = User.get_by_username(username)

        if user_data and User.verify_password(user_data['password_hash'], password):
            user = FlaskUser(user_data)
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard with KPIs and charts"""
    from collections import Counter

    # Get issues based on user role
    if current_user.is_admin():
        issues = Issue.get_all()
    else:
        issues = Issue.get_all(
            company=current_user.company,
            department=current_user.department
        )

    # Filter out closed issues from charts
    active_issues = [i for i in issues if i['status'] != 'Closed']

    # Calculate KPIs
    kpi = {
        'total_issues': len(active_issues),
        'open_issues': len([i for i in active_issues if i['status'] == 'Not Started']),
        'in_progress_issues': len([i for i in active_issues if i['status'] == 'In Progress']),
        'resolved_issues': len([i for i in active_issues if i['status'] == 'Resolved'])
    }

    # Prepare chart data (excluding closed issues)
    # Status distribution
    status_counter = Counter(i['status'] for i in active_issues)
    status_labels = ['Not Started', 'In Progress', 'Resolved']
    status_values = [status_counter.get(s, 0) for s in status_labels]

    # Priority distribution
    priority_counter = Counter(i['priority'] for i in active_issues)
    priority_labels = ['Low', 'Medium', 'High', 'Critical']
    priority_values = [priority_counter.get(p, 0) for p in priority_labels]

    # Category distribution
    category_counter = Counter(i['category'] for i in active_issues)
    category_labels = list(category_counter.keys())
    category_values = list(category_counter.values())

    # Company distribution by status (stacked, excluding closed)
    company_status_data = {}
    valid_statuses = ['Not Started', 'In Progress', 'Resolved']
    for issue in active_issues:
        company = issue['company'] or 'Unassigned'
        status = issue['status']
        if company not in company_status_data:
            company_status_data[company] = {'Not Started': 0, 'In Progress': 0, 'Resolved': 0}
        # Only count valid statuses (handle legacy data)
        if status in valid_statuses:
            company_status_data[company][status] += 1

    # Get top 10 companies by total issues
    sorted_companies = sorted(company_status_data.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]
    company_labels = [c[0] for c in sorted_companies]
    company_not_started = [company_status_data[c]['Not Started'] for c in company_labels]
    company_in_progress = [company_status_data[c]['In Progress'] for c in company_labels]
    company_resolved = [company_status_data[c]['Resolved'] for c in company_labels]

    chart_data = {
        'status_labels': status_labels,
        'status_values': status_values,
        'priority_labels': priority_labels,
        'priority_values': priority_values,
        'category_labels': category_labels,
        'category_values': category_values,
        'company_labels': company_labels,
        'company_not_started': company_not_started,
        'company_in_progress': company_in_progress,
        'company_resolved': company_resolved
    }

    return render_template('dashboard.html', kpi=kpi, chart_data=chart_data)


@app.route('/tracker')
@login_required
def tracker():
    """Issue tracker showing list of issues (defaults to Open issues)"""
    # Get filter parameters - default to 'Not Started' status if no parameters provided
    status_filter = request.args.get('status', 'Not Started' if not request.args else '')
    priority_filter = request.args.get('priority', '')
    category_filter = request.args.get('category', '')
    company_filter = request.args.get('company', '')
    department_filter = request.args.get('department', '')
    application_filter = request.args.get('application', '')
    search_query = request.args.get('search', '')

    # Get issues based on user role
    if current_user.is_admin():
        # Admin sees all issues
        issues = Issue.get_all()
    else:
        # HOD and Viewer only see issues from their company/department
        issues = Issue.get_all(
            company=current_user.company,
            department=current_user.department
        )

    # Apply filters
    if status_filter:
        issues = [i for i in issues if i['status'] == status_filter]
    if priority_filter:
        issues = [i for i in issues if i['priority'] == priority_filter]
    if category_filter:
        issues = [i for i in issues if i['category'] == category_filter]
    if company_filter:
        issues = [i for i in issues if (i['company'] or '').lower() == company_filter.lower()]
    if department_filter:
        issues = [i for i in issues if (i['department'] or '').lower() == department_filter.lower()]
    if application_filter:
        issues = [i for i in issues if (i['application'] or '').lower() == application_filter.lower()]
    if search_query:
        search_lower = search_query.lower()
        issues = [i for i in issues if
                  search_lower in i['title'].lower() or
                  search_lower in i['description'].lower() or
                  search_lower in (i['company'] or '').lower() or
                  search_lower in (i['department'] or '').lower() or
                  search_lower in (i['application'] or '').lower()]

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()
    applications = Application.get_all()

    return render_template('tracker.html',
                           issues=issues,
                           status_filter=status_filter,
                           priority_filter=priority_filter,
                           category_filter=category_filter,
                           company_filter=company_filter,
                           department_filter=department_filter,
                           application_filter=application_filter,
                           search_query=search_query,
                           companies=companies,
                           departments=departments,
                           applications=applications)


@app.route('/issue/add', methods=['GET', 'POST'])
@login_required
@hod_or_admin_required
def add_issue():
    """Add new issue (HOD or admin)"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        company = request.form.get('company')
        department = request.form.get('department')
        application = request.form.get('application')
        category = request.form.get('category')
        priority = request.form.get('priority')

        # For HOD, force their company/department
        if current_user.is_hod():
            company = current_user.company
            department = current_user.department

        # Validation
        if not title or not description:
            flash('Title and description are required.', 'danger')
            return redirect(url_for('add_issue'))

        issue_id = Issue.create(
            title=title,
            description=description,
            company=company if company else None,
            department=department if department else None,
            application=application if application else None,
            category=category,
            priority=priority,
            status='Not Started',  # Always set new issues to Not Started
            assigned_to=None,
            created_by=current_user.username
        )

        flash(f'Issue #{issue_id} created successfully!', 'success')
        return redirect(url_for('view_issue', issue_id=issue_id))

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()
    applications = Application.get_all()

    return render_template('add_issue.html', companies=companies, departments=departments, applications=applications)


@app.route('/issue/<int:issue_id>')
@login_required
def view_issue(issue_id):
    """View issue details"""
    issue = Issue.get_by_id(issue_id)
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Check if user can access this issue
    if not current_user.can_access_issue(issue):
        flash('You do not have permission to view this issue.', 'danger')
        return redirect(url_for('dashboard'))

    # Get audit log for this issue (only for admin)
    audit_logs = AuditLog.get_by_issue(issue_id) if current_user.is_admin() else []

    # Get documents for this issue
    documents = Document.get_by_issue(issue_id)

    return render_template('view_issue.html', issue=issue, audit_logs=audit_logs, documents=documents)


@app.route('/issue/<int:issue_id>/edit', methods=['GET', 'POST'])
@login_required
@hod_or_admin_required
def edit_issue(issue_id):
    """Edit issue (HOD or admin)"""
    issue = Issue.get_by_id(issue_id, db_path=app.config['DATABASE_PATH'])
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Check if user can access this issue
    if not current_user.can_access_issue(issue):
        flash('You do not have permission to edit this issue.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        from datetime import datetime

        new_description = request.form.get('description')
        old_description = issue['description']

        # Extract existing edit history (everything after first "--- EDIT HISTORY ---")
        history_marker = "--- EDIT HISTORY ---"
        if history_marker in old_description:
            # Split old description to get the old editable text and existing history
            parts = old_description.split(history_marker, 1)
            old_editable_text = parts[0].strip()
            existing_history = parts[1]  # Keep existing history entries
        else:
            # First edit - no history yet
            old_editable_text = old_description.strip()
            existing_history = ""

        # Add new edit entry to history with the previous text
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Build new history entry with the old text
        if existing_history:
            # Append to existing history
            new_history = existing_history + f"\n\n--- Edit by {current_user.username} on {timestamp} ---\nPrevious text: {old_editable_text}"
        else:
            # First edit - create history section
            new_history = f"\n--- Edit by {current_user.username} on {timestamp} ---\nPrevious text: {old_editable_text}"

        # Build the final description:
        # 1. New content (user's editable text)
        # 2. Edit history section (preserved with old text)
        description_with_history = new_description.strip() + "\n\n" + history_marker + new_history

        updates = {
            'title': request.form.get('title'),
            'description': description_with_history,
            'company': request.form.get('company') if request.form.get('company') else None,
            'department': request.form.get('department') if request.form.get('department') else None,
            'application': request.form.get('application') if request.form.get('application') else None,
            'category': request.form.get('category'),
            'priority': request.form.get('priority'),
            'status': request.form.get('status')
        }

        # For HOD, don't allow changing company/department
        if current_user.is_hod():
            updates['company'] = current_user.company
            updates['department'] = current_user.department

        try:
            Issue.update(issue_id, current_user.username, updates, db_path=app.config['DATABASE_PATH'])
            flash(f'Issue #{issue_id} updated successfully!', 'success')
            return redirect(url_for('view_issue', issue_id=issue_id))
        except Exception as e:
            app.logger.error(f"Error updating issue #{issue_id}: {str(e)}")
            flash(f'Error updating issue: {str(e)}', 'danger')
            return redirect(url_for('edit_issue', issue_id=issue_id))

    # Get available options for dropdowns
    companies = Company.get_all(db_path=app.config['DATABASE_PATH'])
    departments = Department.get_all(db_path=app.config['DATABASE_PATH'])
    applications = Application.get_all(db_path=app.config['DATABASE_PATH'])

    return render_template('edit_issue.html', issue=issue, companies=companies, departments=departments, applications=applications)


@app.route('/issue/<int:issue_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_issue(issue_id):
    """Delete issue (admin only)"""
    issue = Issue.get_by_id(issue_id)
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('dashboard'))

    Issue.delete(issue_id, current_user.username)
    flash(f'Issue #{issue_id} deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/audit-log')
@login_required
def audit_log():
    """View complete audit log"""
    logs = AuditLog.get_all()
    return render_template('audit_log.html', logs=logs)


@app.route('/users')
@login_required
@admin_required
def manage_users():
    """Manage users (admin only)"""
    users = User.get_all()
    return render_template('manage_users.html', users=users)


@app.route('/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """Add new user (admin only)"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        company = request.form.get('company') if request.form.get('company') else None
        department = request.form.get('department') if request.form.get('department') else None

        # Validation
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('add_user'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('add_user'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('add_user'))

        # Validate that HOD and Viewer have company/department
        if role in ['hod', 'viewer'] and (not company or not department):
            flash('Company and department are required for HOD and Viewer roles.', 'danger')
            return redirect(url_for('add_user'))

        user_id = User.create(
            username=username,
            password=password,
            role=role,
            company=company,
            department=department
        )

        if user_id:
            flash(f'User "{username}" created successfully!', 'success')
            return redirect(url_for('manage_users'))
        else:
            flash(f'Username "{username}" already exists.', 'danger')
            return redirect(url_for('add_user'))

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()

    return render_template('add_user.html', companies=companies, departments=departments)


@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit user (admin only)"""
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('manage_users'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        company = request.form.get('company') if request.form.get('company') else None
        department = request.form.get('department') if request.form.get('department') else None

        # Validation
        if password and password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

        if password and len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

        # Validate that HOD and Viewer have company/department
        if role in ['hod', 'viewer'] and (not company or not department):
            flash('Company and department are required for HOD and Viewer roles.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

        # Update user
        success = User.update(
            user_id=user_id,
            username=username if username != user['username'] else None,
            password=password if password else None,
            role=role if role != user['role'] else None,
            company=company,
            department=department
        )

        if success or (username == user['username'] and not password and
                       role == user['role'] and company == user.get('company') and
                       department == user.get('department')):
            flash(f'User "{username}" updated successfully!', 'success')
            return redirect(url_for('manage_users'))
        else:
            flash(f'Failed to update user. Username may already exist.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()

    return render_template('edit_user.html',
                           user=user,
                           companies=companies,
                           departments=departments)


@app.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('manage_users'))

    # Prevent deleting yourself
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('manage_users'))

    User.delete(user_id)
    flash(f'User "{user["username"]}" deleted successfully!', 'success')
    return redirect(url_for('manage_users'))


@app.route('/export/csv')
@login_required
def export_csv():
    """Export issues to CSV"""
    # Get issues based on user role
    if current_user.is_admin():
        issues = Issue.get_all()
    else:
        issues = Issue.get_all(
            company=current_user.company,
            department=current_user.department
        )

    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)

    # Write header
    writer.writerow(['ID', 'Title', 'Description', 'Company', 'Department', 'Application',
                     'Category', 'Priority', 'Status', 'Created By',
                     'Created At', 'Updated At'])

    # Write data
    for issue in issues:
        writer.writerow([
            issue['id'],
            issue['title'],
            issue['description'],
            issue['company'] or '',
            issue['department'] or '',
            issue['application'] or '',
            issue['category'],
            issue['priority'],
            issue['status'],
            issue['created_by'],
            issue['created_at'],
            issue['updated_at']
        ])

    # Create response
    output = si.getvalue()
    si.close()

    from flask import Response
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=issues.csv'}
    )


@app.route('/issue/<int:issue_id>/upload', methods=['POST'])
@login_required
def upload_document(issue_id):
    """Upload a document to an issue"""
    issue = Issue.get_by_id(issue_id)
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('dashboard'))

    if 'document' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('view_issue', issue_id=issue_id))

    file = request.files['document']

    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('view_issue', issue_id=issue_id))

    if not allowed_file(file.filename):
        flash('Only PDF files are allowed.', 'danger')
        return redirect(url_for('view_issue', issue_id=issue_id))

    # Generate unique filename
    original_filename = secure_filename(file.filename)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    # Save file
    file.save(file_path)
    file_size = os.path.getsize(file_path)

    # Save to database
    Document.create(
        issue_id=issue_id,
        filename=unique_filename,
        original_filename=original_filename,
        file_size=file_size,
        uploaded_by=current_user.username
    )

    flash(f'Document "{original_filename}" uploaded successfully!', 'success')
    return redirect(url_for('view_issue', issue_id=issue_id))


@app.route('/document/<int:document_id>/download')
@login_required
def download_document(document_id):
    """Download a document"""
    document = Document.get_by_id(document_id)
    if not document:
        flash('Document not found.', 'danger')
        return redirect(url_for('dashboard'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document['filename'])

    if not os.path.exists(file_path):
        flash('File not found on server.', 'danger')
        return redirect(url_for('view_issue', issue_id=document['issue_id']))

    return send_file(
        file_path,
        as_attachment=True,
        download_name=document['original_filename'],
        mimetype='application/pdf'
    )


@app.route('/document/<int:document_id>/view')
@login_required
def view_document(document_id):
    """View a PDF document inline"""
    document = Document.get_by_id(document_id)
    if not document:
        flash('Document not found.', 'danger')
        return redirect(url_for('dashboard'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document['filename'])

    if not os.path.exists(file_path):
        flash('File not found on server.', 'danger')
        return redirect(url_for('view_issue', issue_id=document['issue_id']))

    return send_file(
        file_path,
        mimetype='application/pdf',
        as_attachment=False,
        download_name=document['original_filename']
    )


@app.route('/document/<int:document_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_document(document_id):
    """Delete a document (admin only)"""
    document = Document.get_by_id(document_id)
    if not document:
        flash('Document not found.', 'danger')
        return redirect(url_for('dashboard'))

    issue_id = document['issue_id']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document['filename'])

    # Delete file from filesystem
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete from database
    Document.delete(document_id)

    flash(f'Document "{document["original_filename"]}" deleted successfully!', 'success')
    return redirect(url_for('view_issue', issue_id=issue_id))


@app.route('/companies')
@login_required
@admin_required
def manage_companies():
    """Manage companies (admin only)"""
    companies = Company.get_all()
    return render_template('manage_companies.html', companies=companies)


@app.route('/company/add', methods=['POST'])
@login_required
@admin_required
def add_company():
    """Add new company (admin only)"""
    name = request.form.get('name')

    if not name:
        flash('Company name is required.', 'danger')
        return redirect(url_for('manage_companies'))

    company_id = Company.create(name=name)

    if company_id:
        flash(f'Company "{name}" added successfully!', 'success')
    else:
        flash(f'Company "{name}" already exists.', 'danger')

    return redirect(url_for('manage_companies'))


@app.route('/company/<int:company_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_company(company_id):
    """Delete company (admin only)"""
    company = Company.get_by_id(company_id)
    if not company:
        flash('Company not found.', 'danger')
        return redirect(url_for('manage_companies'))

    Company.delete(company_id)
    flash(f'Company "{company["name"]}" deleted successfully!', 'success')
    return redirect(url_for('manage_companies'))


@app.route('/departments')
@login_required
@admin_required
def manage_departments():
    """Manage departments (admin only)"""
    departments = Department.get_all()
    return render_template('manage_departments.html', departments=departments)


@app.route('/department/add', methods=['POST'])
@login_required
@admin_required
def add_department():
    """Add new department (admin only)"""
    name = request.form.get('name')

    if not name:
        flash('Department name is required.', 'danger')
        return redirect(url_for('manage_departments'))

    department_id = Department.create(name=name)

    if department_id:
        flash(f'Department "{name}" added successfully!', 'success')
    else:
        flash(f'Department "{name}" already exists.', 'danger')

    return redirect(url_for('manage_departments'))


@app.route('/department/<int:department_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_department(department_id):
    """Delete department (admin only)"""
    department = Department.get_by_id(department_id)
    if not department:
        flash('Department not found.', 'danger')
        return redirect(url_for('manage_departments'))

    Department.delete(department_id)
    flash(f'Department "{department["name"]}" deleted successfully!', 'success')
    return redirect(url_for('manage_departments'))


@app.route('/applications')
@login_required
@admin_required
def manage_applications():
    """Manage applications (admin only)"""
    applications = Application.get_all()
    return render_template('manage_applications.html', applications=applications)


@app.route('/application/add', methods=['POST'])
@login_required
@admin_required
def add_application():
    """Add new application (admin only)"""
    name = request.form.get('name')

    if not name:
        flash('Application name is required.', 'danger')
        return redirect(url_for('manage_applications'))

    application_id = Application.create(name=name)

    if application_id:
        flash(f'Application "{name}" added successfully!', 'success')
    else:
        flash(f'Application "{name}" already exists.', 'danger')

    return redirect(url_for('manage_applications'))


@app.route('/application/<int:application_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_application(application_id):
    """Delete application (admin only)"""
    application = Application.get_by_id(application_id)
    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('manage_applications'))

    Application.delete(application_id)
    flash(f'Application "{application["name"]}" deleted successfully!', 'success')
    return redirect(url_for('manage_applications'))


@app.route('/database')
@login_required
@admin_required
def manage_database():
    """Database management page (admin only)"""
    import sqlite3

    # Get database statistics
    conn = sqlite3.connect('issue_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM documents')
    doc_count = cursor.fetchone()[0]
    conn.close()

    stats = {
        'issues': len(Issue.get_all()),
        'users': len(User.get_all()),
        'companies': len(Company.get_all()),
        'documents': doc_count
    }
    return render_template('manage_database.html', stats=stats)


@app.route('/admin/database-backup')
@login_required
@admin_required
def database_backup():
    """Backup database and uploads to ZIP file (admin only)"""
    from datetime import datetime
    import shutil
    import zipfile

    # Create backups directory if it doesn't exist
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'issue_tracker_backup_{timestamp}.zip'
    backup_path = os.path.join(backup_dir, backup_filename)

    # Create ZIP archive
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add database file
        db_path = 'issue_tracker.db'
        if os.path.exists(db_path):
            zipf.write(db_path, 'issue_tracker.db')

        # Add all files from uploads folder
        uploads_dir = app.config['UPLOAD_FOLDER']
        if os.path.exists(uploads_dir):
            for root, dirs, files in os.walk(uploads_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Store with relative path from uploads folder
                    arcname = os.path.join('uploads', os.path.relpath(file_path, uploads_dir))
                    zipf.write(file_path, arcname)

    # Send the backup ZIP file to user
    return send_file(
        backup_path,
        as_attachment=True,
        download_name=backup_filename,
        mimetype='application/zip'
    )


@app.route('/admin/database-restore', methods=['POST'])
@login_required
@admin_required
def database_restore():
    """Restore database and uploads from ZIP backup file (admin only)"""
    if 'backup_file' not in request.files:
        flash('No backup file selected.', 'danger')
        return redirect(url_for('manage_database'))

    file = request.files['backup_file']

    if file.filename == '':
        flash('No backup file selected.', 'danger')
        return redirect(url_for('manage_database'))

    # Check if it's a .zip file
    if not file.filename.endswith('.zip'):
        flash('Invalid file type. Please upload a .zip backup file.', 'danger')
        return redirect(url_for('manage_database'))

    try:
        from datetime import datetime
        import shutil
        import zipfile
        import tempfile

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        # Create backup of current database and uploads before restoring
        current_backup_filename = f'issue_tracker_pre_restore_{timestamp}.zip'
        current_backup_path = os.path.join(backup_dir, current_backup_filename)

        # Backup current state to ZIP
        with zipfile.ZipFile(current_backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            db_path = 'issue_tracker.db'
            if os.path.exists(db_path):
                zipf.write(db_path, 'issue_tracker.db')

            uploads_dir = app.config['UPLOAD_FOLDER']
            if os.path.exists(uploads_dir):
                for root, dirs, files in os.walk(uploads_dir):
                    for filename in files:
                        file_path = os.path.join(root, filename)
                        arcname = os.path.join('uploads', os.path.relpath(file_path, uploads_dir))
                        zipf.write(file_path, arcname)

        # Save uploaded file to temporary location
        temp_zip_path = os.path.join(tempfile.gettempdir(), f'restore_{timestamp}.zip')
        file.save(temp_zip_path)

        # Extract the backup ZIP
        with zipfile.ZipFile(temp_zip_path, 'r') as zipf:
            # Check if database file exists in ZIP
            if 'issue_tracker.db' not in zipf.namelist():
                os.remove(temp_zip_path)
                flash('Invalid backup file: database not found in archive.', 'danger')
                return redirect(url_for('manage_database'))

            # Delete current database
            db_path = 'issue_tracker.db'
            if os.path.exists(db_path):
                os.remove(db_path)

            # Extract database
            zipf.extract('issue_tracker.db', os.path.dirname(__file__))

            # Clear and restore uploads folder
            uploads_dir = app.config['UPLOAD_FOLDER']
            if os.path.exists(uploads_dir):
                shutil.rmtree(uploads_dir)
            os.makedirs(uploads_dir, exist_ok=True)

            # Extract all files from uploads folder in the ZIP
            for member in zipf.namelist():
                if member.startswith('uploads/') and member != 'uploads/':
                    # Extract to correct location
                    target_path = os.path.join(os.path.dirname(__file__), member)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zipf.open(member) as source, open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)

        # Clean up temporary file
        os.remove(temp_zip_path)

        flash(f'Database and uploads restored successfully! Previous state backed up to: {current_backup_filename}', 'success')
        flash('Please log in again.', 'info')

        # Log out the user since the database was restored
        logout_user()
        return redirect(url_for('login'))

    except Exception as e:
        flash(f'Error restoring database: {str(e)}', 'danger')
        return redirect(url_for('manage_database'))


@app.route('/admin/database-init', methods=['POST'])
@login_required
@admin_required
def database_init():
    """Re-initialize database (admin only) - WARNING: This deletes all data!"""
    confirmation = request.form.get('confirmation')

    if confirmation != 'RESET DATABASE':
        flash('Invalid confirmation. Please type "RESET DATABASE" exactly to confirm.', 'danger')
        return redirect(url_for('manage_database'))

    try:
        # Close existing database connections
        db_path = 'issue_tracker.db'

        # Backup before deleting
        from datetime import datetime
        import shutil
        backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'issue_tracker_pre_reset_{timestamp}.db')

        if os.path.exists(db_path):
            shutil.copy2(db_path, backup_path)
            os.remove(db_path)

        # Reinitialize database
        db.init_db()

        flash(f'Database reset successfully! A backup was created at: {backup_path}', 'warning')
        flash('Please log in again with the default admin account.', 'info')

        # Log out the user since the database was reset
        logout_user()
        return redirect(url_for('login'))

    except Exception as e:
        flash(f'Error resetting database: {str(e)}', 'danger')
        return redirect(url_for('manage_database'))


@app.template_filter('datetime_format')
def datetime_format(value):
    """Format datetime for display as dd-MMM-YYYY"""
    if not value:
        return '-'
    try:
        # Handle string date/datetime format
        if isinstance(value, str):
            # Try datetime format first (with time)
            try:
                dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                return dt.strftime('%d-%b-%Y')
            except:
                # Try date only format
                dt = datetime.strptime(value[:10], '%Y-%m-%d')
                return dt.strftime('%d-%b-%Y')
        # If it's already a datetime object
        elif hasattr(value, 'strftime'):
            return value.strftime('%d-%b-%Y')
        else:
            return str(value)
    except Exception as e:
        return str(value) if value else '-'


@app.template_filter('filesize_format')
def filesize_format(size_bytes):
    """Format file size in human readable format"""
    return format_file_size(size_bytes)


if __name__ == '__main__':
    # Make sure database is initialized
    db.init_db()

    # Get local IP address
    import socket
    try:
        # Get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "Unable to detect"

    # Run the application
    print("\n" + "="*60)
    print("EFI IT Issue Tracker Application")
    print("="*60)
    print("Server is running and accessible at:")
    print(f"  • Local:   http://127.0.0.1:5000")
    print(f"  • Network: http://{local_ip}:5000")
    print("\nOther devices on your network can access using:")
    print(f"  http://{local_ip}:5000")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
