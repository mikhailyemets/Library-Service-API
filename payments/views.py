from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

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
