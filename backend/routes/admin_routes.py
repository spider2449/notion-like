from flask import Blueprint, request, jsonify
from backend.services.admin_service import AdminService
from backend.middleware.admin_middleware import require_admin

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/users', methods=['GET'])
@require_admin
def get_all_users():
    """Get all users (admin only)."""
    try:
        users = AdminService.get_all_users()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    """Get user by ID (admin only)."""
    try:
        user = AdminService.get_user_by_id(user_id)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users', methods=['POST'])
@require_admin
def create_user():
    """Create a new user (admin only)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_admin = data.get('is_admin', False)
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        user = AdminService.create_user(username, email, password, is_admin)
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>/admin', methods=['PUT'])
@require_admin
def update_admin_status(user_id):
    """Update user's admin status (admin only)."""
    try:
        data = request.get_json()
        if not data or 'is_admin' not in data:
            return jsonify({'error': 'is_admin field is required'}), 400
        
        user = AdminService.update_user_admin_status(user_id, data['is_admin'])
        return jsonify({
            'message': 'Admin status updated successfully',
            'user': user.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Delete a user (admin only)."""
    try:
        AdminService.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/statistics', methods=['GET'])
@require_admin
def get_statistics():
    """Get user statistics (admin only)."""
    try:
        stats = AdminService.get_user_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
