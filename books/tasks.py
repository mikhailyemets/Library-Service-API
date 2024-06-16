from celery import shared_task
from telegram_bot.bot import send_telegram_file
from decouple import config


def write_books_to_file(books_data, file_path='books.txt'):
    """
    Writes books to a file.
    :param books_data:
    :param file_path:
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("Books\n")
        for idx, books in enumerate(books_data, start=1):
            file.write(f"{idx}) {books}\n")


@shared_task
def scheduled_task():
    """
    This function is called every 24 hours at 19:00.
    To save and show all books that are in stock.
    :return:
    """
    from books.models import Book
    from books.serializers import BookRetrieveSerializer

    books = Book.objects.all().filter(inventory__gt=0)
    serializer = BookRetrieveSerializer(books, many=True)
    books_data = serializer.data

    write_books_to_file(books_data)
    file_path = 'books.txt'

    token = config("TG_TOKEN")
    chat_id = config("TG_CHAT_ID")

    send_telegram_file(file_path, token, chat_id)

    return f"Books: {books_data}"
