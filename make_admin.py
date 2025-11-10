#!/usr/bin/env python3
"""Script to make a user an admin."""
import sys
from backend.database import get_db_connection

def make_admin(email):
    """Make a user admin by email."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id, username, email, is_admin FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User with email '{email}' not found")
            conn.close()
            return False
        
        user_id, username, user_email, is_admin = user['id'], user['username'], user['email'], user['is_admin']
        
        if is_admin:
            print(f"✓ User '{username}' ({user_email}) is already an admin")
            conn.close()
            return True
        
        # Make user admin
        cursor.execute('UPDATE users SET is_admin = 1 WHERE id = ?', (user_id,))
        conn.commit()
        
        print(f"✓ Successfully granted admin privileges to '{username}' ({user_email})")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_users():
    """List all users."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, email, is_admin FROM users ORDER BY id')
        users = cursor.fetchall()
        
        if not users:
            print("No users found")
            conn.close()
            return
        
        print("\nCurrent users:")
        print("-" * 70)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Admin':<10}")
        print("-" * 70)
        
        for user in users:
            admin_status = "Yes" if user['is_admin'] else "No"
            print(f"{user['id']:<5} {user['username']:<20} {user['email']:<30} {admin_status:<10}")
        
        print("-" * 70)
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("=" * 70)
    print("Admin User Management")
    print("=" * 70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python make_admin.py <email>          - Make user admin")
        print("  python make_admin.py --list           - List all users")
        print("\nExample:")
        print("  python make_admin.py test@example.com")
        print("=" * 70)
        sys.exit(1)
    
    if sys.argv[1] == '--list':
        list_users()
    else:
        email = sys.argv[1]
        make_admin(email)
