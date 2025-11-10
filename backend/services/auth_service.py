import bcrypt
import jwt
from datetime import datetime, timedelta
from backend.repositories.user_repository import UserRepository
from backend.utils.security import sanitize_input, validate_email, validate_username

SECRET_KEY = 'dev-secret-key-change-in-production'
TOKEN_EXPIRATION_HOURS = 24

class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt with cost factor 12."""
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify password against hash."""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            password_hash.encode('utf-8')
        )
    
    @staticmethod
    def generate_token(user_id, email):
        """Generate JWT token for user."""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError('Token expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')
    
    @staticmethod
    def register_user(username, email, password):
        """Register a new user with validation."""
        # Sanitize inputs
        username = sanitize_input(username)
        email = sanitize_input(email)
        
        # Validation
        if not validate_username(username):
            raise ValueError('Username must be 3-50 characters and contain only letters, numbers, and underscores')
        if not validate_email(email):
            raise ValueError('Invalid email address')
        if not password or len(password) < 6:
            raise ValueError('Password must be at least 6 characters')
        
        # Check if user already exists
        existing_user = UserRepository.find_by_email(email)
        if existing_user:
            raise ValueError('Email already registered')
        
        existing_username = UserRepository.find_by_username(username)
        if existing_username:
            raise ValueError('Username already taken')
        
        # Hash password and create user
        password_hash = AuthService.hash_password(password)
        user = UserRepository.create(username, email, password_hash)
        
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user and return JWT token."""
        # Find user by username
        user = UserRepository.find_by_username(username)
        if not user:
            raise ValueError('Invalid credentials')
        
        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            raise ValueError('Invalid credentials')
        
        # Generate token
        token = AuthService.generate_token(user.id, user.email)
        
        return {
            'token': token,
            'user': user.to_dict()
        }
