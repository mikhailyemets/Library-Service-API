from django.core.management.base import BaseCommand
from faker import Faker

from books.models import Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker().unique
        authors = [
            Author(
                first_name=faker.first_name(),
                last_name=faker.last_name()
            )
            for _ in range(10)
        ]

        Author.objects.bulk_create(authors, ignore_conflicts=True)
