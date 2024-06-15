from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingViewSet


app_name = "borrowings"

router = routers.DefaultRouter()

router.register("borrowings", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
