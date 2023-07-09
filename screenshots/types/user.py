import graphene
from graphene_django import DjangoObjectType

from screenshots.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
