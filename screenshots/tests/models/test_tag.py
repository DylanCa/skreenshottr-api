import pytest

from screenshots.tests.factories import UserFactory, TagFactory


@pytest.mark.django_db
class TestTag:
    def test_fields(self):
        tag = TagFactory()

        assert tag.name == "Tag 123"
        assert tag.__str__() == "Tag 123"
        assert tag.owner

    def test_tag_with_owner(self):
        user = UserFactory()
        tag = TagFactory(owner=user)

        assert tag.owner == user
