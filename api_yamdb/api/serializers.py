from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email',
            'role', 'bio'
            'first_name', 'last_name',
        )


class UserSerializerReadOnly(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email',
            'role', 'bio'
            'first_name', 'last_name',
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError(
                message='Использовать имя "me" в качестве username запрещено!'
            )
        return data
