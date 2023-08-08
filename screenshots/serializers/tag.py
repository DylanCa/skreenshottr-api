from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from screenshots.models import Tag, Screenshot
from screenshots.serializers.mixins import BaseModelSerializerMixin


class TagSerializer(BaseModelSerializerMixin):
    parent_lookup_kwargs = {
        'screenshot_pk': 'screenshot__pk',
    }

    class Meta:
        model = Tag
        fields = ['id', 'name']
