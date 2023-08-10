import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from screenshots.tests.factories import UserFactory

from rest_framework.test import APIClient

from . import ViewsetTestsHelper


@pytest.mark.django_db
class TestUserViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_get_me(self):
        self.setup_method()

        path = '/me/'

        response = ViewsetTestsHelper.get_response(self.client, 'GET', path, self.user)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert data['id'] == self.user.id
        assert data['first_name'] == self.user.first_name
        assert data['last_name'] == self.user.last_name
        assert data['username'] == self.user.username
        assert data['email'] == self.user.email

    def test_patch_me(self):
        self.setup_method()

        path = '/me/'
        data = {"first_name": "First Name",
                "last_name": "Last Name",
                "email": "test@toto.fr",
                "username": "test_username"}

        response = ViewsetTestsHelper.get_response(self.client, 'PATCH', path, self.user, data=data)

        data = response.data
        self.user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert self.user.username == "test_username" == data['username']
        assert self.user.first_name == "First Name" == data['first_name']
        assert self.user.last_name == "Last Name" == data['last_name']
        assert self.user.email == "test@toto.fr" == data['email']

    def test_patch_me_cant_take_taken_email(self):
        self.setup_method()

        user2 = UserFactory(username="test2", email="test2@toto.fr")
        path = '/me/'
        data = {"email": user2.email}

        response = ViewsetTestsHelper.get_response(self.client, 'PATCH', path, self.user, data=data)

        data = response.data

        expected_error = ErrorDetail(string="This email is already in use.", code='invalid')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['email'][0].title() == expected_error.title()
        assert data['email'][0].code == expected_error.code

    def test_patch_me_cant_take_taken_username(self):
        self.setup_method()

        user2 = UserFactory(username="test2")

        path = '/me/'
        data = {"username": user2.username}

        response = ViewsetTestsHelper.get_response(self.client, 'PATCH', path, self.user, data=data)

        data = response.data

        expected_error = ErrorDetail(string="A User With That Username Already Exists.", code='unique')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['username'][0].title() == expected_error.title()
        assert data['username'][0].code == expected_error.code
