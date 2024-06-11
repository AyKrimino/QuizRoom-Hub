from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "is_teacher", "password")
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {
                "write_only": True,
                "required": True,
            },
        }
