from django.contrib import admin
from .models import Author, Book
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_year')
    search_fields = ('title', 'author__name')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)