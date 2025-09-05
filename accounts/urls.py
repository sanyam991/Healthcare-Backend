from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    logout_view,
    refresh_token_view
)

app_name = 'accounts'

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('refresh/', refresh_token_view, name='refresh'),
    
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='profile'),
]
