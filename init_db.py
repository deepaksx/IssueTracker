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
        print(f"Admin user created: username='admin', password='admin123'")
    else:
        print("Admin user already exists.")

    # Create default viewer user
    viewer_id = User.create(username='viewer', password='viewer123', role='viewer')
    if viewer_id:
        print(f"Viewer user created: username='viewer', password='viewer123'")
    else:
        print("Viewer user already exists.")

    print("\n" + "="*60)
    print("Database initialization complete!")
    print("="*60)
    print("\nDefault credentials:")
    print("  Admin:  username='admin'  password='admin123'")
    print("  Viewer: username='viewer' password='viewer123'")
    print("\n*** IMPORTANT: Change these passwords in production! ***")
    print("="*60)


if __name__ == '__main__':
    init_database()
