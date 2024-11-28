from rest_framework import serializers
from .models import Author, Book
from datetime import date

# Created serializers for the models
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# Custom validation to ensure the publication_year is not in the future.
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# A nested BookSerializer to serialize the related books dynamically.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

# The AuthorSerializer includes a books field that is a nested BookSerializer. 
# This allows the API to return the Author data along with its related books.all
