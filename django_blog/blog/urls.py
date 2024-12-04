from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import RegisterView
from . import views

urlpatterns = [
    # Login & Logout urls
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Profile & Register urls
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
]