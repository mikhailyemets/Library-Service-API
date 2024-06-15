from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books.models import Book, Author
from books.serializers import BookSerializer, AuthorSerializer, \
    AuthorListSerializer, AuthorRetrieveSerializer, BookListSerializer, \
    BookRetrieveSerializer
from books.permissions import IsAdminOrReadOnly


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


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookRetrieveSerializer

        return super().get_serializer_class()
