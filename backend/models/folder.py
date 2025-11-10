from datetime import datetime

class Folder:
    """Folder model representing a folder for organizing documents."""
    
    def __init__(self, id=None, user_id=None, name=None, parent_folder_id=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.parent_folder_id = parent_folder_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert folder to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'parent_folder_id': self.parent_folder_id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    
    @staticmethod
    def from_row(row):
        """Create Folder instance from database row."""
        if row is None:
            return None
        return Folder(
            id=row['id'],
            user_id=row['user_id'],
            name=row['name'],
            parent_folder_id=row['parent_folder_id'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
