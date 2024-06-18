from random import randint, sample

from django.core.management.base import BaseCommand
from faker import Faker

from books.models import Book, Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        unique_fake = Faker().unique
        fake = Faker()

        all_covers = tuple(i[0] for i in Book.COVER_CHOICES)
        all_authors = list(Author.objects.all())
        for _ in range(10):
            book = Book.objects.create(
                title=unique_fake.sentence(nb_words=3),
                cover=fake.random_element(elements=all_covers),
                inventory=fake.random_digit_not_null(),
                daily_fee=fake.random_digit_not_null(),
            )
            book_authors = sample(
                all_authors,
                min(randint(1, 3), len(all_authors))
            )
            book.authors.set(book_authors)
