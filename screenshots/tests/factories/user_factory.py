import factory

from screenshots.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = 'bobibop'
    first_name = 'Bob'
    last_name = 'Bibop'
    email = 'bob.bibop@gmail.com'
    password = factory.django.Password('password')

    is_superuser = False
    is_staff = False

    class Meta:
        model = User
        django_get_or_create = ('username', 'email',)
