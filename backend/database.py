import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = 'notion.db'

def get_db_connection():
    """Create and return a database connection with proper configuration."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Failed to connect to database: {e}")

@contextmanager
def get_db():
    """Context manager for database connections with automatic commit/rollback."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize the database with schema on first run."""
    if os.path.exists(DATABASE_PATH):
        print(f"Database already exists at {DATABASE_PATH}")
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create folders table
        cursor.execute('''
            CREATE TABLE folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                parent_folder_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (parent_folder_id) REFERENCES folders(id) ON DELETE CASCADE
            )
        ''')
        
        # Create documents table
        cursor.execute('''
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                folder_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE SET NULL
            )
        ''')
        
        # Create blocks table
        cursor.execute('''
            CREATE TABLE blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                block_type TEXT NOT NULL DEFAULT 'paragraph',
                order_index INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes for foreign keys and frequently queried columns
        cursor.execute('CREATE INDEX idx_folders_user_id ON folders(user_id)')
        cursor.execute('CREATE INDEX idx_folders_parent_id ON folders(parent_folder_id)')
        cursor.execute('CREATE INDEX idx_documents_user_id ON documents(user_id)')
        cursor.execute('CREATE INDEX idx_documents_folder_id ON documents(folder_id)')
        cursor.execute('CREATE INDEX idx_blocks_document_id ON blocks(document_id)')
        cursor.execute('CREATE INDEX idx_blocks_order ON blocks(document_id, order_index)')
        
        conn.commit()
        print(f"Database initialized successfully at {DATABASE_PATH}")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
