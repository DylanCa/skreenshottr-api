from rest_framework import viewsets

from screenshots.models import Tag, Screenshot
from screenshots.serializers import TagSerializer
from .mixins import BaseModelViewSetMixin


class TagViewSet(BaseModelViewSetMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
