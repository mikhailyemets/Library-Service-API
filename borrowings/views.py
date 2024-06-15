from datetime import date

from django.db import transaction
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer
)
from borrowings.permissions import IsAdminOrOwner


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    queryset = Borrowing.objects.select_related("book", "user")
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
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

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
