import hashlib
import os

from PIL import Image
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from screenshots.lib.image_helper import ImageHelper
from screenshots.models.application import Application
from screenshots.models.screenshot import Screenshot
from screenshots.serializers.application_serializer import ApplicationSerializer
from screenshots.serializers.mixins import BaseModelSerializerMixin
from screenshots.serializers.tag_serializer import TagSerializer


class ScreenshotSerializer(BaseModelSerializerMixin):
    name = serializers.CharField(max_length=128, required=False)
    file = serializers.ImageField(write_only=True, required=True)
    tags = TagSerializer(many=True, read_only=True)
    application = ApplicationSerializer(required=False)
    owner_id = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Screenshot
        fields = [
            "id",
            "name",
            "description",
            "image_url",
            "application",
            "tags",
            "file",
            "filename",
            "thumbnail_url",
            "format",
            "size",
            "width",
            "height",
            "owner_id",
        ]
        read_only_fields = [
            "filename",
            "image_url",
            "thumbnail_url",
            "format",
            "size",
            "width",
            "height",
        ]

    def validate(self, attrs):
        attrs = self.validate_owner(attrs)
        user = attrs["owner"]

        if "file" in attrs:
            file = attrs.pop("file")
            filename = file.name

            with Image.open(file) as image:
                image_hash = hashlib.md5(image.tobytes()).hexdigest()

                instance = Screenshot.objects.filter(image_hash=image_hash, owner=user)

                if instance.count():
                    instance = instance.get()
                    raise ValidationError({'file': 'File already exists.',
                                           'duplicate_screenshot_id': instance.id}, code=status.HTTP_409_CONFLICT)

                attrs["image_hash"] = image_hash
                attrs["filename"] = filename
                attrs["format"] = image.format
                attrs["width"] = image.width
                attrs["height"] = image.height
                attrs["size"] = file.size

                image_url, thumbnail_url = ImageHelper.upload_image_to_storage(
                    image, filename, image_hash
                )

                attrs["image_url"] = image_url
                attrs["thumbnail_url"] = thumbnail_url

            if "name" not in attrs:
                filename = os.path.splitext(file.name)[0]
                attrs["name"] = filename

        return attrs

    def validate_application(self, value):
        application = None

        if 'name' in value:
            name = value.pop("name")
            application, _ = Application.objects.get_or_create(name=name, owner=self.get_owner())

        elif 'id' in value:
            uuid = value.pop("id")
            application = Application.objects.filter(id=uuid).get()

        return application
