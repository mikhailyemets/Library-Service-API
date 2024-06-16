from celery import shared_task

from time import sleep


@shared_task
def my_task():
    print("start task")
    sleep(3)
    print("end task")


@shared_task
def another_task():
    print("start another task")
    sleep(5)
    print("end another task")


@shared_task
def scheduled_task():
    from books.models import Book
    from books.serializers import BookSerializer

    books = Book.objects.all().filter(inventory__gt=0)
    serializer = BookSerializer(books, many=True)
    books_data = serializer.data
    return f"Books: {books_data}"
