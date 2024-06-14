from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

from books.models import Book

from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram_bot.bot import send_telegram_message


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


@receiver(post_save, sender=Borrowing)
def send_telegram_notification_borrowing(sender, instance, created, **kwargs):
    if created:
        borrowing_info = f"ID: {instance.id}, User: {instance.user.username}, Book: {instance.book.title}, Expected Return Date: {instance.expected_return_date}"
        message = f"New Borrowing: {borrowing_info}"
        send_telegram_message(message)
