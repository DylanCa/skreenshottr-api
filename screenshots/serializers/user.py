from rest_framework import serializers

from screenshots.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
