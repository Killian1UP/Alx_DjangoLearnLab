from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RegisterView, ProfileView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Registration view
    path('register/', RegisterView.as_view(), name='register'),
    # User management view
    path('profile/', ProfileView.as_view(), name='profile'),
    # Login & Logout views
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout',)
]