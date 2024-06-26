from datetime import date

from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from books.serializers import BookSerializer
from borrowings.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title", read_only=True)


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta(BorrowingSerializer.Meta):
        read_only_fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book", "expected_return_date")

    def validate(self, attrs):
        book = attrs["book"]
        expected_return_date = attrs["expected_return_date"]
        if book.inventory < 1:
            raise ValidationError({"book_inventory": "Book inventory is less than 1"})
        if expected_return_date <= date.today():
            raise ValidationError(
                {"expected_return_date": "Expected return date should be more than today"}
            )

        return attrs

    def create(self, validated_data):
        book = validated_data.pop("book")
        expected_return_date = validated_data.pop("expected_return_date")
        user = self.context.get("request").user
        if (
            Borrowing.objects
                .filter(user=user)
                .filter(actual_return_date__isnull=True)
                .filter(expected_return_date__lt=date.today())
                .exists()
        ):
            raise ValidationError(
                {"borrowing": ("It is forbidden to create borrowing, "
                               "user has expired borrowings")}
            )

        with transaction.atomic():
            borrowing = Borrowing.objects.create(
                user=user,
                book=book,
                expected_return_date=expected_return_date
            )
            book.inventory -= 1
            book.save()

        return borrowing
