from celery import shared_task
import datetime
from decouple import config
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowings.models import Borrowing
from telegram_bot.bot import send_telegram_message, send_telegram_file


def write_borrowings_to_file(borrow_data, file_path='borrowings.txt'):
    """
    Writes borrowings to a file.
    :param borrow_data:
    :param file_path:
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("Borrowings\n")
        for idx, borrowing in enumerate(borrow_data, start=1):
            file.write(f"{idx}) {borrowing}\n")


@shared_task
def scheduled_task():
    """
    This function is called every 24 hours at 19:00.
    To save all borrowings that are not returned yet.
    :return:
    """
    from borrowings.models import Borrowing
    from borrowings.serializers import BorrowingSerializer

    borrowings = Borrowing.objects.all().filter(actual_return_date__isnull=True)
    serializer = BorrowingSerializer(borrowings, many=True)
    borrow_data = serializer.data

    write_borrowings_to_file(borrow_data)

    file_path = 'borrowings.txt'

    token = "7131670430:AAHm9egBs0ASAXWBTnPk0uUbesWnTp5UmMY"
    chat_id = "992655456"

    send_telegram_file(file_path, token, chat_id)

    return f"Borrowings: {borrow_data}"


@shared_task
def send_overdue_borrowings_notification():
    """
    Sends notification about overdue borrowings every 4 hour.
    :return:
    """
    from borrowings.models import Borrowing
    from borrowings.serializers import BorrowingSerializer
    current_date = datetime.date.today()

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=current_date + datetime.timedelta(days=1),
        actual_return_date__isnull=True)

    notification_message = ""

    for idx, borrowing in enumerate(overdue_borrowings, start=1):
        serializer = BorrowingSerializer(borrowing)
        borrowing_data = serializer.data

        borrowing_info = "----------------------\n"
        borrowing_info += f"Overdue Borrowing {idx}: \n"
        borrowing_info += f"User: {borrowing_data['user']}\n"
        borrowing_info += f"Book ID: {borrowing_data['book']}\n"
        borrowing_info += f"Borrow Date: {borrowing_data['borrow_date']}\n"
        borrowing_info += f"Expected Return Date: {borrowing_data['expected_return_date']}\n\n"
        borrowing_info = "----------------------\n"
        notification_message += borrowing_info

        send_telegram_message(notification_message)

    return f"Notifications sent for {len(overdue_borrowings)} overdue borrowings"
