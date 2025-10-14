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

# Initialize database
db = Database()


class FlaskUser(UserMixin):
    """User class for Flask-Login"""

    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.role = user_data['role']

    def is_admin(self):
        return self.role == 'admin'


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
    """Main dashboard showing issues (defaults to Open issues)"""
    # Get filter parameters - default to 'Open' status if no parameters provided
    status_filter = request.args.get('status', 'Open' if not request.args else '')
    priority_filter = request.args.get('priority', '')
    category_filter = request.args.get('category', '')
    company_filter = request.args.get('company', '')
    department_filter = request.args.get('department', '')
    application_filter = request.args.get('application', '')
    search_query = request.args.get('search', '')

    # Get all issues
    issues = Issue.get_all()

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

    return render_template('dashboard.html',
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
@admin_required
def add_issue():
    """Add new issue (admin only)"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        company = request.form.get('company')
        department = request.form.get('department')
        application = request.form.get('application')
        category = request.form.get('category')
        priority = request.form.get('priority')

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
            status='Open',  # Always set new issues to Open
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

    # Get audit log for this issue
    audit_logs = AuditLog.get_by_issue(issue_id)

    # Get documents for this issue
    documents = Document.get_by_issue(issue_id)

    return render_template('view_issue.html', issue=issue, audit_logs=audit_logs, documents=documents)


@app.route('/issue/<int:issue_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_issue(issue_id):
    """Edit issue (admin only)"""
    issue = Issue.get_by_id(issue_id)
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        updates = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'company': request.form.get('company') if request.form.get('company') else None,
            'department': request.form.get('department') if request.form.get('department') else None,
            'application': request.form.get('application') if request.form.get('application') else None,
            'category': request.form.get('category'),
            'priority': request.form.get('priority'),
            'status': request.form.get('status')
        }

        Issue.update(issue_id, current_user.username, updates)
        flash(f'Issue #{issue_id} updated successfully!', 'success')
        return redirect(url_for('view_issue', issue_id=issue_id))

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()
    applications = Application.get_all()

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

        user_id = User.create(username=username, password=password, role=role)

        if user_id:
            flash(f'User "{username}" created successfully!', 'success')
            return redirect(url_for('manage_users'))
        else:
            flash(f'Username "{username}" already exists.', 'danger')
            return redirect(url_for('add_user'))

    return render_template('add_user.html')


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

        # Validation
        if password and password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

        if password and len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

        # Update user
        success = User.update(
            user_id=user_id,
            username=username if username != user['username'] else None,
            password=password if password else None,
            role=role if role != user['role'] else None
        )

        if success or (username == user['username'] and not password and role == user['role']):
            flash(f'User "{username}" updated successfully!', 'success')
            return redirect(url_for('manage_users'))
        else:
            flash(f'Failed to update user. Username may already exist.', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))

    return render_template('edit_user.html', user=user)


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
    issues = Issue.get_all()

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


@app.template_filter('datetime_format')
def datetime_format(value):
    """Format datetime for display"""
    if not value:
        return ''
    # SQLite stores datetime as string, so just format it nicely
    try:
        from datetime import datetime
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%b %d, %Y at %I:%M %p')
    except:
        return value


@app.template_filter('filesize_format')
def filesize_format(size_bytes):
    """Format file size in human readable format"""
    return format_file_size(size_bytes)


if __name__ == '__main__':
    # Make sure database is initialized
    db.init_db()

    # Run the application
    print("\n" + "="*60)
    print("EFI IT Issue Tracker Application")
    print("="*60)
    print("Starting server at http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")

    app.run(debug=True, host='127.0.0.1', port=5000)
