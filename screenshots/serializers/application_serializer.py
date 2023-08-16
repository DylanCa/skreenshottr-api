
from screenshots.models import Application
from screenshots.serializers.mixins import BaseModelSerializerMixin


class ApplicationSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Application
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {"validators": [], "allow_blank": True},
        }
