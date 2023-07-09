from graphene_django import DjangoObjectType

from screenshots.models import Tag


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name", )
