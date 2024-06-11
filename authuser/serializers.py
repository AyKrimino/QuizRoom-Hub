from django.conf import settings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("id", "email", "first_name", "last_name", "is_teacher", "password")
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {
                "write_only": True,
                "required": True,
            },
        }
