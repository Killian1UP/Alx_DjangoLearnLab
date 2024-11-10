from django.shortcuts import render
from .models import Book

# Create your views here.
def list_book(request):
    books = Book.objects.all()
    context = {'list_book': books}
    return render(request, 'relationship_app/list_books.html', context) 

from .models import Library
from django.views.generic.detail import DetailView

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.objects.books.all()
        return context