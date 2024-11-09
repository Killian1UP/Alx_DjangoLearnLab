from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.
def list_book(request):
    books = Book.objects.all()
    context = {'list_book': books}
    return render(request, 'relationship_app/list_books.html', context) 

class BookDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.objects.books.all()
        return context