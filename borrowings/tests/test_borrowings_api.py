from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from books.models import Book
from borrowings.models import Borrowing


BORROWING_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


def sample_book(**params):
    defaults = {
        "title": "Sample Book",
        "author": "sample author",
        "cover": "Hard",
        "inventory": 5,
        "daily_fee": 1,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_user(**params):
    defaults = {
        "first_name": "fname",
        "last_name": "lname",
        "email": "sample@user.com",
        "password": "password",
        "is_staff": False,
    }
    defaults.update(params)
    return get_user_model().objects.create(**defaults)


def sample_staff_user(**params):
    return sample_user(is_staff=True, **params)


def sample_borrowing(user, book, **params):
    defaults = {
        "expected_return_date": date.today() + timedelta(days=1),
        "actual_return_date": date.today() + timedelta(days=2),
        "book": book,
        "user": user,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class TestBorrowingModel(TestCase):
    def setUp(self):
        self.book = sample_book()
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


class TestBorrowingSerializers(TestCase):
    pass


class TestBorrowingViews(TestCase):
    pass
