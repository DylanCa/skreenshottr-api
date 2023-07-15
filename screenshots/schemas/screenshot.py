import graphene
import logging

from django.core.files.storage import default_storage
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required

from screenshots.lib import ImageHelper
from screenshots.models import Screenshot, Tag
from screenshots.scalars import URL
from screenshots.types import ScreenshotType, TagType

from screenshots.schemas.schema_utils import MutationBase, StatusCode, MutationMethods

logger = logging.getLogger(__name__)


class ScreenshotQuery(graphene.ObjectType):
    my_screenshots = graphene.List(ScreenshotType)
    screenshot = graphene.Field(ScreenshotType, id=graphene.ID())

    @login_required
    def resolve_my_screenshots(self, info):
        return Screenshot.objects.filter(owner=info.context.user, deleted_at=None)

    @login_required
    def resolve_screenshot(self, info, id):
        return Screenshot.objects.get(id=id, owner=info.context.user, deleted_at=None)


class UploadScreenshot(graphene.Mutation, MutationBase):
    class Arguments:
        file = Upload(required=True)

    screenshot = graphene.Field(ScreenshotType)

    @classmethod
    @login_required
    def mutate(cls, root, info, file):
        try:
            if ImageHelper.verify_image_from_file(file):

                filepath = ImageHelper.save_image_in_storage(file)
                screenshot = Screenshot.objects.create(
                    owner=info.context.user,
                    file_url=filepath
                )
                screenshot.save()

                message = f"Successfully created Screenshot #{screenshot.id}."
                status_code = StatusCode.success
            else:
                screenshot = None
                message = f"Uploaded file is not an image."
                status_code = StatusCode.error
        except Exception as e:
            logger.exception(e)
            screenshot = None
            message = f"Error while creating Screenshot."
            status_code = StatusCode.error

        return UploadScreenshot(screenshot=screenshot,
                                 message=message,
                                 status_code=status_code)


class UpdateScreenshot(graphene.Mutation, MutationBase):
    class Arguments:
        id = graphene.ID(required=True)

        file_url = URL(required=True)

    screenshot = graphene.Field(ScreenshotType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, file_url):
        screenshot, message, status_code = MutationMethods.update_object("Screenshot", id, info.context.user, False, file_url=file_url)

        return UpdateScreenshot(screenshot=screenshot,
                                message=message,
                                status_code=status_code)


class DeleteScreenshot(graphene.Mutation, MutationBase):
    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        message, status_code = MutationMethods.delete_object("Screenshot", id, info.context.user)

        return DeleteScreenshot(message=message,
                                status_code=status_code)


def get_screenshot_and_tags(user,
                            screenshot_id,
                            tag_id,
                            tag_name):

    screenshot = Screenshot.objects.get(
        id=screenshot_id,
        owner=user,
        deleted_at=None
    )

    tags_ids = []
    if tag_id:
        tag = Tag.objects.get(id=tag_id, owner=user, deleted_at=None)
        if tag:
            tags_ids.append(tag.id)
    if tag_name:
        tag, _ = Tag.objects.get_or_create(name=tag_name, owner=user, deleted_at=None)
        tags_ids.append(tag.id)

    return screenshot, tags_ids


class AddTagToScreenshot(graphene.Mutation, MutationBase):
    class Arguments:
        screenshot_id = graphene.ID(required=True)

        tag_id = graphene.ID(required=False)
        tag_name = graphene.String(required=False)

    screenshot = graphene.Field(ScreenshotType)

    @classmethod
    @login_required
    def mutate(cls, root, info, screenshot_id, tag_id=None, tag_name=None):
        try:
            screenshot, tags_ids = get_screenshot_and_tags(info.context.user, screenshot_id, tag_id, tag_name)

            if screenshot:

                screenshot.tags.add(*tags_ids)
                screenshot.save()

                message = f"Successfully added tags to Screenshot #{screenshot.id}."
                status_code = StatusCode.success

            else:
                message = f"Screenshot #{screenshot.id} not found."
                status_code = StatusCode.not_found

        except Exception as e:
            logger.exception(e)
            screenshot = None
            message = f"Error while adding tags to Screenshot, please double-check sent data."
            status_code = StatusCode.error

        return UpdateScreenshot(screenshot=screenshot,
                                message=message,
                                status_code=status_code)


class RemoveTagFromScreenshot(graphene.Mutation, MutationBase):
    class Arguments:
        screenshot_id = graphene.ID(required=True)

        tag_id = graphene.ID(required=False)
        tag_name = graphene.String(required=False)

    screenshot = graphene.Field(ScreenshotType)

    @classmethod
    @login_required
    def mutate(cls, root, info, screenshot_id, tag_id=None, tag_name=None):
        try:
            screenshot, tags_ids = get_screenshot_and_tags(info.context.user, screenshot_id, tag_id, tag_name)

            if screenshot:

                screenshot.tags.remove(*tags_ids)
                screenshot.save()

                message = f"Successfully removed tags from Screenshot #{screenshot.id}."
                status_code = StatusCode.success

            else:
                message = f"Screenshot #{screenshot.id} not found."
                status_code = StatusCode.not_found

        except Exception as e:
            logger.exception(e)
            screenshot = None
            message = f"Error while removing tags from Screenshot, please double-check sent data."
            status_code = StatusCode.error

        return RemoveTagFromScreenshot(screenshot=screenshot,
                                message=message,
                                status_code=status_code)


class ScreenshotMutation(graphene.ObjectType):
    upload_screenshot = UploadScreenshot.Field()
    update_screenshot = UpdateScreenshot.Field()
    delete_screenshot = DeleteScreenshot.Field()
    add_tags_to_screenshot = AddTagToScreenshot.Field()
    remove_tags_to_screenshot = RemoveTagFromScreenshot.Field()
