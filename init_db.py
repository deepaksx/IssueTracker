"""
Database initialization script for IT Issue Tracker
Run this script to set up the database and create default users
"""
from models import Database, User


def init_database():
    """Initialize database and create default users"""
    print("Initializing database...")

    # Create database tables
    db = Database()
    db.init_db()
    print("Database tables created successfully.")

    # Create default admin user
    admin_id = User.create(username='admin', password='admin123', role='admin')
    if admin_id:
        print("Default admin user created successfully")
    else:
        print("Admin user already exists.")

    # Create default viewer user
    viewer_id = User.create(username='viewer', password='viewer123', role='viewer')
    if viewer_id:
        print("Default viewer user created successfully")
    else:
        print("Viewer user already exists.")

    print("\n" + "="*60)
    print("Database initialization complete!")
    print("="*60)
    print("\n*** IMPORTANT SECURITY NOTICE ***")
    print("Default users have been created with standard credentials.")
    print("Please refer to the documentation for login information.")
    print("Change all default passwords immediately after first login!")
    print("="*60)


if __name__ == '__main__':
    init_database()
