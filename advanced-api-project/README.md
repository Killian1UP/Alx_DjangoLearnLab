ListView:
is configured to list all the books in our API and you can access them by using this url http://127.0.0.1:8000/api/books/. For permissions i used IsAuthenticatedOrReadOnly to not allow users who are not authenticated to alter the list.

DetailView:
is configured to only retrieve a single book in our API and you can access the book by using this url http://127.0.0.1:8000/api/books/id/. For permissions i used IsAuthenticatedOrReadOnly to not allow users who are not authenticated to alter the book.

CreateView:
is configured to add a new book in our API and you can do so by using this url http://127.0.0.1:8000/api/books/create/. For permissions i used IsAuthenticated to allow authenticated users to add new books. I customized the settings in CreateView to notify you if you create a book that has been created.

UpdateView:
is configured to modify an existing book in our API and you can do so by using this url http://127.0.0.1:8000/api/books/id/update/. For permissions i used IsAuthenticated to allow authenticated users to modify an existing book. I customized the settings in UpdateView to allow only admin users the privilege to update only.

DeleteView:
is configured to remove a book in our API and you can do so by using this url http://127.0.0.1:8000/api/books/id/delete/. For permissions i used IsAuthenticated to allow authenticated users to remove a book.

