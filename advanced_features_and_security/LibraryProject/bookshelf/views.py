from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import permission_required

# Create your views here.
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