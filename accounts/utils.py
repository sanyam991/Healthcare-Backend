from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a given user.
    
    Args:
        user: User instance
        
    Returns:
        dict: Dictionary containing refresh and access tokens
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def create_user_account(email, name, username, password):
    """
    Create a new user account with the provided details.
    
    Args:
        email (str): User's email address
        name (str): User's full name
        username (str): User's username
        password (str): User's password
        
    Returns:
        User: Created user instance
    """
    user = User.objects.create_user(
        email=email.lower(),
        username=username.lower(),
        name=name,
        password=password
    )
    return user


def validate_user_data(email, username):
    """
    Validate user registration data.
    
    Args:
        email (str): Email to validate
        username (str): Username to validate
        
    Returns:
        dict: Dictionary containing validation errors if any
    """
    errors = {}
    
    if User.objects.filter(email=email.lower()).exists():
        errors['email'] = 'A user with this email already exists.'
    
    if User.objects.filter(username=username.lower()).exists():
        errors['username'] = 'A user with this username already exists.'
    
    return errors
