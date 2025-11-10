from flask import Blueprint, request, jsonify, g
from backend.middleware.auth_middleware import require_auth
from backend.services.document_service import DocumentService

bp = Blueprint('documents', __name__, url_prefix='/api')

@bp.route('/documents', methods=['GET'])
@require_auth
def get_documents():
    """Get all documents and folders for authenticated user."""
    try:
        result = DocumentService.get_user_documents(g.user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/documents/<int:document_id>', methods=['GET'])
@require_auth
def get_document(document_id):
    """Get a single document."""
    try:
        document = DocumentService.get_document(document_id, g.user_id)
        return jsonify({'document': document.to_dict()}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/documents', methods=['POST'])
@require_auth
def create_document():
    """Create a new document."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        title = data.get('title')
        folder_id = data.get('folder_id')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        document = DocumentService.create_document(g.user_id, title, folder_id)
        
        return jsonify({
            'message': 'Document created successfully',
            'document': document.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/documents/<int:document_id>', methods=['PUT'])
@require_auth
def update_document(document_id):
    """Update a document."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        title = data.get('title')
        folder_id = data.get('folder_id')
        
        document = DocumentService.update_document(document_id, g.user_id, title, folder_id)
        
        return jsonify({
            'message': 'Document updated successfully',
            'document': document.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/documents/<int:document_id>', methods=['DELETE'])
@require_auth
def delete_document(document_id):
    """Delete a document."""
    try:
        DocumentService.delete_document(document_id, g.user_id)
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/folders', methods=['POST'])
@require_auth
def create_folder():
    """Create a new folder."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        name = data.get('name')
        parent_folder_id = data.get('parent_folder_id')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        folder = DocumentService.create_folder(g.user_id, name, parent_folder_id)
        
        return jsonify({
            'message': 'Folder created successfully',
            'folder': folder.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/folders/<int:folder_id>', methods=['DELETE'])
@require_auth
def delete_folder(folder_id):
    """Delete a folder."""
    try:
        DocumentService.delete_folder(folder_id, g.user_id)
        
        return jsonify({'message': 'Folder deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError:
        return jsonify({'error': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
