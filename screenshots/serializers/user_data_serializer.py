from rest_framework import serializers

from screenshots.models.user_data import UserData


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['screenshot_total_count',
                  'screenshot_total_size']
