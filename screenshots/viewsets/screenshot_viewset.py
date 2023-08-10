from screenshots.models import Screenshot
from screenshots.serializers import ScreenshotSerializer
from .mixins import BaseModelViewSetMixin


class ScreenshotViewSet(BaseModelViewSetMixin):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Screenshot.objects.filter(owner=self.request.user).order_by('id')
