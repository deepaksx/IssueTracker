"""
Command-line user management tool for IT Issue Tracker
Use this script to manage users from the command line
"""
from models import User
import sys


def list_users():
    """List all users"""
    users = User.get_all()
    print("\n" + "="*60)
    print("USER LIST")
    print("="*60)
    print(f"{'ID':<5} {'Username':<20} {'Role':<10} {'Created At'}")
    print("-"*60)
    for user in users:
        print(f"{user['id']:<5} {user['username']:<20} {user['role']:<10} {user['created_at']}")
    print("="*60)
    print(f"Total users: {len(users)}\n")


def create_user():
    """Create a new user"""
    print("\n" + "="*60)
    print("CREATE NEW USER")
    print("="*60)

    username = input("Enter username: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return

    password = input("Enter password (min 6 characters): ").strip()
    if len(password) < 6:
        print("❌ Password must be at least 6 characters")
        return

    print("\nRoles:")
    print("  1. Viewer (Read-only access)")
    print("  2. Admin (Full access)")
    role_choice = input("Enter role (1 or 2): ").strip()

    if role_choice == '1':
        role = 'viewer'
    elif role_choice == '2':
        role = 'admin'
    else:
        print("❌ Invalid role selection")
        return

    user_id = User.create(username=username, password=password, role=role)

    if user_id:
        print(f"\n✓ User '{username}' created successfully (ID: {user_id})")
        print(f"  Role: {role}")
    else:
        print(f"\n❌ Failed to create user. Username '{username}' may already exist.")


def delete_user():
    """Delete a user"""
    print("\n" + "="*60)
    print("DELETE USER")
    print("="*60)

    list_users()

    user_id = input("Enter user ID to delete (or 'cancel' to abort): ").strip()

    if user_id.lower() == 'cancel':
        print("Cancelled")
        return

    try:
        user_id = int(user_id)
    except ValueError:
        print("❌ Invalid user ID")
        return

    user = User.get_by_id(user_id)
    if not user:
        print(f"❌ User with ID {user_id} not found")
        return

    confirm = input(f"Are you sure you want to delete '{user['username']}'? (yes/no): ").strip().lower()

    if confirm == 'yes':
        User.delete(user_id)
        print(f"✓ User '{user['username']}' deleted successfully")
    else:
        print("Cancelled")


def change_password():
    """Change user password"""
    print("\n" + "="*60)
    print("CHANGE USER PASSWORD")
    print("="*60)

    list_users()

    user_id = input("Enter user ID (or 'cancel' to abort): ").strip()

    if user_id.lower() == 'cancel':
        print("Cancelled")
        return

    try:
        user_id = int(user_id)
    except ValueError:
        print("❌ Invalid user ID")
        return

    user = User.get_by_id(user_id)
    if not user:
        print(f"❌ User with ID {user_id} not found")
        return

    new_password = input(f"Enter new password for '{user['username']}' (min 6 characters): ").strip()

    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters")
        return

    success = User.update(user_id=user_id, password=new_password)

    if success:
        print(f"✓ Password changed successfully for '{user['username']}'")
    else:
        print("❌ Failed to change password")


def change_role():
    """Change user role"""
    print("\n" + "="*60)
    print("CHANGE USER ROLE")
    print("="*60)

    list_users()

    user_id = input("Enter user ID (or 'cancel' to abort): ").strip()

    if user_id.lower() == 'cancel':
        print("Cancelled")
        return

    try:
        user_id = int(user_id)
    except ValueError:
        print("❌ Invalid user ID")
        return

    user = User.get_by_id(user_id)
    if not user:
        print(f"❌ User with ID {user_id} not found")
        return

    print(f"\nCurrent role for '{user['username']}': {user['role']}")
    print("\nRoles:")
    print("  1. Viewer (Read-only access)")
    print("  2. Admin (Full access)")
    role_choice = input("Enter new role (1 or 2): ").strip()

    if role_choice == '1':
        new_role = 'viewer'
    elif role_choice == '2':
        new_role = 'admin'
    else:
        print("❌ Invalid role selection")
        return

    success = User.update(user_id=user_id, role=new_role)

    if success:
        print(f"✓ Role changed successfully for '{user['username']}' to '{new_role}'")
    else:
        print("❌ Failed to change role")


def main_menu():
    """Display main menu"""
    while True:
        print("\n" + "="*60)
        print("IT ISSUE TRACKER - USER MANAGEMENT")
        print("="*60)
        print("1. List all users")
        print("2. Create new user")
        print("3. Delete user")
        print("4. Change user password")
        print("5. Change user role")
        print("6. Exit")
        print("="*60)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            list_users()
        elif choice == '2':
            create_user()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            change_password()
        elif choice == '5':
            change_role()
        elif choice == '6':
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
