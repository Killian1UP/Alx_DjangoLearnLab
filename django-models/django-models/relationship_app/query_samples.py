from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Access books using the related_name defined in ForeignKey
        return books
    except Author.DoesNotExist:
        return f"No author found with the name {author_name}"

# List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Access books using the related_name defined in ManyToManyField
        return books
    except Library.DoesNotExist:
        return f"No library found with the name {library_name}"

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Access librarian using the related_name in OneToOneField
        return librarian
    except Library.DoesNotExist:
        return f"No library found with the name {library_name}"
    except Librarian.DoesNotExist:
        return f"No librarian found for the library {library_name}"