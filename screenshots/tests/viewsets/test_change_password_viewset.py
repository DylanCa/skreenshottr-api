import pytest
from rest_framework import status

from screenshots.tests.factories import UserFactory

from rest_framework.test import APIClient

from . import ViewsetTestsHelper


@pytest.mark.django_db
class TestChangePasswordViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_change_password(self):
        self.setup_method()

        password = "NewPassword123"

        path = '/me/change_password/'
        data = {"old_password": "password",
                "password": password,
                "password2": password}

        response = ViewsetTestsHelper.get_response(self.client, 'PUT', path, self.user, data=data)

        self.user.refresh_from_db()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.user.check_password(password)

    def test_wrong_old_password(self):
        self.setup_method()

        password = "NewPassword123"

        path = '/me/change_password/'
        data = {"old_password": "wrong_password",
                "password": password,
                "password2": password}

        response = ViewsetTestsHelper.get_response(self.client, 'PUT', path, self.user, data=data)

        data = response.data
        self.user.refresh_from_db()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['old_password']['old_password'].title() == 'Old Password Is Not Correct'
        assert self.user.check_password("password")

    def test_password_dont_match(self):
        self.setup_method()

        path = '/me/change_password/'
        data = {"old_password": "password",
                "password": "NewPassword123",
                "password2": "NewPassword1234"}

        response = ViewsetTestsHelper.get_response(self.client, 'PUT', path, self.user, data=data)

        data = response.data
        self.user.refresh_from_db()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data['password'][0].title() == "Password Fields Didn'T Match."
        assert self.user.check_password("password")
