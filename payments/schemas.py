from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view

from payments.serializers import PaymentRetrieveSerializer, PaymentListSerializer


payment_schema = extend_schema_view(
    list=extend_schema(
        responses=PaymentListSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Payments.",
                description="A sample example of a list of Payments.",
                value=[
                    {
                        "id": 1,
                        "borrowing": {"id": 1, "book": "The Great Gatsby"},
                        "status": "pending",
                        "money_to_pay": "10.00",
                        "last_update": "2023-01-01"
                    },
                    {
                        "id": 2,
                        "borrowing": {"id": 2, "book": "1984"},
                        "status": "paid",
                        "money_to_pay": "15.00",
                        "last_update": "2023-01-05"
                    },
                ],
            )
        ],
    ),
    retrieve=extend_schema(
        responses=PaymentRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Retrieve Example",
                summary="Example response for retrieving a Payment.",
                description="A sample example of a Payment detail.",
                value={
                    "id": 1,
                    "borrowing": {"id": 1, "book": "The Great Gatsby"},
                    "status": "pending",
                    "money_to_pay": "10.00",
                    "last_update": "2023-01-01"
                },
            )
        ],
    ),
)

success_payment_schema = extend_schema_view(
    get=extend_schema(
        responses={"200": None, "404": None},
        examples=[
            OpenApiExample(
                "Success Example",
                summary="Example response for successful payment.",
                description="A sample example of a successful payment.",
                value={"detail": "Payment successful."},
            )
        ],
    ),
)

cancel_payment_schema = extend_schema_view(
    get=extend_schema(
        responses={"200": None},
        examples=[
            OpenApiExample(
                "Cancel Example",
                summary="Example response for canceled payment.",
                description="A sample example of a canceled payment.",
                value={"detail": "Payment can be made later. The session is available for only 24 hours."},
            )
        ],
    ),
)
