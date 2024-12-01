from rest_framework.test import APITestCase
from .models import Book
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

class BookAPITests(APITestCase):
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')
        self.url = reverse('book-list')  # Assuming the URL pattern for listing books

    def test_create_book_with_login(self):
        # Log in the user using self.client.login()
        self.client.login(username='testuser', password='password')
        
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2024
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')
        self.assertEqual(Book.objects.get().author, 'Test Author')
        self.assertEqual(Book.objects.get().publication_year, 2024)

    def test_update_book(self):
        # Create a book first
        book = Book.objects.create(
            title='Old Title',
            author='Old Author',
            publication_year=2020
        )
        url = reverse('book-detail', args=[book.id])
        updated_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'publication_year': 2025
        }

        response = self.client.put(url, updated_data, format='json')

        book.refresh_from_db()  # Refresh the book object to get updated values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, 'Updated Title')
        self.assertEqual(book.author, 'Updated Author')
        self.assertEqual(book.publication_year, 2025)

    def test_delete_book(self):
        # Create a book first
        book = Book.objects.create(
            title='Book to delete',
            author='Author',
            publication_year=2021
        )
        url = reverse('book-detail', args=[book.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Book should be deleted

    def test_search_books(self):
        # Create some books
        Book.objects.create(title='Book A', author='Author A', publication_year=2022)
        Book.objects.create(title='Book B', author='Author B', publication_year=2023)
        Book.objects.create(title='Another Book A', author='Author A', publication_year=2021)

        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Book A'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books with "Book A" in the title
        self.assertTrue('Book A' in [book['title'] for book in response.data])

    def test_filter_books_by_year(self):
        Book.objects.create(title='Book A', author='Author A', publication_year=2022)
        Book.objects.create(title='Book B', author='Author B', publication_year=2023)
        Book.objects.create(title='Book C', author='Author C', publication_year=2022)

        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2022}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books published in 2022
        self.assertTrue(all(book['publication_year'] == 2022 for book in response.data))

    def test_order_books_by_year(self):
        Book.objects.create(title='Book C', author='Author C', publication_year=2024)
        Book.objects.create(title='Book A', author='Author A', publication_year=2022)
        Book.objects.create(title='Book B', author='Author B', publication_year=2023)

        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book A')  # The oldest book first (2022)
        self.assertEqual(response.data[1]['title'], 'Book B')
        self.assertEqual(response.data[2]['title'], 'Book C')  # The newest book last

    def test_create_book_without_authentication(self):
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2024
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Assuming 403 Forbidden for unauthenticated users

    def test_create_book_with_authentication(self):
        self.client.force_authenticate(user=self.user)  # Assuming you have a user object
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2024
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)