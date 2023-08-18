import factory

from screenshots.models.user_data import UserData


class UserDataFactory(factory.django.DjangoModelFactory):
    owner = None
    screenshot_total_count = 0
    screenshot_total_size = 0

    class Meta:
        model = UserData
        django_get_or_create = ("owner",)
