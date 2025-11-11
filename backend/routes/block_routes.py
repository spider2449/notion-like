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

@bp.route('/upload/image', methods=['POST'])
@require_auth
def upload_image():
    """Upload an image file."""
    try:
        print(f"Upload request received from user {g.user_id}")
        print(f"Files in request: {list(request.files.keys())}")
        
        if 'image' not in request.files:
            print("Error: No 'image' field in request.files")
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Error: Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        print(f"File extension: {file_ext}")
        
        if file_ext not in allowed_extensions:
            print(f"Error: Invalid extension {file_ext}")
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp, svg'}), 400
        
        # Generate unique filename
        import uuid
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        print(f"Generated unique filename: {unique_filename}")
        
        # Save file
        from flask import current_app
        import os
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        print(f"Saving to: {filepath}")
        
        file.save(filepath)
        print(f"File saved successfully")
        
        # Return URL
        image_url = f"/uploads/{unique_filename}"
        print(f"Returning URL: {image_url}")
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'url': image_url
        }), 200
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500
