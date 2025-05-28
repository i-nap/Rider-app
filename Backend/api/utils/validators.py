import re
from typing import List

def validate_password_strength(password: str) -> List[str]:
    """
    Validate password strength and return list of errors
    
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit.")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character.")
    
    # Check for common weak passwords
    common_passwords = [
        'password', '12345678', 'qwerty', 'abc123', 'password123',
        '123456789', 'welcome', 'admin', 'letmein', 'monkey'
    ]
    
    if password.lower() in common_passwords:
        errors.append("Password is too common. Please choose a stronger password.")
    
    return errors

def validate_email_format(email: str) -> bool:
    """
    Validate email format using regex
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format (basic validation)
    """
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's between 10-15 digits (international format)
    return 10 <= len(digits_only) <= 15

# utils/security.py
import hashlib
import secrets
from django.conf import settings

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(length)

def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data using SHA-256"""
    return hashlib.sha256(data.encode()).hexdigest()

def generate_password_reset_token() -> str:
    """Generate a secure token for password reset"""
    return generate_secure_token(32)

# middleware/security_middleware.py
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware:
    """
    Add security headers to all responses
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

class RequestLoggingMiddleware:
    """
    Log all authentication-related requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log auth-related requests
        if any(path in request.path for path in ['/auth/', '/login', '/signup', '/verify']):
            logger.info(f"Auth request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
        
        response = self.get_response(request)
        return response

# Custom exception classes
class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass

class RateLimitExceeded(Exception):
    """Custom exception for rate limiting"""
    pass

class EmailVerificationError(Exception):
    """Custom exception for email verification errors"""
    pass