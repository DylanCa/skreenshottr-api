import pytest
from rest_framework import status

from screenshots.tests.factories import UserFactory

from rest_framework.test import APIClient

from ...models import User


@pytest.mark.django_db
class TestRegisterViewSet:
    def test_register(self):
        client = APIClient()

        path = '/register/'
        data = {"username": "Bob",
                "email": "bob@bibop.fr",
                "password": "Bobibop1234",
                "password2": "Bobibop1234"}

        response = client.post(path, data=data)

        user = User.objects.get(email=data['email'])

        assert response.status_code == status.HTTP_201_CREATED
        assert user.username == data['username']
        assert user.email == data['email']
        assert user.check_password(data['password'])

    def test_register_cant_take_unique_fields(self):
        client = APIClient()
        user = UserFactory()

        path = '/register/'
        data = {"username": user.username,
                "email": user.email,
                "password": "NewPassword1234",
                "password2": "NewPassword1234"}

        response = client.post(path, data=data)

        data = response.data
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['username'][0].title() == 'A User With That Username Already Exists.'
        assert data['email'][0].title() == 'This Field Must Be Unique.'

    def test_passwords_must_match(self):
        client = APIClient()

        path = '/register/'
        data = {"username": "Bob",
                "email": "bob@bibop.fr",
                "password": "Bobibop1234",
                "password2": "Bobibop12345"}

        response = client.post(path, data=data)
        data = response.data

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['password'][0].title() == "Password Fields Didn'T Match."
