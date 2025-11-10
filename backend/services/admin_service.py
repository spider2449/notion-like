from backend.repositories.user_repository import UserRepository
from backend.services.auth_service import AuthService
from backend.utils.security import sanitize_input, validate_email, validate_username

class AdminService:
    """Service for admin operations."""
    
    @staticmethod
    def get_all_users():
        """Get all users (admin only)."""
        return UserRepository.find_all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID (admin only)."""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        return user
    
    @staticmethod
    def create_user(username, email, password, is_admin=False):
        """Create a new user (admin only)."""
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
        user = UserRepository.create(username, email, password_hash, is_admin)
        
        return user
    
    @staticmethod
    def update_user_admin_status(user_id, is_admin):
        """Update user's admin status."""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        UserRepository.update_admin_status(user_id, is_admin)
        return UserRepository.find_by_id(user_id)
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user account (admin only)."""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        UserRepository.delete(user_id)
        return True
    
    @staticmethod
    def get_user_statistics():
        """Get user statistics."""
        users = UserRepository.find_all()
        return {
            'total_users': len(users),
            'admin_users': len([u for u in users if u.is_admin]),
            'regular_users': len([u for u in users if not u.is_admin])
        }
