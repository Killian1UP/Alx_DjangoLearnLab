from django.urls import path
from .views import list_books, LibraryDetailView, RegisterView

urlpatterns = [
    path('list/', list_books, name='list'),
    path('library/', LibraryDetailView.as_view(), name='library'),
]

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]

from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]

from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    ...,

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", RegisterView.as_view(), name="templates/registration/register"),
        ...
]