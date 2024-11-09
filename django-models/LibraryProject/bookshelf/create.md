```python
from bookshelf.models import Book

# Create a new book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)

# Confirm successful creation
Book.objects.all().values()
<QuerySet [{'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}]>