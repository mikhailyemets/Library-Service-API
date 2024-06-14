import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book
from borrowings.models import Borrowing


def send_telegram_message(message, object_type):
    """
    Sends a message to the Telegram bot depending on the object type.
    :param message: The message to be sent.
    :param object_type: The type of object (book or borrowing).
    :return:
    """
    token = '7131670430:AAHm9egBs0ASAXWBTnPk0uUbesWnTp5UmMY'
    chat_id = '992655456'

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print("Message sent successfully to Telegram!")
    else:
        print("Error sending message to Telegram.")


@receiver(post_save, sender=Book)
def send_telegram_notification_book(sender, instance, created, **kwargs):
    if created:
        book_title = instance.title
        message = f"New book: '{book_title}' was added to the Library!"
        send_telegram_message(message, "book")


@receiver(post_save, sender=Borrowing)
def send_telegram_notification_borrowing(sender, instance, created, **kwargs):
    if created:
        borrowing_info = f"ID: {instance.id}, Book: {instance.book.title}, Expected Return Date: {instance.expected_return_date}"
        message = f"New Borrowing: {borrowing_info}"
        send_telegram_message(message, "borrowing")

