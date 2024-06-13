from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer

        return BorrowingSerializer
