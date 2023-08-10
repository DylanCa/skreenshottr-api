from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from screenshots.models import User
from screenshots.serializers import UserSerializer
from screenshots.viewsets.permissions import IsOwner


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]

    def get_object(self) -> User:
        return self.request.user

    @action(methods=['GET', 'PATCH'], detail=False)
    def me(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.method == 'PATCH':
            serializer = self.get_serializer(instance,
                                             data=self.request.data,
                                             partial=True)
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()

        data = self.get_serializer(instance=instance).data
        return Response(data=data)

    @action(methods=['DELETE'], detail=False, url_path='me/deactivate')
    def deactivate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
