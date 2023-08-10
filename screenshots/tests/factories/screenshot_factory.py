import factory

from screenshots.models import Screenshot
from . import UserFactory


class ScreenshotFactory(factory.django.DjangoModelFactory):
    name = "Screenshot"
    file_url = "http://test.com"
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Screenshot
