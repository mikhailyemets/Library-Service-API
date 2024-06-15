from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer
)
from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentListSerializer(PaymentSerializer):
    borrowing = BorrowingListSerializer()


class PaymentRetrieveSerializer(PaymentSerializer):
    borrowing = BorrowingRetrieveSerializer()
