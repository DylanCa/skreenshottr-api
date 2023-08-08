from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from screenshots.models import User
from screenshots.serializers.change_password import ChangePasswordSerializer


class ChangePasswordViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self) -> User:
        return self.request.user

    @action(methods=['PUT'], detail=False, url_path='me/change_password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
