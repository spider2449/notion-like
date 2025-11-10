from datetime import datetime

class Document:
    """Document model representing a user document."""
    
    def __init__(self, id=None, user_id=None, title=None, folder_id=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.folder_id = folder_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert document to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'folder_id': self.folder_id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    
    @staticmethod
    def from_row(row):
        """Create Document instance from database row."""
        if row is None:
            return None
        return Document(
            id=row['id'],
            user_id=row['user_id'],
            title=row['title'],
            folder_id=row['folder_id'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
