from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import (
    AuthorSerializer,
    AuthorListSerializer,
    AuthorRetrieveSerializer,
    BookSerializer,
    BookListSerializer,
    BookRetrieveSerializer
)

author_schema = {
    "list": extend_schema(
        responses=AuthorListSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Authors.",
                description="A sample example of a list of Authors.",
                value=[
                    {
                        "id": 1,
                        "name": "J.K. Rowling",
                        "birthdate": "1965-07-31"
                    },
                    {
                        "id": 2,
                        "name": "George R.R. Martin",
                        "birthdate": "1948-09-20"
                    },
                ],
            )
        ],
    ),
    "retrieve": extend_schema(
        responses=AuthorRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Retrieve Example",
                summary="Example response for retrieving an Author.",
                description="A sample example of an Author detail.",
                value={
                    "id": 1,
                    "name": "J.K. Rowling",
                    "birthdate": "1965-07-31",
                    "books": [
                        {
                            "id": 1,
                            "title": "Harry Potter and the Philosopher's Stone",
                        }
                    ]
                },
            )
        ],
    ),
    "create": extend_schema(
        request=AuthorSerializer,
        responses=AuthorSerializer,
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating an Author.",
                description="A sample example of creating an Author.",
                value={
                    "name": "J.K. Rowling",
                    "birthdate": "1965-07-31"
                },
            )
        ],
    ),
    "update": extend_schema(
        request=AuthorSerializer,
        responses=AuthorSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating an Author.",
                description="A sample example of updating an Author.",
                value={
                    "name": "J.K. Rowling Updated",
                    "birthdate": "1965-07-31"
                },
            )
        ],
    ),
    "partial_update": extend_schema(
        request=AuthorSerializer,
        responses=AuthorSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating an Author.",
                description="A sample example of partially updating an Author.",
                value={"name": "J.K. Rowling"},
            )
        ],
    ),
    "destroy": extend_schema(
        responses={"204": None},
    ),
}

book_schema = {
    "list": extend_schema(
        responses=BookListSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Books.",
                description="A sample example of a list of Books.",
                value=[
                    {
                        "id": 1,
                        "title": "Harry Potter and the Philosopher's Stone",
                        "author": {
                            "id": 1,
                            "name": "J.K. Rowling"
                        },
                        "published_date": "1997-06-26"
                    },
                    {
                        "id": 2,
                        "title": "A Game of Thrones",
                        "author": {
                            "id": 2,
                            "name": "George R.R. Martin"
                        },
                        "published_date": "1996-08-06"
                    },
                ],
            )
        ],
    ),
    "retrieve": extend_schema(
        responses=BookRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Retrieve Example",
                summary="Example response for retrieving a Book.",
                description="A sample example of a Book detail.",
                value={
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "author": {
                        "id": 1,
                        "name": "J.K. Rowling"
                    },
                    "published_date": "1997-06-26"
                },
            )
        ],
    ),
    "create": extend_schema(
        request=BookSerializer,
        responses=BookSerializer,
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a Book.",
                description="A sample example of creating a Book.",
                value={
                    "title": "Harry Potter and the Philosopher's Stone",
                    "author": 1,
                    "published_date": "1997-06-26"
                },
            )
        ],
    ),
    "update": extend_schema(
        request=BookSerializer,
        responses=BookSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating a Book.",
                description="A sample example of updating a Book.",
                value={
                    "title": "Harry Potter and the Philosopher's Stone Updated",
                    "author": 1,
                    "published_date": "1997-06-26"
                },
            )
        ],
    ),
    "partial_update": extend_schema(
        request=BookSerializer,
        responses=BookSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating a Book.",
                description="A sample example of partially updating a Book.",
                value={"title": "Harry Potter and the Philosopher's Stone"},
            )
        ],
    ),
    "destroy": extend_schema(
        responses={"204": None},
    ),
}

