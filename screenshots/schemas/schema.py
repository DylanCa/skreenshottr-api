import graphene

from .user import UserQuery, Mutation as UserMutation
from .screenshot import ScreenshotQuery, Mutation as ScreenshotMutation


class Query(UserQuery,
            ScreenshotQuery,
            graphene.ObjectType):
    pass


class Mutation(UserMutation,
               ScreenshotMutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
