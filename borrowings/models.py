from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrowings")
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="borrowings"
    )

    class Meta:
        ordering = ("expected_return_date", "borrow_date")
        constraints = [
            models.CheckConstraint(
                check=Q(borrow_date__lt=F("expected_return_date")),
                name="Expected return date should be more than borrowing date",
            ),
            models.CheckConstraint(
                check=Q(borrow_date__lte=F("actual_return_date")),
                name="Actual return date should be equal or more than borrowing date",
            ),
        ]

    def __str__(self):
        return f"Borrowing id: {self.id}  (expired: {self.expected_return_date})"
