from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import UserSerializer, CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Це endpoint для реєстрації, використовуйте POST"},
            status=200
        )


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
