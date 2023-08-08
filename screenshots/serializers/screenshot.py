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

    def validate(self, attrs):
        attrs = self.validate_owner(attrs)
        user = attrs['owner']

        if "file" in attrs:
            file = attrs.pop('file')
            file_url = ImageHelper.upload_to_storage(file,
                                                     user.id)
            attrs['file_url'] = file_url

            if "name" not in attrs:
                filename = os.path.splitext(file.name)[0]
                attrs['name'] = filename

        return attrs
