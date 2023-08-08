from rest_framework import viewsets, permissions

from screenshots.viewsets.permissions import IsOwner


class BaseModelViewSetMixin(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]
