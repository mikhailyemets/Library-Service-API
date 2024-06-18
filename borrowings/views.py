from datetime import date

from django.db import transaction
from django.db.models import Q
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.permissions import IsAdminOrOwner
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer
)
from payments.models import Payment
from payments.service import create_stripe_session


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = (
        Borrowing.objects
        .annotate(is_active=Q(actual_return_date__isnull=True))
        .select_related("book", "user")
    )
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action in ("retrieve", "return_book"):
            return BorrowingRetrieveSerializer
        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(is_active=True)
            if is_active.lower() == "false":
                queryset = queryset.filter(is_active=False)

        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        stripe_session = create_stripe_session(self.request, serializer.instance)
        print(stripe_session.url)
        print(stripe_session.id)
        Payment.objects.create(
            borrowing=serializer.instance,
            session_url=stripe_session.url,
            session_id=stripe_session.id,
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
            money_to_pay=stripe_session.amount_total / 100
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="return"
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            raise ValidationError(
                {"actual_return_date": "Date already set, book returned"}
            )

        book = borrowing.book
        serializer = self.get_serializer(borrowing)

        with transaction.atomic():
            book.inventory += 1
            borrowing.actual_return_date = date.today()
            book.save()
            borrowing.save()

        return Response(serializer.data)
