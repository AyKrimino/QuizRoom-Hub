from rest_framework import serializers

from .models import TeacherProfile, StudentProfile
from authuser.serializers import UserSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ("id", "user", "bio", "date_of_birth", "profile_picture", "years_of_experience",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "bio", "date_of_birth", "profile_picture",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }
