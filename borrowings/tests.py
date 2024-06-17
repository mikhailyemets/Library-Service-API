from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Author, Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer
)


BORROWING_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


def return_book_url(borrowing_id):
    return reverse("borrowings:borrowing-return-book", args=[borrowing_id])


def sample_author(**params):
    defaults = {
        "first_name": "Sample",
        "last_name": "Author",
    }
    defaults.update(params)
    author = Author.objects.create(**defaults)

    return author


def sample_book(author, **params):
    defaults = {
        "title": "Sample Book",
        "cover": "Hard",
        "inventory": 5,
        "daily_fee": 1,
    }
    defaults.update(params)
    book = Book.objects.create(**defaults)
    book.authors.add(author)

    return book


def sample_user(**params):
    defaults = {
        "first_name": "fname",
        "last_name": "lname",
        "email": "user@sample.com",
        "password": "password",
        "is_staff": False,
    }
    defaults.update(params)
    return get_user_model().objects.create(**defaults)


def sample_staff_user(**params):
    return sample_user(
        is_staff=True,
        email="admin@sample.com",
        **params
    )


def sample_borrowing(user, book, **params):
    defaults = {
        "expected_return_date": date.today() + timedelta(days=1),
        "book": book,
        "user": user,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class TestBorrowingModel(TestCase):
    def setUp(self):
        author = sample_author()
        self.book = sample_book(author)
        self.user = sample_user()

    def test_create_borrowing(self):
        borrowing = sample_borrowing(self.user, self.book)
        self.assertIsInstance(borrowing, Borrowing)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)

    def test_expected_return_date_constraint(self):
        return_date = date.today()
        with self.assertRaisesMessage(
            IntegrityError,
            "Expected return date should be more than borrowing date"
        ):
            sample_borrowing(self.user, self.book, expected_return_date=return_date)

    def test_actual_return_date_constraint(self):
        return_date = date.today() - timedelta(days=1)
        with self.assertRaisesMessage(
            IntegrityError,
            "Actual return date should be equal or more than borrowing date"
        ):
            sample_borrowing(self.user, self.book, actual_return_date=return_date)

    def test_cannot_delete_book_while_book_is_borrowed(self):
        sample_borrowing(self.user, self.book)
        with self.assertRaises(ProtectedError):
            self.book.delete()

    def test_cannot_delete_user_while_book_is_borrowed(self):
        sample_borrowing(self.user, self.book)
        with self.assertRaises(ProtectedError):
            self.user.delete()


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.author = sample_author()
        self.book1 = sample_book(self.author)
        self.book2 = sample_book(self.author, title="Sample Book 2")
        self.book3 = sample_book(self.author, title="Sample Book 3")

        self.client.force_authenticate(user=self.user)

    def test_list_borrowings(self):
        admin = sample_staff_user()
        sample_borrowing(user=admin, book=self.book1)
        sample_borrowing(user=self.user, book=self.book2)
        sample_borrowing(user=self.user, book=self.book3)

        response = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_borrowing(self):
        borrowing = sample_borrowing(self.user, book=self.book1)

        url = detail_url(borrowing.id)
        response = self.client.get(url)
        serializer = BorrowingRetrieveSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_borrowing(self):
        response = self.client.post(
            BORROWING_URL,
            {
                "book": self.book1.id,
                "expected_return_date": date.today() + timedelta(days=1),
            }
        )
        borrowing = Borrowing.objects.first()
        serializer = BorrowingCreateSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_cannot_create_borrowing_if_book_inventory_lt_zero(self):
        book = sample_book(
            author=self.author,
            title="Sample Book 3",
            inventory=0,
        )
        response = self.client.post(
            BORROWING_URL,
            {
                "book": book.id,
                "expected_return_date": date.today() + timedelta(days=1),
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_minimum_expected_return_date_today_raise_error(self):
        data = {
            "book": self.book1.id,
            "expected_return_date": date.today(),
        }
        serializer = BorrowingCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_filter_borrowings_by_is_active(self):
        active_borrowing = sample_borrowing(self.user, book=self.book1)
        inactive_borrowing = sample_borrowing(
            self.user,
            book=self.book2,
            actual_return_date=date.today()
        )

        active_serializer = BorrowingListSerializer(active_borrowing)
        inactive_serializer = BorrowingListSerializer(inactive_borrowing)

        response = self.client.get(BORROWING_URL, {"is_active": "true"})
        self.assertEqual([active_serializer.data], response.data)

        response = self.client.get(BORROWING_URL, {"is_active": "false"})
        self.assertEqual([inactive_serializer.data], response.data)

    def test_return_book(self):
        borrowing = sample_borrowing(self.user, self.book1)

        url = return_book_url(borrowing.id)
        response = self.client.post(url)
        borrowing = Borrowing.objects.filter(id=borrowing.id).first()
        book1 = Book.objects.filter(id=self.book1.id).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(borrowing.actual_return_date, date.today())
        self.assertEqual(book1.inventory, 6)


class AuthenticatedAdminBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.admin = sample_staff_user()
        self.author = sample_author()
        self.book1 = sample_book(self.author)
        self.book2 = sample_book(self.author, title="Sample Book 2")

        self.client.force_authenticate(user=self.admin)

    def test_list_borrowings(self):
        sample_borrowing(self.admin, book=self.book1)
        sample_borrowing(self.user, book=self.book2)

        response = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_borrowings_by_user_id(self):
        sample_borrowing(self.admin, book=self.book1)
        sample_borrowing(self.user, book=self.book2)

        user_borrowings = Borrowing.objects.filter(user=self.user)
        user_borrowings_serializer = BorrowingListSerializer(user_borrowings, many=True)

        response = self.client.get(BORROWING_URL, {"user_id": self.user.id})
        self.assertEqual(user_borrowings_serializer.data, response.data)
