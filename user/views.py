from rest_framework import generics
from rest_framework.permissions import IsAuthenticated as DRFIsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer
from user.schemas import create_user_schema, create_token_schema, manage_user_schema  # Import schemas


@create_user_schema
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


@create_token_schema
class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


@manage_user_schema
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (DRFIsAuthenticated,)

    def get_object(self):
        return self.request.user
