from functools import wraps
from flask import jsonify, g
from backend.middleware.auth_middleware import require_auth

def require_admin(f):
    """Middleware decorator to require admin privileges."""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        # Check if user is admin
        if not g.user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
