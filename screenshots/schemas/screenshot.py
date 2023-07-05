import graphene
from graphene_django import DjangoObjectType

from screenshots.models import Screenshot


class ScreenshotType(DjangoObjectType):
    class Meta:
        model = Screenshot
        fields = ("id", "file_url", "owner")


class ScreenshotQuery(graphene.ObjectType):

    all_screenshots = graphene.List(ScreenshotType)

    def resolve_all_screenshots(self, root):
        return Screenshot.objects.all()


class ScreenshotMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        file_url = graphene.String(required=True)

    screenshot = graphene.Field(ScreenshotType)

    @classmethod
    def mutate(cls, root, info, id, file_url):
        screenshot = Screenshot.objects.get(id=id)
        screenshot.file_url = file_url

        screenshot.save()

        return ScreenshotMutation(screenshot=screenshot)


class Mutation(graphene.ObjectType):
    update_screenshot = ScreenshotMutation.Field()
