import pytest
from django.contrib.auth.hashers import check_password

from screenshots.tests.factories import UserFactory


@pytest.mark.django_db
class TestUser:
    def test_fields(self):
        user = UserFactory()

        assert user.username == 'bobibop'
        assert user.first_name == 'Bob'
        assert user.last_name == 'Bibop'
        assert user.email == 'bob.bibop@gmail.com'
        assert not user.is_staff
        assert not user.is_superuser
        assert check_password("password", user.password)
        assert user.__str__() == user.username
