from backend.database import get_db
from backend.models.user import User

class UserRepository:
    """Repository for user data access."""
    
    @staticmethod
    def create(username, email, password_hash, is_admin=False):
        """Create a new user with parameterized query."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO users (username, email, password_hash, is_admin) 
                   VALUES (?, ?, ?, ?)''',
                (username, email, password_hash, 1 if is_admin else 0)
            )
            user_id = cursor.lastrowid
            
            # Fetch the created user
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return User.from_row(row)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email using parameterized query."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            return User.from_row(row)
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID using parameterized query."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return User.from_row(row)
    
    @staticmethod
    def find_by_username(username):
        """Find user by username using parameterized query."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return User.from_row(row)
    
    @staticmethod
    def update_username(user_id, username):
        """Update user's username."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET username = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (username, user_id)
            )
    
    @staticmethod
    def update_email(user_id, email):
        """Update user's email."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (email, user_id)
            )
    
    @staticmethod
    def update_password(user_id, password_hash):
        """Update user's password hash."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (password_hash, user_id)
            )
    
    @staticmethod
    def delete(user_id):
        """Delete user account."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

    @staticmethod
    def find_all():
        """Get all users."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [User.from_row(row) for row in rows]
    
    @staticmethod
    def update_admin_status(user_id, is_admin):
        """Update user's admin status."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET is_admin = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (1 if is_admin else 0, user_id)
            )
