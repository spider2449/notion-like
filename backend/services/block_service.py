from backend.repositories.block_repository import BlockRepository
from backend.repositories.document_repository import DocumentRepository
from backend.utils.security import sanitize_input

VALID_BLOCK_TYPES = ['paragraph', 'heading1', 'heading2', 'heading3', 
                     'bullet_list', 'numbered_list', 'code', 'quote', 
                     'callout', 'toggle', 'divider']

class BlockService:
    """Service for block operations."""
    
    @staticmethod
    def create_block(document_id, user_id, content='', block_type='paragraph'):
        """Create a new block with automatic order_index assignment."""
        # Sanitize content
        content = sanitize_input(content)
        
        # Verify document exists and user owns it
        document = DocumentRepository.find_by_id(document_id)
        if not document:
            raise ValueError('Document not found')
        if document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        # Validate block type
        if block_type not in VALID_BLOCK_TYPES:
            raise ValueError(f'Invalid block type. Must be one of: {", ".join(VALID_BLOCK_TYPES)}')
        
        # Get next order_index
        max_order = BlockRepository.get_max_order_index(document_id)
        order_index = max_order + 1
        
        return BlockRepository.create(document_id, content, block_type, order_index)
    
    @staticmethod
    def update_block(block_id, user_id, content=None, block_type=None):
        """Update block content and/or type."""
        # Sanitize content if provided
        if content is not None:
            content = sanitize_input(content)
        
        # Verify block exists
        block = BlockRepository.find_by_id(block_id)
        if not block:
            raise ValueError('Block not found')
        
        # Verify user owns the document
        document = DocumentRepository.find_by_id(block.document_id)
        if not document or document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        # Validate block type if provided
        if block_type and block_type not in VALID_BLOCK_TYPES:
            raise ValueError(f'Invalid block type. Must be one of: {", ".join(VALID_BLOCK_TYPES)}')
        
        return BlockRepository.update(block_id, content, block_type)
    
    @staticmethod
    def delete_block(block_id, user_id):
        """Delete a block."""
        # Verify block exists
        block = BlockRepository.find_by_id(block_id)
        if not block:
            raise ValueError('Block not found')
        
        # Verify user owns the document
        document = DocumentRepository.find_by_id(block.document_id)
        if not document or document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        return BlockRepository.delete(block_id)
    
    @staticmethod
    def get_blocks_by_document(document_id, user_id):
        """Get all blocks for a document."""
        # Verify document exists and user owns it
        document = DocumentRepository.find_by_id(document_id)
        if not document:
            raise ValueError('Document not found')
        if document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        return BlockRepository.find_by_document(document_id)
    
    @staticmethod
    def reorder_blocks(document_id, user_id, block_order_list):
        """Update order_index for multiple blocks.
        
        Args:
            document_id: ID of the document
            user_id: ID of the user
            block_order_list: List of dicts with 'id' and 'order_index'
        """
        # Verify document exists and user owns it
        document = DocumentRepository.find_by_id(document_id)
        if not document:
            raise ValueError('Document not found')
        if document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        # Verify all blocks belong to this document
        for item in block_order_list:
            block = BlockRepository.find_by_id(item['id'])
            if not block or block.document_id != document_id:
                raise ValueError(f'Block {item["id"]} does not belong to this document')
        
        # Update order
        block_orders = [(item['id'], item['order_index']) for item in block_order_list]
        BlockRepository.reorder_blocks(block_orders)
