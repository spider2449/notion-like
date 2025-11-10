"""Migration to add is_admin column to users table."""
import sqlite3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import get_db_connection, DATABASE_PATH

def migrate():
    """Add is_admin column to users table."""
    if not os.path.exists(DATABASE_PATH):
        print("Database does not exist. Run init_db first.")
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("is_admin column already exists")
            conn.close()
            return
        
        # Add is_admin column
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
        
        conn.commit()
        print("Successfully added is_admin column to users table")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
