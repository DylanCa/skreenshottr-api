from rest_framework import serializers


class BaseModelSerializerMixin(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    def validate_owner(self, attrs):
        user = self.get_owner()
        attrs["owner"] = user

        return attrs

    def get_owner(self):
        return self.context["request"].user

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return self.validate_owner(attrs)


class UniqueObjectSerializerMixin:
    def create(self, validated_data):
        instance, _ = self.Meta.model.objects.get_or_create(**validated_data)
        return instance
