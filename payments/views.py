from payments.service import create_stripe_session
import datetime
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from payments.models import Payment
from payments.serializers import (
    PaymentListSerializer,
    PaymentRetrieveSerializer
)


class PaymentView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            self.queryset = self.queryset.filter(borrowing__user=user)
        self.queryset = self.queryset.select_related("borrowing__user")
        self.queryset = self.queryset.select_related("borrowing__book")
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentListSerializer
        if self.action == 'retrieve':
            return PaymentRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.date_added != datetime.date.today():
            stripe_session = create_stripe_session(request, instance.borrowing)
            instance.session_url = stripe_session.url
            instance.session_id = stripe_session.id
            instance.money_to_pay = stripe_session.amount_total / 100
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SuccessPaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Borrowing.objects.select_related("payment")

    def get(self, request, pk):
        borrowing = get_object_or_404(self.queryset, user=request.user, id=pk)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_status = (
            stripe.checkout.Session
            .retrieve(borrowing.payment.session_id)["payment_status"]
        )
        if payment_status == "paid":
            payment = borrowing.payment
            payment.status = Payment.Status.PAID
            payment.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CancelPaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        return Response(
            {
                "detail": "Payment can be made later. "
                "The session is available for only 24 hours."
            },
            status=status.HTTP_200_OK,
        )
