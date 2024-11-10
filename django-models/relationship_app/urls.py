from django.urls import path
from .views import list_book, LibraryDetailView

urlpatterns = [
    path('list/', list_book, name='list'),
    path('library/', LibraryDetailView.as_view, name='library'),
]