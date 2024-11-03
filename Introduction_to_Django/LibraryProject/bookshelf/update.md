```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title='1984')

# Update the title
book.title = 'Nineteen Eighty-Four'
book.save()

# Display the updated title
Book.objects.all().values()
<QuerySet [{'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}]>