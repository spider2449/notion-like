from backend.database import get_db
from backend.models.document import Document

class DocumentRepository:
    """Repository for document data access."""
    
    @staticmethod
    def create(user_id, title, folder_id=None):
        """Create a new document."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO documents (user_id, title, folder_id) 
                   VALUES (?, ?, ?)''',
                (user_id, title, folder_id)
            )
            document_id = cursor.lastrowid
            
            cursor.execute('SELECT * FROM documents WHERE id = ?', (document_id,))
            row = cursor.fetchone()
            return Document.from_row(row)
    
    @staticmethod
    def find_by_id(document_id):
        """Find document by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM documents WHERE id = ?', (document_id,))
            row = cursor.fetchone()
            return Document.from_row(row)
    
    @staticmethod
    def find_by_user(user_id):
        """Find all documents for a user."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM documents WHERE user_id = ?', (user_id,))
            rows = cursor.fetchall()
            return [Document.from_row(row) for row in rows]
    
    @staticmethod
    def update(document_id, title=None, folder_id=None):
        """Update document."""
        with get_db() as conn:
            cursor = conn.cursor()
            if title is not None:
                cursor.execute(
                    'UPDATE documents SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (title, document_id)
                )
            if folder_id is not None:
                cursor.execute(
                    'UPDATE documents SET folder_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (folder_id, document_id)
                )
            
            cursor.execute('SELECT * FROM documents WHERE id = ?', (document_id,))
            row = cursor.fetchone()
            return Document.from_row(row)
    
    @staticmethod
    def delete(document_id):
        """Delete document."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM documents WHERE id = ?', (document_id,))
            return cursor.rowcount > 0
