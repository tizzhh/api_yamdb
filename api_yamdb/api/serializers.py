from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from custom_user.models import CustomUser


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField()

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = get_object_or_404(CustomUser, username=username)
        if confirmation_code != user.confirmation_code:
            raise BadRequest('Incorrect confirmation code')
        return attrs


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise BadRequest('Username cannot be "me"')
        return value


class UserSerializerAuth(BaseUserSerializer):
    ...


class UserSerializerAdmin(BaseUserSerializer):
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
