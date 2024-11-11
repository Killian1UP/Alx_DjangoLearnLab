from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView
from . import views

urlpatterns = [
    # App-specific views
    path('list/', list_books, name='list'),
    path('library/', LibraryDetailView.as_view(), name='library'),

    # Authentication views
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # Registration and profile views
    path('register/', views.register, name='register'),
    path('accounts/profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),

    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Include Django's default authentication URLs for password management, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]