from django.contrib import admin
from books.models import Book, Author
from django.contrib.auth.models import Group

admin.site.register(Book)
admin.site.register(Author)

admin.site.unregister(Group)
