from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer
)
from rest_framework import serializers

from payments.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    borrowing = BorrowingListSerializer()

    class Meta:
        model = Payment
        fields = (
            'id',
            'borrowing',
            'status',
            'type',
            "money_to_pay",
            "date_added"
        )


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    borrowing = BorrowingRetrieveSerializer()

    class Meta:
        model = Payment
        fields = "__all__"
