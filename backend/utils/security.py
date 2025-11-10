import html
import re

def sanitize_input(text):
    """Sanitize user input to prevent XSS attacks."""
    if not text:
        return text
    
    # Remove any HTML tags
    text = html.escape(text)
    
    return text

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username format."""
    if not username or len(username) < 3 or len(username) > 50:
        return False
    
    # Allow alphanumeric and underscores
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None
