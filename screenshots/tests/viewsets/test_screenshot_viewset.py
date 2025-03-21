import tempfile

import pytest
from PIL import Image
from rest_framework import status
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

from rest_framework.test import APIClient

from screenshots.models.screenshot import Screenshot
from screenshots.tests.factories.screenshot_factory import ScreenshotFactory
from screenshots.tests.factories.tag_factory import TagFactory
from screenshots.tests.factories.user_data_factory import UserDataFactory
from screenshots.tests.factories.user_factory import UserFactory
from screenshots.tests.viewsets.viewset_tests_helper import ViewsetTestsHelper


@pytest.mark.django_db
class TestScreenshotViewset:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        UserDataFactory(owner=self.user)
        self.user2 = UserFactory(username="user2", email="email2@toto.fr")
        UserDataFactory(owner=self.user2)
        self.tag1_u1 = TagFactory(name="Tag1, User 1", owner=self.user)
        self.screenshot1_u1 = ScreenshotFactory(owner=self.user)
        self.screenshot2_u1 = ScreenshotFactory(owner=self.user)
        self.screenshot1_u1.tags.add(self.tag1_u1)
        self.screenshot1_u2 = ScreenshotFactory(owner=self.user2)

    def test_get_all_screenshots(self):
        self.setup_method()
        path = "/screenshots/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert self.screenshot1_u1 in data["results"].serializer.instance
        assert self.screenshot2_u1 in data["results"].serializer.instance
        assert self.screenshot1_u2 not in data["results"].serializer.instance

    def test_retrieve_screenshot(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.screenshot1_u1.id)
        assert data["name"] == self.screenshot1_u1.name

    def test_cannot_retrieve_not_owned_screenshot(self):
        self.setup_method()
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        response = ViewsetTestsHelper.get_response(self.client, "GET", path, self.user2)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_screenshot(self):
        self.setup_method()
        path = "/screenshots/"

        name = "Test Screenshot"
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {"name": name, "file": tmp_file}

        screenshot_count_before = Screenshot.objects.filter(owner=self.user).count()

        response = ViewsetTestsHelper.get_response(
            self.client,
            "POST",
            path,
            self.user,
            data=encode_multipart(data=data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        data = response.data

        screenshot = Screenshot.objects.get(name=name, owner=self.user)
        screenshot_count_after = Screenshot.objects.filter(owner=self.user).count()

        assert response.status_code == status.HTTP_201_CREATED
        assert data["id"] == str(screenshot.id)
        assert data["name"] == screenshot.name
        assert data["image_url"] == screenshot.image_url
        assert screenshot_count_after == screenshot_count_before + 1

    def test_patch_screenshot(self):
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        name = "Test Patch Screenshot"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PATCH", path, self.user, data=data
        )

        data = response.data
        self.screenshot1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == str(self.screenshot1_u1.id)
        assert data["name"] == name == self.screenshot1_u1.name

    def test_cant_patch_not_owned_screenshot(self):
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        name = "Test Patch Screenshot"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PATCH", path, self.user2, data=data
        )

        self.screenshot1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_screenshot(self):
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        original_modified_at = self.screenshot1_u1.modified_at
        name = "Test Put Screenshot"
        data = {"name": name}

        response = ViewsetTestsHelper.get_response(
            self.client, "PUT", path, self.user, data=data
        )

        self.screenshot1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.screenshot1_u1.modified_at == original_modified_at

    def test_delete_screenshot(self):
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        response = ViewsetTestsHelper.get_response(
            self.client, "DELETE", path, self.user
        )

        self.screenshot1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.screenshot1_u1.deleted_at

    def test_cannot_delete_not_owned_screenshot(self):
        path = f"/screenshots/{self.screenshot1_u1.id}/"

        response = ViewsetTestsHelper.get_response(
            self.client, "DELETE", path, self.user2
        )

        self.screenshot1_u1.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not self.screenshot1_u1.deleted_at
