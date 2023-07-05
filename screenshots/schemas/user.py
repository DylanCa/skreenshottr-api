import graphene
from graphene_django import DjangoObjectType

from screenshots.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "name", "surname", "email")


class UserQuery(graphene.ObjectType):
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))

    def resolve_user_by_username(self, root, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class UserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String(required=False)
        name = graphene.String(required=False)
        surname = graphene.String(required=False)
        email = graphene.String(required=False)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, id, username=None, name=None, surname=None, email=None):
        user = User.objects.get(id=id)
        user.username = username or user.username
        user.name = name or user.name
        user.surname = surname or user.surname
        user.email = email or user.email

        user.save()

        return UserMutation(user=user)


class Mutation(graphene.ObjectType):
    update_user = UserMutation.Field()
