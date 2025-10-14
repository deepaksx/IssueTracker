"""
Database migration script to add company, department, and application fields
Run this to update your existing database without losing data
"""
import sqlite3

def migrate_database():
    """Add new columns to existing database"""
    print("Starting database migration...")

    conn = sqlite3.connect('issue_tracker.db')
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(issues)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add company column if it doesn't exist
        if 'company' not in columns:
            print("Adding 'company' column...")
            cursor.execute('ALTER TABLE issues ADD COLUMN company TEXT')
            print("✓ Added 'company' column")
        else:
            print("✓ 'company' column already exists")

        # Add department column if it doesn't exist
        if 'department' not in columns:
            print("Adding 'department' column...")
            cursor.execute('ALTER TABLE issues ADD COLUMN department TEXT')
            print("✓ Added 'department' column")
        else:
            print("✓ 'department' column already exists")

        # Add application column if it doesn't exist
        if 'application' not in columns:
            print("Adding 'application' column...")
            cursor.execute('ALTER TABLE issues ADD COLUMN application TEXT')
            print("✓ Added 'application' column")
        else:
            print("✓ 'application' column already exists")

        conn.commit()
        print("\n" + "="*60)
        print("Migration completed successfully!")
        print("="*60)
        print("\nYour existing data has been preserved.")
        print("You can now add Company, Department, and Application to issues.")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        print("Please check the error and try again.")
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
