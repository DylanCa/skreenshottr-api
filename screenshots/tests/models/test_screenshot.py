import pytest

from screenshots.tests.factories.screenshot_factory import ScreenshotFactory
from screenshots.tests.factories.tag_factory import TagFactory
from screenshots.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestScreenshot:
    def test_fields(self):
        screenshot = ScreenshotFactory()

        assert screenshot.name == "Screenshot"
        assert screenshot.image_url == "http://test.com"
        assert screenshot.__str__() == screenshot.name
        assert screenshot.owner

    def test_screenshot_with_owner(self):
        user = UserFactory()
        screenshot = ScreenshotFactory(owner=user)

        assert screenshot.owner == user

    def test_screenshot_with_tag(self):
        tag = TagFactory()
        screenshot = ScreenshotFactory()
        screenshot.tags.add(tag)

        assert tag in screenshot.tags.all()
