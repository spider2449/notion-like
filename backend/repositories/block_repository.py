from backend.database import get_db
from backend.models.block import Block

class BlockRepository:
    """Repository for block data access."""
    
    @staticmethod
    def create(document_id, content='', block_type='paragraph', order_index=0):
        """Create a new block."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO blocks (document_id, content, block_type, order_index) 
                   VALUES (?, ?, ?, ?)''',
                (document_id, content, block_type, order_index)
            )
            block_id = cursor.lastrowid
            
            cursor.execute('SELECT * FROM blocks WHERE id = ?', (block_id,))
            row = cursor.fetchone()
            return Block.from_row(row)
    
    @staticmethod
    def find_by_id(block_id):
        """Find block by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM blocks WHERE id = ?', (block_id,))
            row = cursor.fetchone()
            return Block.from_row(row)
    
    @staticmethod
    def find_by_document(document_id):
        """Find all blocks for a document ordered by order_index."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM blocks WHERE document_id = ? ORDER BY order_index ASC',
                (document_id,)
            )
            rows = cursor.fetchall()
            return [Block.from_row(row) for row in rows]
    
    @staticmethod
    def update(block_id, content=None, block_type=None):
        """Update block content and/or type."""
        with get_db() as conn:
            cursor = conn.cursor()
            
            if content is not None and block_type is not None:
                cursor.execute(
                    '''UPDATE blocks SET content = ?, block_type = ?, 
                       updated_at = CURRENT_TIMESTAMP WHERE id = ?''',
                    (content, block_type, block_id)
                )
            elif content is not None:
                cursor.execute(
                    'UPDATE blocks SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (content, block_id)
                )
            elif block_type is not None:
                cursor.execute(
                    'UPDATE blocks SET block_type = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (block_type, block_id)
                )
            
            cursor.execute('SELECT * FROM blocks WHERE id = ?', (block_id,))
            row = cursor.fetchone()
            return Block.from_row(row)
    
    @staticmethod
    def delete(block_id):
        """Delete block."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM blocks WHERE id = ?', (block_id,))
            return cursor.rowcount > 0
    
    @staticmethod
    def reorder_blocks(block_orders):
        """Update order_index for multiple blocks.
        
        Args:
            block_orders: List of tuples (block_id, new_order_index)
        """
        with get_db() as conn:
            cursor = conn.cursor()
            for block_id, order_index in block_orders:
                cursor.execute(
                    'UPDATE blocks SET order_index = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (order_index, block_id)
                )
    
    @staticmethod
    def get_max_order_index(document_id):
        """Get the maximum order_index for a document."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT MAX(order_index) as max_order FROM blocks WHERE document_id = ?',
                (document_id,)
            )
            row = cursor.fetchone()
            return row['max_order'] if row['max_order'] is not None else -1
