from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_book, name='list'),
    path('library/', views.BookDetailView.as_view, name='library'),
]