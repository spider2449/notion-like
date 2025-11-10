from flask import Blueprint, request, jsonify, g
from backend.services.account_service import AccountService
from backend.middleware.auth_middleware import require_auth

bp = Blueprint('account', __name__, url_prefix='/api/account')

@bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get current user's profile."""
    try:
        profile = AccountService.get_user_profile(g.user_id)
        return jsonify(profile), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/username', methods=['PUT'])
@require_auth
def update_username():
    """Update user's username."""
    try:
        data = request.get_json()
        if not data or 'username' not in data:
            return jsonify({'error': 'Username is required'}), 400
        
        user = AccountService.update_username(g.user_id, data['username'])
        return jsonify({
            'message': 'Username updated successfully',
            'user': user.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/email', methods=['PUT'])
@require_auth
def update_email():
    """Update user's email."""
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        user = AccountService.update_email(g.user_id, data['email'])
        return jsonify({
            'message': 'Email updated successfully',
            'user': user.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/password', methods=['PUT'])
@require_auth
def update_password():
    """Update user's password."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password:
            return jsonify({'error': 'Current password is required'}), 400
        if not new_password:
            return jsonify({'error': 'New password is required'}), 400
        
        AccountService.update_password(g.user_id, current_password, new_password)
        return jsonify({'message': 'Password updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/delete', methods=['DELETE'])
@require_auth
def delete_account():
    """Delete user account."""
    try:
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        AccountService.delete_account(g.user_id, data['password'])
        return jsonify({'message': 'Account deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
