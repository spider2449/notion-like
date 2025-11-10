from datetime import datetime

class Block:
    """Block model representing a content block."""
    
    def __init__(self, id=None, document_id=None, content='', block_type='paragraph',
                 order_index=0, created_at=None, updated_at=None):
        self.id = id
        self.document_id = document_id
        self.content = content
        self.block_type = block_type
        self.order_index = order_index
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert block to dictionary."""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'content': self.content,
            'block_type': self.block_type,
            'order_index': self.order_index,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    
    @staticmethod
    def from_row(row):
        """Create Block instance from database row."""
        if row is None:
            return None
        return Block(
            id=row['id'],
            document_id=row['document_id'],
            content=row['content'],
            block_type=row['block_type'],
            order_index=row['order_index'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
