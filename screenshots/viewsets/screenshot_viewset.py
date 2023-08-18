from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .mixins import BaseModelViewSetMixin
from ..models.screenshot import Screenshot
from ..serializers.screenshot_serializer import ScreenshotSerializer


class ScreenshotViewSet(BaseModelViewSetMixin):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'description', 'filename', 'format', 'application__name', 'tags__name']
    search_fields = filterset_fields
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Screenshot.objects.filter(owner=self.request.user).order_by("id")
