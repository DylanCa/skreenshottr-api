from rest_framework import serializers


class BaseModelSerializerMixin(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    def validate_owner(self, attrs):
        user = self.context["request"].user
        attrs["owner"] = user

        return attrs

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return self.validate_owner(attrs)
