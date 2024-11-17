from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('edit/', views.edit_post, name='edit_post'),
    path('delete/', views.delete_post, name='delete_post'),
]