from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book, Author
from books.permissions import IsAdminOrReadOnly


BOOKS_URL = reverse("books:book-list")


class BookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="qwerty",
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="adminuser@example.com", password="qwerty1234",
        )
        self.author1 = Author.objects.create(
            first_name="Taras",
            last_name="Shevchenko"
        )
        self.author2 = Author.objects.create(
            first_name="Ivan",
            last_name="Franko"
        )
        self.author3 = Author.objects.create(
            first_name="Ostap",
            last_name="Vyshnya"
        )

        self.book1 = Book.objects.create(
            title="Kobzar",
            cover="Hard",
            inventory=10,
            daily_fee=9.99,
        )
        self.book1.authors.add(self.author1)

        self.book2 = Book.objects.create(
            title="Zakhar Berkut",
            cover="Soft",
            inventory=5,
            daily_fee=14.99,
        )
        self.book2.authors.add(self.author2)

        self.book3 = Book.objects.create(
            title="Zenitka",
            cover="Soft",
            inventory=2,
            daily_fee=7.99,
        )
        self.book3.authors.add(self.author3)

    def authenticate_user(self, is_admin=False):
        if is_admin:
            self.client.force_authenticate(user=self.admin_user)
        else:
            self.client.force_authenticate(user=self.user)

    def test_get_books(self):
        self.authenticate_user()
        response = self.client.get(BOOKS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_book(self):
        self.authenticate_user()
        url = reverse("books:book-detail", args=[self.book3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book3.title)

    def test_create_book_as_admin(self):
        self.authenticate_user(is_admin=True)
        payload = {
            "title": "Testament",
            "authors": [self.author1.id],
            "cover": "Soft",
            "inventory": 15,
            "daily_fee": 12.99,
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title=payload["title"]).exists())

    def test_create_book_as_non_admin(self):
        self.authenticate_user()
        payload = {
            "title": "Testament",
            "authors": [self.author1.id],
            "cover": "Soft",
            "inventory": 15,
            "daily_fee": 12.99,
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_admin(self):
        self.authenticate_user(is_admin=True)
        url = reverse("books:book-detail", args=[self.book1.id])
        payload = {
            "title": "Fatherland",
            "authors": [self.author2.id],
            "cover": "Hard",
            "inventory": 8,
            "daily_fee": 11.99,
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, payload["title"])
        self.assertEqual(self.book1.inventory, payload["inventory"])
        self.assertEqual(
            list(self.book1.authors.values_list('id', flat=True)),
            payload["authors"]
        )

    def test_update_book_as_non_admin(self):
        self.authenticate_user()
        url = reverse("books:book-detail", args=[self.book1.id])
        payload = {
            "title": "Fatherland",
            "authors": [self.author2.id],
            "cover": "Hard",
            "inventory": 8,
            "daily_fee": 11.99,
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_book(self):
        self.authenticate_user(is_admin=True)
        url = reverse("books:book-detail", args=[self.book2.id])
        payload = {"title": "My love"}
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, payload["title"])

    def test_delete_book_as_admin(self):
        self.authenticate_user(is_admin=True)
        url = reverse("books:book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_as_non_admin(self):
        self.authenticate_user()
        url = reverse("books:book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_invalid_create_book(self):
        self.authenticate_user(is_admin=True)
        payload = {
            "title": "Invalid Book",
            "authors": [self.author1.id],
            "cover": "Invalid Cover",
            "inventory": -5,
            "daily_fee": "Invalid Fee",
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_book(self):
        self.authenticate_user(is_admin=True)
        url = reverse("books:book-detail", args=[self.book1.id])
        payload = {
            "inventory": "Invalid Inventory",
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
