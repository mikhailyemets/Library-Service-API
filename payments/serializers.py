from rest_framework import serializers

from payments.models import Payment
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer
)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
