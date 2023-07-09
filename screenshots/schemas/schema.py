import graphene

from .authentication import AuthMutation
from .user import UserQuery, UserMutation
from .screenshot import ScreenshotQuery, ScreenshotMutation
from .tag import TagQuery, TagMutation


class Query(UserQuery,
            ScreenshotQuery,
            TagQuery,
            graphene.ObjectType):
    pass


class Mutation(UserMutation,
               ScreenshotMutation,
               TagMutation,
               AuthMutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
