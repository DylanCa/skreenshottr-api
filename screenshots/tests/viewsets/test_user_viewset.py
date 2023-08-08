import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from screenshots.tests.factories import UserFactory

from rest_framework.test import force_authenticate, APIClient, APIRequestFactory


def assert_not_auth(response):
    expected_error = ErrorDetail(string="Authentication Credentials Were Not Provided.", code='not_authenticated')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'].title() == expected_error.title()
    assert response.data['detail'].code == expected_error.code


@pytest.mark.django_db
class TestUserViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory(password="test")

    def test_get_me_not_auth(self):
        self.setup_method()

        response = self.client.get('/me/')
        assert_not_auth(response)

    def test_patch_not_auth(self):
        self.setup_method()

        response = self.client.patch('/me/')
        assert_not_auth(response)

    def test_get_me(self):
        self.setup_method()

        self.client.login(username=self.user.username, password="test")
        response = self.client.get('/me/')
        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert data['id'] == self.user.id
        assert data['first_name'] == self.user.first_name
        assert data['last_name'] == self.user.last_name
        assert data['username'] == self.user.username
        assert data['email'] == self.user.email

    def test_patch_me(self):
        self.setup_method()

        self.client.login(username=self.user.username, password="test")
        response = self.client.patch('/me/', data={"first_name": "First Name",
                                                   "last_name": "Last Name",
                                                   "email": "test@toto.fr",
                                                   "username": "test_username"})
        data = response.data

        self.user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert self.user.username == "test_username"
        assert self.user.first_name == "First Name"
        assert self.user.last_name == "Last Name"
        assert self.user.email == "test@toto.fr"

    def test_patch_me_cant_take_taken_email(self):
        self.setup_method()

        user2 = UserFactory(username="test2", email="test2@toto.fr")

        self.client.login(username=self.user.username, password="test")
        response = self.client.patch('/me/', data={"email": user2.email})
        data = response.data

        expected_error = ErrorDetail(string="This email is already in use.", code='invalid')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['email'][0].title() == expected_error.title()
        assert data['email'][0].code == expected_error.code

    def test_patch_me_cant_take_taken_username(self):
        self.setup_method()

        user2 = UserFactory(username="test2")

        self.client.login(username=self.user.username, password="test")
        response = self.client.patch('/me/', data={"username": user2.username})
        data = response.data

        expected_error = ErrorDetail(string="A User With That Username Already Exists.", code='unique')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['username'][0].title() == expected_error.title()
        assert data['username'][0].code == expected_error.code
