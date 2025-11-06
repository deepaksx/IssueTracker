"""
Database schema migration script
Rebuilds the issues table with correct CHECK constraints while preserving all data
"""
import sqlite3
import sys

def migrate_database(db_path='issue_tracker.db'):
    """Migrate database schema to fix CHECK constraints"""
    print(f"Starting migration for {db_path}...")

    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Check if migration is needed
        cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'Open'")
        open_count = cursor.fetchone()[0]

        if open_count == 0:
            print("✓ No migration needed - no 'Open' status issues found")
            conn.close()
            return True

        print(f"Found {open_count} issues with 'Open' status")
        print("Starting schema migration...")

        # Step 1: Create new table with correct schema
        print("1. Creating new issues table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issues_new (
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

        # Step 2: Copy all data, converting 'Open' to 'Not Started'
        print("2. Copying data and converting 'Open' to 'Not Started'...")
        cursor.execute('''
            INSERT INTO issues_new
                (id, title, description, company, department, application,
                 category, priority, status, assigned_to, created_by, created_at, updated_at)
            SELECT
                id, title, description, company, department, application,
                category, priority,
                CASE WHEN status = 'Open' THEN 'Not Started' ELSE status END,
                assigned_to, created_by, created_at, updated_at
            FROM issues
        ''')

        rows_copied = cursor.rowcount
        print(f"✓ Copied {rows_copied} issues")

        # Step 3: Drop old table
        print("3. Dropping old issues table...")
        cursor.execute('DROP TABLE issues')

        # Step 4: Rename new table
        print("4. Renaming new table to issues...")
        cursor.execute('ALTER TABLE issues_new RENAME TO issues')

        # Step 5: Commit changes
        conn.commit()
        print("✓ Migration completed successfully!")
        print(f"✓ Converted {open_count} issues from 'Open' to 'Not Started'")

        conn.close()
        return True

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'issue_tracker.db'
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
