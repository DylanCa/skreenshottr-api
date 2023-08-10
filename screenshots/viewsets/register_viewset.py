from rest_framework import generics
from rest_framework.permissions import AllowAny

from screenshots.models import User
from screenshots.serializers import RegisterSerializer


class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
