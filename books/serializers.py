from decimal import Decimal

from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator
from rest_framework import serializers
from books.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$",
                message="Only English letters are allowed in the name.",
                code="invalid_name",
            )
        ],
        help_text="Only English characters allowed.",
    )
    last_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$",
                message="Only English letters are allowed in the surname.",
                code="invalid_surname",
            )
        ],
        help_text="Only English characters allowed.",
    )

    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "full_name")


class BookSerializer(serializers.ModelSerializer):
    daily_fee = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("1000.00")),
        ],
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "authors",
            "cover",
            "inventory",
            "daily_fee",
        )


class BookListSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )

    class Meta:
        model = Book
        fields = ("id", "title", "authors", "inventory", "daily_fee")


class BookRetrieveSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("title", "authors", "cover", "inventory", "daily_fee")
