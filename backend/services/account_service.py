from backend.repositories.user_repository import UserRepository
from backend.services.auth_service import AuthService
from backend.utils.security import sanitize_input, validate_email, validate_username

class AccountService:
    """Service for account management operations."""
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile information."""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        return user.to_dict()
    
    @staticmethod
    def update_username(user_id, new_username):
        """Update user's username."""
        new_username = sanitize_input(new_username)
        
        if not validate_username(new_username):
            raise ValueError('Username must be 3-50 characters and contain only letters, numbers, and underscores')
        
        # Check if username is already taken
        existing_user = UserRepository.find_by_username(new_username)
        if existing_user and existing_user.id != user_id:
            raise ValueError('Username already taken')
        
        UserRepository.update_username(user_id, new_username)
        return UserRepository.find_by_id(user_id)
    
    @staticmethod
    def update_email(user_id, new_email):
        """Update user's email."""
        new_email = sanitize_input(new_email)
        
        if not validate_email(new_email):
            raise ValueError('Invalid email address')
        
        # Check if email is already registered
        existing_user = UserRepository.find_by_email(new_email)
        if existing_user and existing_user.id != user_id:
            raise ValueError('Email already registered')
        
        UserRepository.update_email(user_id, new_email)
        return UserRepository.find_by_id(user_id)
    
    @staticmethod
    def update_password(user_id, current_password, new_password):
        """Update user's password."""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        # Verify current password
        if not AuthService.verify_password(current_password, user.password_hash):
            raise ValueError('Current password is incorrect')
        
        # Validate new password
        if not new_password or len(new_password) < 6:
            raise ValueError('New password must be at least 6 characters')
        
        # Hash and update password
        new_password_hash = AuthService.hash_password(new_password)
        UserRepository.update_password(user_id, new_password_hash)
        
        return UserRepository.find_by_id(user_id)
    
    @staticmethod
    def delete_account(user_id, password):
        """Delete user account after password verification."""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        # Verify password before deletion
        if not AuthService.verify_password(password, user.password_hash):
            raise ValueError('Password is incorrect')
        
        UserRepository.delete(user_id)
        return True
