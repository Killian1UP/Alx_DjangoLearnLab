from django.urls import path
from .views import RegisterView, ProfileView
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # User Registration view
    path('register/', RegisterView.as_view(), name='register'),
    # User profile management (requires authentication)
    path('profile/', ProfileView.as_view(), name='profile'),
    # User login (returns token upon success)
    path('login/', obtain_auth_token, name='login'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)