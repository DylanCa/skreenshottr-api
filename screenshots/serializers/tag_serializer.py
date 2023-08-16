from screenshots.models import Tag
from screenshots.serializers.mixins import BaseModelSerializerMixin


class TagSerializer(BaseModelSerializerMixin):
    parent_lookup_kwargs = {
        "screenshot_pk": "screenshot__pk",
    }

    class Meta:
        model = Tag
        fields = ["id", "name"]
