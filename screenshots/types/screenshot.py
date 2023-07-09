from graphene_django import DjangoObjectType

from screenshots.models import Screenshot


class ScreenshotType(DjangoObjectType):
    class Meta:
        model = Screenshot
        fields = ("id", "file_url", "tags", )
