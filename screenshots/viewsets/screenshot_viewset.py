from .mixins import BaseModelViewSetMixin
from ..models.screenshot import Screenshot
from ..serializers.screenshot_serializer import ScreenshotSerializer


class ScreenshotViewSet(BaseModelViewSetMixin):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Screenshot.objects.filter(owner=self.request.user).order_by("id")
