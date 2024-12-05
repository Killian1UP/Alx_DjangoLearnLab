from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserProfileForm, PostForm
from .models import UserProfile, Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

    def form_valid(self, form):
        user = form.save()
        user_profile = UserProfile(user=user)
        user_profile.save()
        return super().form_valid(form)

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
    