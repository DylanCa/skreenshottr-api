import pytest

from screenshots.models import User
from screenshots.serializers import UserSerializer
from screenshots.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserSerializer:
    def test_fields(self):
        data = {'id': 1234,
                'email': "test@toto.fr",
                'username': 'Testoto',
                'first_name': 'test',
                'last_name': 'toto'}

        serializer = UserSerializer(data=data)

        assert serializer.is_valid()

        result = serializer.save()
        user = User.objects.first()
        assert result == user

        validated_data = serializer.validated_data
        assert 'id' not in validated_data
        assert validated_data['email'] == data['email']
        assert validated_data['username'] == data['username']
        assert validated_data['first_name'] == data['first_name']
        assert validated_data['last_name'] == data['last_name']
        assert len(serializer.errors) == 0

    def test_email_required(self):
        data = {'username': 'Testoto',
                'first_name': 'test',
                'last_name': 'toto'}

        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors['email'][0].title() == "This Field Is Required."
        assert len(serializer.errors) == 1

    def test_validate_username(self):
        email = 'test@toto.fr'
        data = {'email': email,
                'username': 'Testoto',
                'first_name': 'test',
                'last_name': 'toto'}

        UserFactory(email=email)

        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors['email'][0].title() == 'This Email Is Already In Use.'
        assert len(serializer.errors) == 1

    def test_validate_email(self):
        username = 'Testoto'
        data = {'email': 'test@toto.fr',
                'username': username,
                'first_name': 'test',
                'last_name': 'toto'}

        UserFactory(username=username)

        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors['username'][0].title() == 'A User With That Username Already Exists.'
        assert len(serializer.errors) == 1
