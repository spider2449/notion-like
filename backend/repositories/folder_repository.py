from backend.database import get_db
from backend.models.folder import Folder

class FolderRepository:
    """Repository for folder data access."""
    
    @staticmethod
    def create(user_id, name, parent_folder_id=None):
        """Create a new folder."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO folders (user_id, name, parent_folder_id) 
                   VALUES (?, ?, ?)''',
                (user_id, name, parent_folder_id)
            )
            folder_id = cursor.lastrowid
            
            cursor.execute('SELECT * FROM folders WHERE id = ?', (folder_id,))
            row = cursor.fetchone()
            return Folder.from_row(row)
    
    @staticmethod
    def find_by_id(folder_id):
        """Find folder by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM folders WHERE id = ?', (folder_id,))
            row = cursor.fetchone()
            return Folder.from_row(row)
    
    @staticmethod
    def find_by_user(user_id):
        """Find all folders for a user."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM folders WHERE user_id = ?', (user_id,))
            rows = cursor.fetchall()
            return [Folder.from_row(row) for row in rows]
    
    @staticmethod
    def update(folder_id, name=None, parent_folder_id=None):
        """Update folder."""
        with get_db() as conn:
            cursor = conn.cursor()
            if name is not None:
                cursor.execute(
                    'UPDATE folders SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (name, folder_id)
                )
            if parent_folder_id is not None:
                cursor.execute(
                    'UPDATE folders SET parent_folder_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (parent_folder_id, folder_id)
                )
            
            cursor.execute('SELECT * FROM folders WHERE id = ?', (folder_id,))
            row = cursor.fetchone()
            return Folder.from_row(row)
    
    @staticmethod
    def delete(folder_id):
        """Delete folder."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM folders WHERE id = ?', (folder_id,))
            return cursor.rowcount > 0
