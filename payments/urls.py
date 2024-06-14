from django.urls import path, include
from rest_framework import routers

from payments.views import PaymentView

router = routers.DefaultRouter()
router.register("", PaymentView, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "payments"
