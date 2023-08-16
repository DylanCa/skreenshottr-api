from datetime import datetime

import pytest
from rest_framework import status

from screenshots.tests.factories import UserFactory, TagFactory, ScreenshotFactory

from rest_framework.test import APIClient

from . import ViewsetTestsHelper
from ...models import Tag


@pytest.mark.django_db
class TestTagViewset:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user2 = UserFactory(username="user2", email="email2@toto.fr")
        self.tag1_u1 = TagFactory(name="Tag1, User 1", owner=self.user)
        self.tag2_u1 = TagFactory(name="Tag2, User 1", owner=self.user)
        self.tag1_u2 = TagFactory(name="Tag1, User 2", owner=self.user2)
        self.screenshot = ScreenshotFactory(owner=self.user)
        self.screenshot.tags.add(self.tag1_u1)

    def test_list_tags(self):
        self.setup_method()
        path = "/tags/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert self.tag1_u1 in data["results"].serializer.instance
        assert self.tag2_u1 in data["results"].serializer.instance
        assert self.tag1_u2 not in data["results"].serializer.instance

    def test_retrieve_tag(self):
        self.setup_method()
        path = f"/tags/{self.tag1_u1.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.tag1_u1.id)
        assert data["name"] == self.tag1_u1.name

    def test_cannot_retrieve_others_tag(self):
        self.setup_method()
        path = f"/tags/{self.tag1_u2.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_retrieve_deleted_tag(self):
        self.setup_method()

        self.tag1_u1.deleted_at = datetime.now()
        self.tag1_u1.save()

        path = f"/tags/{self.tag1_u1.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_tag(self):
        path = "/tags/"

        name = "Test Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "POST", path, self.user, data=data
        )

        data = response.data
        tag = Tag.objects.get(name=name, owner=self.user)

        assert response.status_code == status.HTTP_201_CREATED
        assert data["id"] == str(tag.id)
        assert data["name"] == name == tag.name

    def test_patch_tag(self):
        path = f"/tags/{self.tag2_u1.id}/"

        name = "Test Patch Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PATCH", path, self.user, data=data
        )

        data = response.data
        self.tag2_u1.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.tag2_u1.id)
        assert data["name"] == name == self.tag2_u1.name

    def test_cant_patch_not_owned_tag(self):
        path = f"/tags/{self.tag1_u2.id}/"

        name = "Test Patch Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PATCH", path, self.user, data=data
        )

        self.tag2_u1.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_tag(self):
        path = f"/tags/{self.tag2_u1.id}/"

        name = "Test Patch Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PUT", path, self.user, data=data
        )

        data = response.data
        self.tag2_u1.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.tag2_u1.id)
        assert data["name"] == name == self.tag2_u1.name

    def test_delete_tag(self):
        path = f"/tags/{self.tag1_u1.id}/"

        response = ViewsetTestsHelper.get_response(
            self.client, "DELETE", path, self.user
        )

        self.tag1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.tag1_u1.deleted_at

    def test_cannot_delete_not_owned_tag(self):
        path = f"/tags/{self.tag1_u2.id}/"

        response = ViewsetTestsHelper.get_response(
            self.client, "DELETE", path, self.user
        )

        self.tag1_u2.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not self.tag1_u2.deleted_at

    def test_get_screenshot_tags(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert self.tag1_u1 in data["results"].serializer.instance
        assert self.tag2_u1 not in data["results"].serializer.instance
        assert self.tag1_u2 not in data["results"].serializer.instance

    def test_retrieve_screenshot_tag(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.tag1_u1.id)
        assert data["name"] == self.tag1_u1.name

    def test_cannot_retrieve_tag_not_associated_to_screenshot(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag2_u1.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_screenshot_tag(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/"
        name = "Test Post Screenshot Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "POST", path, self.user, data=data
        )

        data = response.data
        tag = Tag.objects.get(name=name, owner=self.user)
        self.screenshot.refresh_from_db()

        assert response.status_code == status.HTTP_201_CREATED
        assert data["id"] == str(tag.id)
        assert data["name"] == tag.name
        assert tag in self.screenshot.tags.all()

    def test_cannot_post_tag_to_not_owned_screenshot(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/"
        name = "Test Post Screenshot Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "POST", path, self.user2, data=data
        )

        tag_count = Tag.objects.filter(name=name, owner=self.user2).count()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert tag_count == 0

    def test_patch_screenshot_tag(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"
        name = "Test Patch Screenshot Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PATCH", path, self.user, data=data
        )

        data = response.data
        self.tag1_u1.refresh_from_db()
        self.screenshot.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.tag1_u1.id)
        assert data["name"] == self.tag1_u1.name
        assert self.tag1_u1 in self.screenshot.tags.all()

    def test_cannot_patch_tag_to_not_owned_screenshot(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"
        name = "Test Patch Screenshot Tag"
        original_name = self.tag1_u1.name
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PATCH", path, self.user2, data=data
        )

        self.tag1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.tag1_u1.name == original_name

    def test_put_screenshot_tag(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"
        name = "Test Put Screenshot Tag"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PUT", path, self.user, data=data
        )

        data = response.data
        self.tag1_u1.refresh_from_db()
        self.screenshot.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.tag1_u1.id)
        assert data["name"] == self.tag1_u1.name
        assert self.tag1_u1 in self.screenshot.tags.all()

    def test_cannot_put_tag_to_not_owned_screenshot(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"
        name = "Test Put Screenshot Tag"
        original_name = self.tag1_u1.name
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PUT", path, self.user2, data=data
        )

        self.tag1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.tag1_u1.name == original_name

    def test_remove_screenshot_tag(self):
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"

        response = ViewsetTestsHelper.get_response(
            self.client, "DELETE", path, self.user
        )

        self.tag1_u1.refresh_from_db()
        self.screenshot.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not self.tag1_u1.deleted_at
        assert self.tag1_u1 not in self.screenshot.tags.all()

    def test_cannot_remove_not_owned_tag_from_screenshot(self):
        path = f"/screenshots/{self.screenshot.id}/tags/{self.tag1_u1.id}/"

        response = ViewsetTestsHelper.get_response(
            self.client, "DELETE", path, self.user2
        )

        self.tag1_u1.refresh_from_db()
        self.screenshot.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not self.tag1_u1.deleted_at
        assert self.tag1_u1 in self.screenshot.tags.all()
