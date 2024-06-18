from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import TeacherProfile

User = get_user_model()


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_is_teacher = serializers.BooleanField(source="user.is_teacher", read_only=True)
    user_is_active = serializers.BooleanField(source="user.is_active", read_only=True)
    user_date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    user_last_login = serializers.DateTimeField(source="user.last_login", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", allow_blank=True, required=False)
    user_last_name = serializers.CharField(source="user.last_name", allow_blank=True, required=False)

    class Meta:
        model = TeacherProfile
        fields = ("user_id", "user_email", "user_first_name", "user_last_name", "user_is_teacher", "user_is_active",
                  "user_date_joined", "user_last_login", "id", "bio", "date_of_birth", "years_of_experience",
                  "profile_picture",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }

    def validate_user_first_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Not a valid string.")
        return value

    def validate_user_last_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Not a valid string.")
        return value

    def is_valid(self, raise_exception=False):
        self.invalid_fields = []
        for field in self.initial_data:
            if field not in self.fields:
                self.invalid_fields.append(field)

        if self.invalid_fields:
            if raise_exception:
                raise serializers.ValidationError({"invalid_fields": self.invalid_fields})
            return False

        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop("user", None)

        # Update nested User fields if present
        if user_data:
            user = instance.user
            if "first_name" in user_data:
                user.first_name = user_data["first_name"]
            if "last_name" in user_data:
                user.last_name = user_data["last_name"]
            user.save()

        # Update TeacherProfile fields
        instance.bio = validated_data.get("bio", instance.bio)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        instance.years_of_experience = validated_data.get("years_of_experience", instance.years_of_experience)
        instance.save()

        return instance


class StudentProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_is_teacher = serializers.BooleanField(source="user.is_teacher", read_only=True)
    user_is_active = serializers.BooleanField(source="user.is_active", read_only=True)
    user_date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    user_last_login = serializers.DateTimeField(source="user.last_login", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", allow_blank=True, required=False)
    user_last_name = serializers.CharField(source="user.last_name", allow_blank=True, required=False)

    class Meta:
        model = TeacherProfile
        fields = ("user_id", "user_email", "user_first_name", "user_last_name", "user_is_teacher", "user_is_active",
                  "user_date_joined", "user_last_login", "id", "bio", "date_of_birth", "profile_picture")
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }

    def validate_user_first_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Not a valid string.")
        return value

    def validate_user_last_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Not a valid string.")
        return value

    def is_valid(self, raise_exception=False):
        self.invalid_fields = []
        for field in self.initial_data:
            if field not in self.fields:
                self.invalid_fields.append(field)

        if self.invalid_fields:
            if raise_exception:
                raise serializers.ValidationError({"invalid_fields": self.invalid_fields})
            return False

        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop("user", None)

        # Update nested User fields if present
        if user_data:
            user = instance.user
            if "first_name" in user_data:
                user.first_name = user_data["first_name"]
            if "last_name" in user_data:
                user.last_name = user_data["last_name"]
            user.save()

        # Update TeacherProfile fields
        instance.bio = validated_data.get("bio", instance.bio)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        instance.save()

        return instance
