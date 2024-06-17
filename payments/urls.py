from django.urls import path, include
from rest_framework import routers

from payments.views import PaymentView, SuccessPaymentView, CancelPaymentView

router = routers.DefaultRouter()
router.register("", PaymentView, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
    path("success/", SuccessPaymentView.as_view(), name="success_payments"),
    path("cancel/", CancelPaymentView.as_view(), name="cancel_payment"),
]

app_name = "payments"
