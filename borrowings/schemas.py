from drf_spectacular.utils import extend_schema, OpenApiExample

borrowing_schema = extend_schema_view(
    list=extend_schema(
        responses=BorrowingListSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Borrowings.",
                description="A sample example of a list of Borrowings.",
                value=[
                    {
                        "id": 1,
                        "book": {"id": 1, "title": "The Great Gatsby"},
                        "user": {"id": 1, "username": "user1"},
                        "borrow_date": "2023-01-01",
                        "expected_return_date": "2023-01-10",
                        "actual_return_date": None,
                        "is_active": True
                    },
                    {
                        "id": 2,
                        "book": {"id": 2, "title": "1984"},
                        "user": {"id": 2, "username": "user2"},
                        "borrow_date": "2023-01-05",
                        "expected_return_date": "2023-01-15",
                        "actual_return_date": "2023-01-12",
                        "is_active": False
                    },
                ],
            )
        ],
    ),
    retrieve=extend_schema(
        responses=BorrowingRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Retrieve Example",
                summary="Example response for retrieving a Borrowing.",
                description="A sample example of a Borrowing detail.",
                value={
                    "id": 1,
                    "book": {"id": 1, "title": "The Great Gatsby"},
                    "user": {"id": 1, "username": "user1"},
                    "borrow_date": "2023-01-01",
                    "expected_return_date": "2023-01-10",
                    "actual_return_date": None,
                    "is_active": True
                },
            )
        ],
    ),
    create=extend_schema(
        request=BorrowingCreateSerializer,
        responses=BorrowingRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a Borrowing.",
                description="A sample example of creating a Borrowing.",
                value={
                    "book": 1,
                    "user": 1,
                    "borrow_date": "2023-01-01",
                    "expected_return_date": "2023-01-10"
                },
            )
        ],
    ),
    update=extend_schema(
        request=BorrowingRetrieveSerializer,
        responses=BorrowingRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating a Borrowing.",
                description="A sample example of updating a Borrowing.",
                value={
                    "book": 1,
                    "user": 1,
                    "borrow_date": "2023-01-01",
                    "expected_return_date": "2023-01-10",
                    "actual_return_date": "2023-01-09"
                },
            )
        ],
    ),
    partial_update=extend_schema(
        request=BorrowingRetrieveSerializer,
        responses=BorrowingRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating a Borrowing.",
                description="A sample example of partially updating a Borrowing.",
                value={"actual_return_date": "2023-01-09"},
            )
        ],
    ),
    destroy=extend_schema(
        responses={"204": None},
    ),
)

