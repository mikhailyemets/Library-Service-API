from datetime import date, timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from books.models import Book
from borrowings.models import Borrowing
from borrowings.tests import BORROWING_URL
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


class MockedDate(date):
    @classmethod
    def today(cls) -> date:
        return cls(2024, 4, 9)


class TestPaymentUnauthorized(APITestCase):
    def test_retrieve(self):
        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        url = reverse(f"payments:{PAYMENTS}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


class TestBorrowingCreatePayment(APITestCase):

    def setUp(self):
        self.user = create_user(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_create_payment_from_borrowing(self):
        self.assertEqual(Payment.objects.count(), 0)
        data = {
            "book": create_book().id,
            "expected_return_date": date.today() + timedelta(days=1)
        }
        self.client.post(BORROWING_URL, data)
        self.assertEqual(Payment.objects.count(), 1)


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
            create_payment(
                borrowing=borrowing,
                session_url=cls.fake.url(),
                session_id=cls.fake.uuid4()
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
        payment = create_payment(
            borrowing=borrowing,
            session_url=self.fake.url(),
            session_id=self.fake.uuid4()
        )
        return payment

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
        payment = create_payment(
            borrowing=borrowing,
            session_url=self.fake.url(),
            session_id=self.fake.uuid4()
        )

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
            borrowing = create_borrowing(
                user=user,
                book=create_book(cls.fake.word()),
                expected_return_date=date.today() + timedelta(days=1)
            )
            cls.payment = create_payment(
                borrowing=borrowing,
                session_url=cls.fake.url(),
                session_id=cls.fake.uuid4()
            )

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


class TestSuccessPayment(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_self_retrieve_with_refresh_payment(self):
        data = {
            "book": create_book().id,
            "expected_return_date": date.today() + timedelta(days=1)
        }
        self.client.post(BORROWING_URL, data)
        old_payments = Payment.objects.first()
        with mock.patch("datetime.date", new=MockedDate):
            self.client.get(
                reverse(
                    f"payments:{PAYMENTS}-detail", kwargs={"pk": old_payments.id}
                )
            )

        self.assertNotEqual(
            Payment.objects.get(pk=old_payments.id).session_url,
            old_payments.session_url
        )

    def test_unpaid_success_payment(self):
        data = {
            "book": create_book().id,
            "expected_return_date": date.today() + timedelta(days=1)
        }
        self.client.post(BORROWING_URL, data).json()
        url = reverse(
            f"payments:success_{PAYMENTS}", kwargs={"pk": Payment.objects.first().id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_paid_success_payment(self):
        pass
