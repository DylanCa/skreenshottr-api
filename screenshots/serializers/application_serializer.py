from screenshots.models.application import Application
from screenshots.serializers.mixins import BaseModelSerializerMixin, UniqueObjectSerializerMixin


class ApplicationSerializer(BaseModelSerializerMixin,
                            UniqueObjectSerializerMixin):
    class Meta:
        model = Application
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {"validators": [], "allow_blank": True},
        }
