from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .mixins import BaseModelViewSetMixin
from ..models.application import Application
from ..serializers.application_serializer import ApplicationSerializer


class ApplicationViewSet(BaseModelViewSetMixin):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = filterset_fields
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user).order_by("id")
