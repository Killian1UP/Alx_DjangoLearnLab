from django.contrib import admin
from .models import Book, CustomUser, Post
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('date_of_birth', 'profile_photo')

admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)