from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view

from books.models import Book, Author
from books.serializers import (
    BookSerializer,
    AuthorSerializer,
    AuthorListSerializer,
    AuthorRetrieveSerializer,
    BookListSerializer,
    BookRetrieveSerializer
)
from books.permissions import IsAdminOrReadOnly
from books.schemas import author_schema, book_schema


@extend_schema_view(**author_schema)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer

        if self.action == "retrieve":
            return AuthorRetrieveSerializer

        return super().get_serializer_class()


@extend_schema_view(**book_schema)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookRetrieveSerializer

        return super().get_serializer_class()
