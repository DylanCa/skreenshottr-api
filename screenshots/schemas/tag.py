import graphene
import logging
from graphql_jwt.decorators import login_required

from screenshots.models import Tag
from screenshots.types import TagType

from screenshots.schemas.schema_utils import MutationBase, StatusCode, MutationMethods

logger = logging.getLogger(__name__)


class TagQuery(graphene.ObjectType):
    my_tags = graphene.List(TagType)
    tag = graphene.Field(TagType, id=graphene.ID())

    @login_required
    def resolve_my_tags(self, info):
        return Tag.objects.filter(owner =info.context.user, deleted_at=None)

    @login_required
    def resolve_tag(self, info, id):
        return Tag.objects.get(id=id, owner=info.context.user, deleted_at=None)


class CreateTag(graphene.Mutation, MutationBase):
    class Arguments:
        name = graphene.String(required=True)

    tag = graphene.Field(TagType)

    @classmethod
    @login_required
    def mutate(cls, root, info, name):
        tag, message, status_code = MutationMethods.create_object("Tag", info.context.user, name=name)

        return CreateTag(tag=tag,
                        message=message,
                        status_code=status_code)


class UpdateTag(graphene.Mutation, MutationBase):
    class Arguments:
        id = graphene.ID(required=True)

        name = graphene.String(required=True)

    tag = graphene.Field(TagType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, name):
        tag, message, status_code = MutationMethods.update_object("Tag", id, info.context.user, False, name=name)

        return UpdateTag(tag=tag,
                        message=message,
                        status_code=status_code)


class DeleteTag(graphene.Mutation, MutationBase):
    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        message, status_code = MutationMethods.delete_object("Tag", id, info.context.user)

        return DeleteTag(message=message,
                                    status_code=status_code)


class TagMutation(graphene.ObjectType):
    create_tag = CreateTag.Field()
    update_tag = UpdateTag.Field()
    delete_tag = DeleteTag.Field()
