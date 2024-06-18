from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    extend_schema_view
)

from user.serializers import UserSerializer, AuthTokenSerializer

create_user_schema = extend_schema_view(
    post=extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        examples=[
            OpenApiExample(
                "Create User Example",
                summary="Example for creating a user.",
                description="A sample example of creating a user.",
                value={
                    "email": "user@example.com",
                    "password": "password123",
                    "name": "John Doe"
                },
            )
        ],
    ),
)

create_token_schema = extend_schema_view(
    post=extend_schema(
        request=AuthTokenSerializer,
        responses={"token": "string"},
        examples=[
            OpenApiExample(
                "Create Token Example",
                summary="Example for creating a token.",
                description="A sample example of creating a token.",
                value={
                    "email": "user@example.com",
                    "password": "password123"
                },
            )
        ],
    ),
)

manage_user_schema = extend_schema_view(
    get=extend_schema(
        responses=UserSerializer,
        examples=[
            OpenApiExample(
                "Retrieve User Example",
                summary="Example response for retrieving a user.",
                description="A sample example of retrieving a user's details.",
                value={
                    "email": "user@example.com",
                    "name": "John Doe"
                },
            )
        ],
    ),
    put=extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        examples=[
            OpenApiExample(
                "Update User Example",
                summary="Example for updating a user.",
                description="A sample example of updating a user's details.",
                value={
                    "email": "user@example.com",
                    "password": "newpassword123",
                    "name": "John Doe Updated"
                },
            )
        ],
    ),
    patch=extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        examples=[
            OpenApiExample(
                "Partial Update User Example",
                summary="Example for partially updating a user.",
                description="A sample example of partially updating a user's details.",
                value={"name": "John Doe"},
            )
        ],
    ),
)

