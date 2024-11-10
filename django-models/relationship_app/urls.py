from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('list/', list_books, name='list'),
    path('library/', LibraryDetailView.as_view, name='library'),
]