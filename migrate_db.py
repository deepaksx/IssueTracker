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
        # Migrate USERS table
        print("\n--- Migrating USERS table ---")
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [column[1] for column in cursor.fetchall()]

        # Add company column to users if it doesn't exist
        if 'company' not in user_columns:
            print("Adding 'company' column to users table...")
            cursor.execute('ALTER TABLE users ADD COLUMN company TEXT')
            print("✓ Added 'company' column to users")
        else:
            print("✓ 'company' column already exists in users")

        # Add department column to users if it doesn't exist
        if 'department' not in user_columns:
            print("Adding 'department' column to users table...")
            cursor.execute('ALTER TABLE users ADD COLUMN department TEXT')
            print("✓ Added 'department' column to users")
        else:
            print("✓ 'department' column already exists in users")

        # Migrate ISSUES table
        print("\n--- Migrating ISSUES table ---")
        cursor.execute("PRAGMA table_info(issues)")
        issue_columns = [column[1] for column in cursor.fetchall()]

        # Add company column if it doesn't exist
        if 'company' not in issue_columns:
            print("Adding 'company' column to issues table...")
            cursor.execute('ALTER TABLE issues ADD COLUMN company TEXT')
            print("✓ Added 'company' column to issues")
        else:
            print("✓ 'company' column already exists in issues")

        # Add department column if it doesn't exist
        if 'department' not in issue_columns:
            print("Adding 'department' column to issues table...")
            cursor.execute('ALTER TABLE issues ADD COLUMN department TEXT')
            print("✓ Added 'department' column to issues")
        else:
            print("✓ 'department' column already exists in issues")

        # Add application column if it doesn't exist
        if 'application' not in issue_columns:
            print("Adding 'application' column to issues table...")
            cursor.execute('ALTER TABLE issues ADD COLUMN application TEXT')
            print("✓ Added 'application' column to issues")
        else:
            print("✓ 'application' column already exists in issues")

        conn.commit()
        print("\n" + "="*60)
        print("Migration completed successfully!")
        print("="*60)
        print("\nYour existing data has been preserved.")
        print("Both users and issues tables have been updated.")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        print("Please check the error and try again.")
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
