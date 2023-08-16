from django.core.exceptions import ValidationError
from rest_framework import serializers

from screenshots.models import Application
from screenshots.serializers.mixins import BaseModelSerializerMixin


class ApplicationSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Application
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {"validators": [], "allow_blank": True},
        }
