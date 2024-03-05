from django.core.exceptions import BadRequest
from rest_framework import serializers

from custom_user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise BadRequest('Username cannot be "me"')
        return value
