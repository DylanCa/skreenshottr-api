import os

from PIL import Image
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
        fields = ["id", "name", "description", "file", "filename", "image_url", "thumbnail_url", "format", "size", "width", "height", "tags", "owner_id"]
        read_only_fields = [ "filename", "image_url", "thumbnail_url", "format", "size", "width", "height"]

    def validate(self, attrs):
        attrs = self.validate_owner(attrs)
        user = attrs['owner']

        if "file" in attrs:
            file = attrs.pop('file')
            filename = file.name

            with Image.open(file) as image:
                attrs['filename'] = filename
                attrs['format'] = image.format
                attrs['width'] = image.width
                attrs['height'] = image.height
                attrs['size'] = file.size

                image_url, thumbnail_url = ImageHelper.upload_image_to_storage(image, filename, user.id)

                attrs['image_url'] = image_url
                attrs['thumbnail_url'] = thumbnail_url

            if "name" not in attrs:
                filename = os.path.splitext(file.name)[0]
                attrs['name'] = filename

        return attrs
