from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserProfileForm, PostForm, CommentForm
from .models import UserProfile, Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

    # def form_valid(self, form):
    #     user = form.save()
    #     user_profile = UserProfile(user=user)
    #     user_profile.save()
    #     return super().form_valid(form)

@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid() and user_profile_form.is_valid():
            profile_form.save()
            user_profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)

    context = {
        'profile_form': profile_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'blog/profile.html', context)

# To list all the posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# To show individual posts
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# To allow authenticated users to create new posts.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        # Automatically set the author as the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

# To enable post authors to edit their posts.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'
    success_url = reverse_lazy('post_list')

# Ensure only the author can edit the post
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        # Automatically set the author as the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

# To let authors delete their posts.
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')

# Ensure only the author can delete the post
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comment_list.html'
    context_object_name = 'comments'

    # Custom query to filter comments for a specific post
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id']).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the specific post and add it to the context
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        return context

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'blog/comment_detail.html'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_create.html'

    def form_valid(self, form):
        # Automatically set the author as the logged-in user
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])  # Automatically set the post
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('comment_list', kwargs={'post_id': self.kwargs['post_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the post object to the context
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_update.html'

    # Ensure only the author can edit the comment
    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user 
    
    def get_success_url(self):
        return reverse_lazy('comment_list', kwargs={'post_id': self.object.post.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the post object to the context
        context['post'] = self.object.post
        context['comment'] = self.object
        return context
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

# Ensure only the author can delete the somment
    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user
    
    def get_success_url(self):
        # Redirect to the comment list of the related post
        return reverse_lazy('comment_list', kwargs={'post_id': self.object.post.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the post object to the context
        context['post'] = self.object.post # Add the related post
        context['comment'] = self.object # Add the comment being deleted
        return context
