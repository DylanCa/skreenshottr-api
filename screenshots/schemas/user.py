import graphene
from graphql_jwt.decorators import login_required

from screenshots.models import User
from screenshots.types import UserType


class UserQuery(graphene.ObjectType):
    my_user_data = graphene.Field(UserType)

    @login_required
    def resolve_my_user_data(self, info):
        return info.context.user


class Register(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        password = kwargs.pop('password')
        user = User.objects.create(**kwargs)
        user.set_password(password)
        user.save()

        return Register(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        email = graphene.String(required=False)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = User.objects.get(id=kwargs.get('id'))
        user.username = kwargs.get('username') or user.username
        user.first_name = kwargs.get('first_name') or user.first_name
        user.last_name = kwargs.get('last_name') or user.last_name
        user.email = kwargs.get('email') or user.email

        user.save()

        return UpdateUser(user=user)


class UserMutation(graphene.ObjectType):
    update_user = UpdateUser.Field()
    create_user = Register.Field()
