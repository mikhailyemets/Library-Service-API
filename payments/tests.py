from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment
from payments.serializers import PaymentListSerializer, PaymentRetrieveSerializer

PAYMENTS = "payments"


def create_user(
        password="testpassword",
        email="testuser@localhost",
        **kwargs
):
    return get_user_model().objects.create_user(
        password=password,
        email=email,
        **kwargs
    )


def create_payment(
    borrowing: Borrowing,
    status=Payment.Status.PENDING,
    payment_type=Payment.Type.PAYMENT,
    session_url="test_session_url",
    session_id="test_session_id",
    money_to_pay=100.00
):
    return Payment.objects.create(
        borrowing=borrowing,
        status=status,
        type=payment_type,
        session_url=session_url,
        session_id=session_id,
        money_to_pay=money_to_pay
    )


def create_borrowing(
        book,
        user,
        expected_return_date=date.today() + timedelta(days=1)
):
    return Borrowing.objects.create(
        book=book,
        user=user,
        expected_return_date=expected_return_date
    )


def create_book(
        title="Test Book",
):
    return Book.objects.create(
        title=title,
        cover=Book.COVER_CHOICES[0][0],
        inventory=10,
        daily_fee=10
    )


class TestPaymentUnauthorized(APITestCase):
    def test_retrieve(self):
        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        url = reverse(f"payments:{PAYMENTS}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


class TestPaymentsUser(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.fake = Faker().unique
        user = create_user(cls.fake.user_name(), cls.fake.email())
        for _ in range(5):
            borrowing = create_borrowing(
                user=user,
                book=create_book(cls.fake.word()),
                expected_return_date=date.today() + timedelta(days=1)
            )

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def create_payment(self, user):
        borrowing = create_borrowing(
            user=user,
            book=create_book(self.fake.word()),
            expected_return_date=date.today() + timedelta(days=1)
        )
        return Payment.objects.get(borrowing=borrowing)

    def test_self_retrieve(self):
        payment = self.create_payment(self.user)
        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        serializer = PaymentRetrieveSerializer(payment)
        self.assertEqual(response.json(), serializer.data)

    def test_other_user_retrieve(self):
        user = create_user(email=self.fake.email())
        payment = self.create_payment(user)

        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        borrowing = create_borrowing(
            user=self.user,
            book=create_book(self.fake.word()),
            expected_return_date=date.today() + timedelta(days=1)
        )
        payment = Payment.objects.get(borrowing=borrowing)

        url = reverse(f"payments:{PAYMENTS}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        serializer = PaymentListSerializer([payment], many=True)
        self.assertEqual(response.json(), serializer.data)


class TestPaymentsAdmin(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker().unique
        user = create_user(email=cls.fake.email())

        for _ in range(5):
            cls.borrowing = create_borrowing(
                user=user,
                book=create_book(cls.fake.word()),
                expected_return_date=date.today() + timedelta(days=1)
            )
        cls.payment = Payment.objects.get(borrowing=cls.borrowing)

    def setUp(self):
        self.user = create_user(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        url = reverse(f"payments:{PAYMENTS}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_retrieve(self):
        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": self.payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
