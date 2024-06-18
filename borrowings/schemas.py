from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view, OpenApiParameter

from borrowings.serializers import BorrowingCreateSerializer, BorrowingRetrieveSerializer, BorrowingListSerializer


borrowing_schema = extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.STR,
                description=(
                    "Filter by active borrowings (ex. ?is_active=true)."
                ),
            ),
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                description=(
                    "Filter by user ids (ex. ?User_id=1)."
                ),
            )
        ],
        responses=BorrowingListSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Borrowings.",
                description="A sample example of a list of Borrowings.",
                value=[
                    {
                        "id": 1,
                        "book": "The Great Gatsby",
                        "user": "user@user.com",
                        "borrow_date": "2023-01-01",
                        "expected_return_date": "2023-01-10",
                        "actual_return_date": None,
                    },
                    {
                        "id": 2,
                        "book": "1984",
                        "user": "user2@user.com",
                        "borrow_date": "2023-01-05",
                        "expected_return_date": "2023-01-15",
                        "actual_return_date": "2023-01-12",
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
                    "book": {
                        "id": 1,
                        "title": "The Great Gatsby",
                        "authors": [1],
                        "cover": "Hard",
                        "inventory": 1,
                        "daily_fee": "1.00"
                    },
                    "user": {
                        "id": 1,
                        "email": "user@user.com",
                        "is_staff": "false"
                    },
                    "borrow_date": "2023-01-01",
                    "expected_return_date": "2023-01-10",
                    "actual_return_date": None,
                },
            )
        ],
    ),
    create=extend_schema(
        request=BorrowingCreateSerializer,
        responses=BorrowingCreateSerializer,
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a Borrowing.",
                description="A sample example of creating a Borrowing.",
                value={
                    "book": 1,
                    "expected_return_date": "2023-01-10"
                },
            )
        ],
    ),
    book_return=extend_schema(
        responses=BorrowingRetrieveSerializer
    )
)
