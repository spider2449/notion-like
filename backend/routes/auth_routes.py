from flask import Blueprint, request, jsonify
from backend.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Register user
        user = AuthService.register_user(username, email, password)
        
        # Generate token
        token = AuthService.generate_token(user.id, user.email)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Authenticate user
        result = AuthService.authenticate_user(username, password)
        
        return jsonify({
            'message': 'Login successful',
            'token': result['token'],
            'user': result['user']
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)."""
    return jsonify({'message': 'Logout successful'}), 200
