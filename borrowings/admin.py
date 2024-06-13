from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "book", "borrow_date", "expected_return_date", "actual_return_date")
