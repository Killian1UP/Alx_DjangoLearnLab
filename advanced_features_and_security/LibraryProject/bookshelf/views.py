from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Book
from django.contrib.auth.decorators import permission_required
from .forms import SearchForm, ExampleForm

# Create your views here.
def book_list(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'book_list.html', {'books': books})

def create_book(request):
    if request.method == 'POST':
        # Create a new book
        Book.objects.create(name=request.POST['name'], description=request.POST['description'])
        return redirect('list')  

@permission_required('bookshelf.can_create', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Post.objects.create(name=name, description=description)
        return redirect('create')
    return render(request, 'bookshelf/create_post.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.name = request.POST.get('name')
        post.description = request.POST.get('description')
        post.save()
        return redirect('edit', post_id=post.id)  
    return render(request, 'bookshelf/edit_post.html', {'post': post})

@permission_required('app_name.can_delete', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('delete')  
    return render(request, 'bookshelf/delete_post.html', {'post': post})

def search_books(request):
    form = SearchForm(request.GET)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.objects.filter(name__icontains=query)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'results': results})

def example_view(request):
    form = ExampleForm(request.POST or None)
    if form.is_valid():
        # Process the form data
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        # Do something with the data...
    return render(request, 'bookshelf/example_form.html', {'form': form})