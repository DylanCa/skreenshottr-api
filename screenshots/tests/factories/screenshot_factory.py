import factory

from screenshots.models import Screenshot
from . import UserFactory


class ScreenshotFactory(factory.django.DjangoModelFactory):
    name = "Screenshot"
    image_url = "http://test.com"
    thumbnail_url = "http://test.com/thumbnail"
    filename = "screenshot.png"
    size = 20_000
    width = 1920
    height = 1080
    format = "PNG"
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Screenshot
