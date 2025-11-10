from datetime import datetime

class User:
    """User model representing a user account."""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 is_admin=False, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert user to dictionary (excluding password_hash)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    
    @staticmethod
    def from_row(row):
        """Create User instance from database row."""
        if row is None:
            return None
        
        # Handle is_admin field - check if it exists in the row
        try:
            is_admin = bool(row['is_admin']) if 'is_admin' in row.keys() else False
        except (KeyError, IndexError):
            is_admin = False
        
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            is_admin=is_admin,
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
