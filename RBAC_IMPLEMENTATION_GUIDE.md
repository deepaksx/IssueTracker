# Role-Based Access Control (RBAC) Implementation Guide

## Overview
This guide documents the complete RBAC implementation for the EFI IT Issue Tracker.

## Roles and Permissions

### 1. Admin
- **Full access** to everything
- Can create/edit/delete issues
- Can view/manage audit logs
- Can manage companies, departments, applications
- Can manage users
- Can view ALL issues regardless of company/department

### 2. HOD (Head of Department)
- Can create/edit/view issues **within their company and department only**
- **CANNOT** create/edit/see audit logs
- **CANNOT** manage companies, departments, or applications
- **CANNOT** manage users
- Can only see issues from their company/department

### 3. Viewer
- Can **only view** issues **within their company and department**
- **CANNOT** create or edit issues
- **CANNOT** access any management features
- **CANNOT** access audit logs
- Can only see issues from their company/department

## Implementation Status

### ✅ Completed
1. Database schema updated
2. User model updated
3. Migration script created and executed
4. Issue model filtering added
5. FlaskUser class with permission methods
6. Access control decorators created

### 🔧 Remaining Changes

#### A. Route Updates (app.py)

**1. Dashboard Route (line ~125):**
```python
@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing issues (defaults to Open issues)"""
    # Get filter parameters
    status_filter = request.args.get('status', 'Open' if not request.args else '')
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
```

**2. Add Issue Route (line ~182):**
Change decorator from `@admin_required` to `@hod_or_admin_required`
```python
@app.route('/issue/add', methods=['GET', 'POST'])
@login_required
@hod_or_admin_required  # CHANGE THIS
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
            status='Open',
            assigned_to=None,
            created_by=current_user.username
        )

        flash(f'Issue #{issue_id} created successfully!', 'success')
        return redirect(url_for('view_issue', issue_id=issue_id))

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()
    applications = Application.get_all()

    return render_template('add_issue.html',
                           companies=companies,
                           departments=departments,
                           applications=applications)
```

**3. View Issue Route (line ~225):**
Add permission check
```python
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
```

**4. Edit Issue Route (line ~243):**
Change decorator and add permission check
```python
@app.route('/issue/<int:issue_id>/edit', methods=['GET', 'POST'])
@login_required
@hod_or_admin_required  # CHANGE THIS
def edit_issue(issue_id):
    """Edit issue (HOD or admin)"""
    issue = Issue.get_by_id(issue_id)
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Check if user can access this issue
    if not current_user.can_access_issue(issue):
        flash('You do not have permission to edit this issue.', 'danger')
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

        # For HOD, don't allow changing company/department
        if current_user.is_hod():
            updates['company'] = current_user.company
            updates['department'] = current_user.department

        Issue.update(issue_id, current_user.username, updates)
        flash(f'Issue #{issue_id} updated successfully!', 'success')
        return redirect(url_for('view_issue', issue_id=issue_id))

    # Get available options for dropdowns
    companies = Company.get_all()
    departments = Department.get_all()
    applications = Application.get_all()

    return render_template('edit_issue.html',
                           issue=issue,
                           companies=companies,
                           departments=departments,
                           applications=applications)
```

**5. Audit Log Route (line ~292):**
Keep admin_required - no change needed

**6. Export CSV Route (line ~408):**
Add filtering
```python
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
```

**7. Add User Route (line ~309):**
Update to include company/department
```python
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
```

**8. Edit User Route (line ~345):**
Update to include company/department
```python
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
```

## Template Updates

All templates need to be updated to show/hide features based on user role. Key changes:

### base.html
- Hide audit log menu item for non-admin users
- Hide Users, Companies, Departments, Applications menu for non-admin users

### dashboard.html
- Hide "Add Issue" button for viewers
- Show appropriate action buttons based on role

### view_issue.html
- Hide "Activity Log" button for non-admin users
- Hide "Edit" and "Delete" buttons for viewers
- Show edit button only for HOD and admin

### add_user.html and edit_user.html
- Add company and department dropdown fields
- Make them required for HOD and Viewer roles
- Add JavaScript to show/hide based on role selection

## Testing Checklist

- [ ] Admin can see and manage everything
- [ ] HOD can create/edit issues in their company/department
- [ ] HOD cannot access audit logs, company/department/application management
- [ ] Viewer can only view issues in their company/department
- [ ] Viewer cannot create or edit issues
- [ ] Users are properly filtered by company/department
- [ ] Company/department fields work in user management

## Next Steps

Apply the route changes documented above to app.py, then update all templates to respect the new permission system.
