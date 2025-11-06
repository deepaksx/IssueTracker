"""
Database models for IT Issue Tracker
"""
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def get_db_connection(db_path='issue_tracker.db'):
    """
    Get database connection with proper settings for concurrency.
    This helper ensures all connections use WAL mode and proper timeouts.
    """
    conn = sqlite3.connect(db_path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrent access
    conn.execute('PRAGMA journal_mode=WAL')
    # Set busy timeout to 5 seconds
    conn.execute('PRAGMA busy_timeout=5000')
    return conn


class Database:
    """Database connection handler"""

    def __init__(self, db_path='issue_tracker.db'):
        self.db_path = db_path

    def get_connection(self):
        """Get database connection with optimizations for concurrency"""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrent access
        conn.execute('PRAGMA journal_mode=WAL')
        # Set busy timeout
        conn.execute('PRAGMA busy_timeout=5000')
        return conn

    def init_db(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'hod', 'viewer')),
                company TEXT,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create issues table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                company TEXT,
                department TEXT,
                application TEXT,
                category TEXT NOT NULL CHECK(category IN ('Hardware', 'Software', 'Network', 'Security', 'Other')),
                priority TEXT NOT NULL CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
                status TEXT NOT NULL CHECK(status IN ('Not Started', 'In Progress', 'Resolved', 'Closed')),
                assigned_to TEXT,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create audit_log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                issue_id INTEGER,
                action TEXT NOT NULL CHECK(action IN ('Created', 'Updated', 'Deleted')),
                field_name TEXT,
                old_value TEXT,
                new_value TEXT
            )
        ''')

        # Create documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                uploaded_by TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (issue_id) REFERENCES issues (id) ON DELETE CASCADE
            )
        ''')

        # Create companies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create departments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

        # Auto-migrate: Add missing columns to existing tables
        try:
            # Check and add missing columns to users table
            cursor.execute("PRAGMA table_info(users)")
            user_columns = [column[1] for column in cursor.fetchall()]

            if 'company' not in user_columns:
                cursor.execute('ALTER TABLE users ADD COLUMN company TEXT')
                print("✓ Auto-migrated: Added 'company' column to users table")

            if 'department' not in user_columns:
                cursor.execute('ALTER TABLE users ADD COLUMN department TEXT')
                print("✓ Auto-migrated: Added 'department' column to users table")

            if 'created_at' not in user_columns:
                cursor.execute('ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                print("✓ Auto-migrated: Added 'created_at' column to users table")

            # Check and add missing columns to issues table
            cursor.execute("PRAGMA table_info(issues)")
            issue_columns = [column[1] for column in cursor.fetchall()]

            if 'company' not in issue_columns:
                cursor.execute('ALTER TABLE issues ADD COLUMN company TEXT')
                print("✓ Auto-migrated: Added 'company' column to issues table")

            if 'department' not in issue_columns:
                cursor.execute('ALTER TABLE issues ADD COLUMN department TEXT')
                print("✓ Auto-migrated: Added 'department' column to issues table")

            if 'application' not in issue_columns:
                cursor.execute('ALTER TABLE issues ADD COLUMN application TEXT')
                print("✓ Auto-migrated: Added 'application' column to issues table")

            conn.commit()
        except Exception as e:
            print(f"Note: Auto-migration check completed with message: {e}")
        finally:
            conn.close()


class User:
    """User model"""

    @staticmethod
    def create(username, password, role='viewer', company=None, department=None, db_path='issue_tracker.db'):
        """Create a new user"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)

        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash, role, company, department) VALUES (?, ?, ?, ?, ?)',
                (username, password_hash, role, company, department)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    @staticmethod
    def get_by_username(username, db_path='issue_tracker.db'):
        """Get user by username"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_id(user_id, db_path='issue_tracker.db'):
        """Get user by ID"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def verify_password(password_hash, password):
        """Verify password against hash"""
        return check_password_hash(password_hash, password)

    @staticmethod
    def get_all(db_path='issue_tracker.db'):
        """Get all users"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT id, username, role, company, department, created_at FROM users ORDER BY username')
        users = cursor.fetchall()
        conn.close()
        return [dict(user) for user in users]

    @staticmethod
    def update(user_id, username=None, password=None, role=None, company=None, department=None, db_path='issue_tracker.db'):
        """Update user information"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        update_fields = []
        values = []

        if username:
            update_fields.append('username = ?')
            values.append(username)

        if password:
            update_fields.append('password_hash = ?')
            values.append(generate_password_hash(password))

        if role:
            update_fields.append('role = ?')
            values.append(role)

        if company is not None:
            update_fields.append('company = ?')
            values.append(company)

        if department is not None:
            update_fields.append('department = ?')
            values.append(department)

        if not update_fields:
            conn.close()
            return False

        values.append(user_id)
        query = f'UPDATE users SET {", ".join(update_fields)} WHERE id = ?'

        try:
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    @staticmethod
    def delete(user_id, db_path='issue_tracker.db'):
        """Delete a user"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()


class Issue:
    """Issue model"""

    @staticmethod
    def create(title, description, company, department, application, category, priority, status, assigned_to, created_by, db_path='issue_tracker.db'):
        """Create a new issue and log the creation"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO issues (title, description, company, department, application, category, priority, status, assigned_to, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, company, department, application, category, priority, status, assigned_to, created_by))

        issue_id = cursor.lastrowid

        # Log the creation in audit log
        AuditLog.log_action(
            username=created_by,
            issue_id=issue_id,
            action='Created',
            field_name='Issue',
            old_value=None,
            new_value=f'{title}',
            conn=conn
        )

        conn.commit()
        conn.close()
        return issue_id

    @staticmethod
    def get_all(company=None, department=None, db_path='issue_tracker.db'):
        """Get all issues, optionally filtered by company and/or department"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = 'SELECT * FROM issues'
        params = []
        conditions = []

        if company:
            conditions.append('company = ?')
            params.append(company)

        if department:
            conditions.append('department = ?')
            params.append(department)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        query += ' ORDER BY created_at DESC'

        cursor.execute(query, params)
        issues = cursor.fetchall()
        conn.close()
        return [dict(issue) for issue in issues]

    @staticmethod
    def get_by_id(issue_id, db_path='issue_tracker.db'):
        """Get issue by ID"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM issues WHERE id = ?', (issue_id,))
        issue = cursor.fetchone()
        conn.close()
        return dict(issue) if issue else None

    @staticmethod
    def update(issue_id, username, updates, db_path='issue_tracker.db'):
        """Update an issue and log all changes"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get current issue data
        cursor.execute('SELECT * FROM issues WHERE id = ?', (issue_id,))
        old_issue = dict(cursor.fetchone())

        # Update the issue
        update_fields = []
        values = []
        for field, new_value in updates.items():
            if field in old_issue and old_issue[field] != new_value:
                update_fields.append(f'{field} = ?')
                values.append(new_value)

                # Log each field change
                AuditLog.log_action(
                    username=username,
                    issue_id=issue_id,
                    action='Updated',
                    field_name=field,
                    old_value=str(old_issue[field]) if old_issue[field] is not None else None,
                    new_value=str(new_value) if new_value is not None else None,
                    conn=conn
                )

        if update_fields:
            # Add updated_at timestamp
            update_fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(issue_id)

            query = f'UPDATE issues SET {", ".join(update_fields)} WHERE id = ?'
            cursor.execute(query, values)

        conn.commit()
        conn.close()

    @staticmethod
    def delete(issue_id, username, db_path='issue_tracker.db'):
        """Delete an issue and log the deletion"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get issue data before deletion
        cursor.execute('SELECT * FROM issues WHERE id = ?', (issue_id,))
        issue = dict(cursor.fetchone())

        # Log the deletion
        AuditLog.log_action(
            username=username,
            issue_id=issue_id,
            action='Deleted',
            field_name='Issue',
            old_value=issue['title'],
            new_value=None,
            conn=conn
        )

        # Delete the issue
        cursor.execute('DELETE FROM issues WHERE id = ?', (issue_id,))

        conn.commit()
        conn.close()


class AuditLog:
    """Audit log model"""

    @staticmethod
    def log_action(username, issue_id, action, field_name, old_value, new_value, conn=None, db_path='issue_tracker.db'):
        """Log an action to the audit trail"""
        should_close = False
        if conn is None:
            conn = sqlite3.connect(db_path)
            should_close = True

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_log (username, issue_id, action, field_name, old_value, new_value)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, issue_id, action, field_name, old_value, new_value))

        if should_close:
            conn.commit()
            conn.close()

    @staticmethod
    def get_all(db_path='issue_tracker.db'):
        """Get all audit log entries"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM audit_log ORDER BY timestamp DESC')
        logs = cursor.fetchall()
        conn.close()
        return [dict(log) for log in logs]

    @staticmethod
    def get_by_issue(issue_id, db_path='issue_tracker.db'):
        """Get audit log entries for a specific issue"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM audit_log WHERE issue_id = ? ORDER BY timestamp DESC', (issue_id,))
        logs = cursor.fetchall()
        conn.close()
        return [dict(log) for log in logs]


class Document:
    """Document model for issue attachments"""

    @staticmethod
    def create(issue_id, filename, original_filename, file_size, uploaded_by, db_path='issue_tracker.db'):
        """Create a new document record"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO documents (issue_id, filename, original_filename, file_size, uploaded_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (issue_id, filename, original_filename, file_size, uploaded_by))

        document_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return document_id

    @staticmethod
    def get_by_issue(issue_id, db_path='issue_tracker.db'):
        """Get all documents for a specific issue"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM documents WHERE issue_id = ? ORDER BY uploaded_at DESC', (issue_id,))
        documents = cursor.fetchall()
        conn.close()
        return [dict(doc) for doc in documents]

    @staticmethod
    def get_by_id(document_id, db_path='issue_tracker.db'):
        """Get document by ID"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM documents WHERE id = ?', (document_id,))
        document = cursor.fetchone()
        conn.close()
        return dict(document) if document else None

    @staticmethod
    def delete(document_id, db_path='issue_tracker.db'):
        """Delete a document record"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM documents WHERE id = ?', (document_id,))
        conn.commit()
        conn.close()


class Company:
    """Company model"""

    @staticmethod
    def create(name, db_path='issue_tracker.db'):
        """Create a new company"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO companies (name) VALUES (?)', (name,))
            conn.commit()
            company_id = cursor.lastrowid
            conn.close()
            return company_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    @staticmethod
    def get_all(db_path='issue_tracker.db'):
        """Get all companies"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM companies ORDER BY name')
        companies = cursor.fetchall()
        conn.close()
        return [dict(company) for company in companies]

    @staticmethod
    def get_by_id(company_id, db_path='issue_tracker.db'):
        """Get company by ID"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM companies WHERE id = ?', (company_id,))
        company = cursor.fetchone()
        conn.close()
        return dict(company) if company else None

    @staticmethod
    def update(company_id, name, db_path='issue_tracker.db'):
        """Update company name"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('UPDATE companies SET name = ? WHERE id = ?', (name, company_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    @staticmethod
    def delete(company_id, db_path='issue_tracker.db'):
        """Delete a company"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM companies WHERE id = ?', (company_id,))
        conn.commit()
        conn.close()


class Department:
    """Department model"""

    @staticmethod
    def create(name, db_path='issue_tracker.db'):
        """Create a new department"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO departments (name) VALUES (?)', (name,))
            conn.commit()
            department_id = cursor.lastrowid
            conn.close()
            return department_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    @staticmethod
    def get_all(db_path='issue_tracker.db'):
        """Get all departments"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM departments ORDER BY name')
        departments = cursor.fetchall()
        conn.close()
        return [dict(dept) for dept in departments]

    @staticmethod
    def get_by_id(department_id, db_path='issue_tracker.db'):
        """Get department by ID"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM departments WHERE id = ?', (department_id,))
        department = cursor.fetchone()
        conn.close()
        return dict(department) if department else None

    @staticmethod
    def update(department_id, name, db_path='issue_tracker.db'):
        """Update department name"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('UPDATE departments SET name = ? WHERE id = ?', (name, department_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    @staticmethod
    def delete(department_id, db_path='issue_tracker.db'):
        """Delete a department"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM departments WHERE id = ?', (department_id,))
        conn.commit()
        conn.close()


class Application:
    """Application model"""

    @staticmethod
    def create(name, db_path='issue_tracker.db'):
        """Create a new application"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO applications (name) VALUES (?)', (name,))
            conn.commit()
            application_id = cursor.lastrowid
            conn.close()
            return application_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    @staticmethod
    def get_all(db_path='issue_tracker.db'):
        """Get all applications"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM applications ORDER BY name')
        applications = cursor.fetchall()
        conn.close()
        return [dict(app) for app in applications]

    @staticmethod
    def get_by_id(application_id, db_path='issue_tracker.db'):
        """Get application by ID"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM applications WHERE id = ?', (application_id,))
        application = cursor.fetchone()
        conn.close()
        return dict(application) if application else None

    @staticmethod
    def update(application_id, name, db_path='issue_tracker.db'):
        """Update application name"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('UPDATE applications SET name = ? WHERE id = ?', (name, application_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    @staticmethod
    def delete(application_id, db_path='issue_tracker.db'):
        """Delete an application"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM applications WHERE id = ?', (application_id,))
        conn.commit()
        conn.close()
