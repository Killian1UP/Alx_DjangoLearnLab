from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import RegisterView
from . import views
from views import PostByTagListView

urlpatterns = [
    # Login & Logout urls
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Profile & Register urls
    path('profile/', views.profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    # Post CRUD Operations Views
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    # Comment CRUD operations views
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment_list'),
    path('posts/<int:post_id>/comments/<int:pk>', views.CommentDetailView.as_view(), name='comment_detail'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('posts/<int:post_id>/comment/<int:pk>/delete/', views.CommentDetailView.as_view(), name='comment_delete'),
    # Search view
    path('search/', views.search_posts, name='search_posts'),
    # Filtered tag view 
    path('tag/<int:tag_id>/', views.TagFilterView.as_view(), name='tag_filter'),
    # posts by tags
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
]