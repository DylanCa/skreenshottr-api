import graphene

from .authentication import AuthMutation
from .user import UserQuery, UserMutation
from .screenshot import ScreenshotQuery, ScreenshotMutation


class Query(UserQuery,
            ScreenshotQuery,
            graphene.ObjectType):
    pass


class Mutation(UserMutation,
               ScreenshotMutation,
               AuthMutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
