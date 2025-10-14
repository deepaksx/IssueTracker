"""
Database Migration Script - Add Documents Table
This script adds the documents table to existing databases
"""
import sqlite3
import os

def migrate_database():
    """Add documents table to existing database"""
    db_path = 'issue_tracker.db'

    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found!")
        print("No migration needed - database will be created with documents table on first run.")
        return

    print("Starting database migration...")
    print(f"Database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if documents table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
    if cursor.fetchone():
        print("✓ Documents table already exists. No migration needed.")
        conn.close()
        return

    # Create documents table
    print("Creating documents table...")
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

    conn.commit()
    print("✓ Documents table created successfully!")

    # Create uploads directory if it doesn't exist
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✓ Created '{uploads_dir}' directory for file storage")
    else:
        print(f"✓ Uploads directory already exists: {uploads_dir}")

    conn.close()
    print("\nMigration completed successfully!")
    print("You can now upload PDF documents to issues.")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Database Migration - Add Documents Support")
    print("="*60 + "\n")

    migrate_database()

    print("\n" + "="*60)
    print("Migration Complete!")
    print("="*60 + "\n")
