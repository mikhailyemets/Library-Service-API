from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        unique_together = (("first_name", "last_name"),)
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    COVER_CHOICES = [
        ("Hard", "Hard"),
        ("Soft", "Soft"),
    ]

    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(
        Author,
        max_length=255,
        related_name="books"
    )
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES,
        default="Hard"
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        authors_str = ", ".join([str(author) for author in self.authors.all()])
        return (f"{self.title}, "
                f"Authors: {authors_str}, "
                f"Cover: {self.cover}, "
                f"Inventory: {self.inventory}, "
                f"Daily Fee: {self.daily_fee} $")

