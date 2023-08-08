import os

from rest_framework import serializers

from screenshots.lib import ImageHelper
from screenshots.models import Screenshot
from screenshots.serializers import TagSerializer
from screenshots.serializers.mixins import BaseModelSerializerMixin


class ScreenshotSerializer(BaseModelSerializerMixin):
    name = serializers.CharField(max_length=128, required=False)
    file = serializers.ImageField(write_only=True, required=True)
    tags = TagSerializer(many=True, read_only=True)
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Screenshot
        fields = ["id", "name", "file", "file_url", "tags", "owner_id"]
        read_only_fields = ["file_url"]
