import graphene
from graphene_django import DjangoObjectType

from screenshots.models import Screenshot
from screenshots.types import ScreenshotType


class ScreenshotQuery(graphene.ObjectType):

    all_screenshots = graphene.List(ScreenshotType)

    def resolve_all_screenshots(self, root):
        return Screenshot.objects.all()


class UpdateScreenshot(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        file_url = graphene.String(required=True)

    screenshot = graphene.Field(ScreenshotType)

    @classmethod
    def mutate(cls, root, info, id, file_url):
        screenshot = Screenshot.objects.get(id=id)
        screenshot.file_url = file_url

        screenshot.save()

        return UpdateScreenshot(screenshot=screenshot)


class ScreenshotMutation(graphene.ObjectType):
    update_screenshot = UpdateScreenshot.Field()
