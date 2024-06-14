from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import freeze_time
from django.urls import reverse

from books.models import Book
from borrowings.models import Borrowing


BORROWING_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowings-detail", args=[borrowing_id])


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


@freeze_time("2024-01-20")
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
    pass


class TestBorrowingSerializers(TestCase):
    pass


class TestBorrowingViews(TestCase):
    pass
