from screenshots.models.tag import Tag
from screenshots.serializers.mixins import BaseModelSerializerMixin, UniqueObjectSerializerMixin


class TagSerializer(BaseModelSerializerMixin,
                    UniqueObjectSerializerMixin):
    parent_lookup_kwargs = {
        "screenshot_pk": "screenshot__pk",
    }

    class Meta:
        model = Tag
        fields = ["id", "name"]
