from rest_framework import serializers

from screenshots.models import User
from screenshots.serializers.user_data_serializer import UserDataSerializer


class UserSerializer(serializers.ModelSerializer):
    user_data = UserDataSerializer(source='data', read_only=True)

    class Meta:
        model = User
        fields = ['email',
                  'user_data',
                  'date_joined']
