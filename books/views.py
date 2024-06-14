from rest_framework import viewsets

from books.models import Book, Author
from books.serializers import (
    BookSerializer,
    AuthorSerializer,
    AuthorListSerializer,
    AuthorRetrieveSerializer,
    BookListSerializer,
    BookRetrieveSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer

        if self.action == "retrieve":
            return AuthorRetrieveSerializer

        return super().get_serializer_class()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookRetrieveSerializer

        return super().get_serializer_class()
