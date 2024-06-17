from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path('api/', include('books.urls')),
    path("api/payments/", include("payments.urls", namespace="payments")),
    path("api/borrowings/", include("borrowings.urls", namespace="borrowings")),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
