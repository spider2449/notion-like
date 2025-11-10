from functools import wraps
from flask import request, jsonify, g
from backend.services.auth_service import AuthService
from backend.repositories.user_repository import UserRepository

def require_auth(f):
    """Middleware decorator to require JWT authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Extract token (format: "Bearer <token>")
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        token = parts[1]
        
        try:
            # Verify token
            payload = AuthService.verify_token(token)
            
            # Get user from database
            user = UserRepository.find_by_id(payload['user_id'])
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            # Attach user to request context
            g.user = user
            g.user_id = user.id
            
            return f(*args, **kwargs)
            
        except ValueError as e:
            error_message = str(e)
            if 'expired' in error_message.lower():
                return jsonify({'error': 'Token expired'}), 401
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function
