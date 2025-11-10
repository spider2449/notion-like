from flask import Blueprint, request, jsonify, g
from backend.middleware.auth_middleware import require_auth
from backend.services.block_service import BlockService

bp = Blueprint('blocks', __name__, url_prefix='/api')

@bp.route('/documents/<int:document_id>/blocks', methods=['GET'])
@require_auth
def get_blocks(document_id):
    """Get all blocks for a document."""
    try:
        blocks = BlockService.get_blocks_by_document(document_id, g.user_id)
        return jsonify({
            'blocks': [block.to_dict() for block in blocks]
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/blocks', methods=['POST'])
@require_auth
def create_block():
    """Create a new block."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        document_id = data.get('document_id')
        content = data.get('content', '')
        block_type = data.get('block_type', 'paragraph')
        
        if not document_id:
            return jsonify({'error': 'document_id is required'}), 400
        
        block = BlockService.create_block(document_id, g.user_id, content, block_type)
        
        return jsonify({
            'message': 'Block created successfully',
            'block': block.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/blocks/<int:block_id>', methods=['PUT'])
@require_auth
def update_block(block_id):
    """Update a block."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        content = data.get('content')
        block_type = data.get('block_type')
        
        block = BlockService.update_block(block_id, g.user_id, content, block_type)
        
        return jsonify({
            'message': 'Block updated successfully',
            'block': block.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/blocks/<int:block_id>', methods=['DELETE'])
@require_auth
def delete_block(block_id):
    """Delete a block."""
    try:
        BlockService.delete_block(block_id, g.user_id)
        
        return jsonify({'message': 'Block deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/documents/<int:document_id>/blocks/reorder', methods=['PUT'])
@require_auth
def reorder_blocks(document_id):
    """Reorder blocks in a document."""
    try:
        data = request.get_json()
        
        if not data or 'blocks' not in data:
            return jsonify({'error': 'blocks array is required'}), 400
        
        block_order_list = data['blocks']
        
        BlockService.reorder_blocks(document_id, g.user_id, block_order_list)
        
        return jsonify({'message': 'Blocks reordered successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
