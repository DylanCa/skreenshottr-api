import factory

from screenshots.models import Tag
from . import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    name = "Tag 123"
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Tag
        django_get_or_create = ("name",)
