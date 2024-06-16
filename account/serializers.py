from rest_framework import serializers

from .models import TeacherProfile, StudentProfile
from authuser.serializers import UserSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeacherProfile
        fields = ("user", "id", "bio", "date_of_birth", "years_of_experience", "profile_picture",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user', None)

        # Update TeacherProfile fields
        instance.bio = validated_data.get('bio', instance.bio)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.years_of_experience = validated_data.get('years_of_experience', instance.years_of_experience)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        # Update nested User fields if present
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.username)
            user.last_name = user_data.get('last_name', user.email)
            user.save()

        return instance


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = ("user", "id", "bio", "date_of_birth", "profile_picture",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user', None)

        # Update StudentProfile fields
        instance.bio = validated_data.get('bio', instance.bio)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        # Update nested User fields if present
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.username)
            user.last_name = user_data.get('last_name', user.email)
            user.save()

        return instance
