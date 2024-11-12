from rest_framework import serializers
from authentication.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "username",
            "address",
            "password",
            'is_staff',
            'is_superuser',
            "phone",
            "date_of_birth",
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "username",
            "address",
            "phone",
            "date_of_birth",
        ]
        read_only_fields = ['id']
