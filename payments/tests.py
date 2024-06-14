from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker
from payments.models import Payment
from payments.serializers import PaymentListSerializer, PaymentRetrieveSerializer


PAYMENTS = "payments-read"


def create_user(
        username="testuser",
        password="testpassword",
        email="testuser@localhost",
        **kwargs
):
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        **kwargs
    )


def create_payment(
    borrowing=None,
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
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(user=self.user)
        self.fake = Faker().unique

        user = create_user()
        for _ in range(5):
            create_payment(
                borrowing=user,
                session_url=self.fake.url(),
                session_id=self.fake.uuid4()
            )

    def test_self_retrieve(self):
        payment = create_payment(
            borrowing=self.user,
            session_url=self.fake.url(),
            session_id=self.fake.uuid4()
        )
        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        serializer = PaymentRetrieveSerializer(payment)
        self.assertEqual(response.json(), serializer.data)

    def test_other_user_retrieve(self):
        user = create_user(
            username=self.fake.user_name(),
            email=self.fake.email()
        )
        payment = create_payment(
            borrowing=user,
            session_url=self.fake.url(),
            session_id=self.fake.uuid4()
        )

        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        payment = create_payment(
            borrowing=self.user,
            session_url=self.fake.url(),
            session_id=self.fake.uuid4()
        )

        url = reverse(f"payments:{PAYMENTS}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        serializer = PaymentListSerializer([payment])
        self.assertEqual(response.json(), serializer.data)


class TestPaymentsAdmin(APITestCase):
    def setUp(self):
        self.user = create_user(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.fake = Faker().unique
        user = create_user(
            username=self.fake.user_name(),
            email=self.fake.email()
        )

        for _ in range(5):
            self.payment = create_payment(
                borrowing=user,
                session_url=self.fake.url(),
                session_id=self.fake.uuid4()
            )

    def test_list(self):
        url = reverse(f"payments:{PAYMENTS}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_retrieve(self):
        url = reverse(f"payments:{PAYMENTS}-detail", kwargs={"pk": self.payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
