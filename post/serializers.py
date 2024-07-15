from rest_framework import serializers

from authuser.serializers import UserSerializer
from classroom.serializers import ClassroomSerializer
from post.models import CoursePost, Comment


class CoursePostSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=True, required=False)

    class Meta:
        model = CoursePost
        fields = ("classroom", "id", "title", "content", "created_at", "last_updated",)
        read_only_fields = ("id", "created_at", "last_updated",)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    post = CoursePostSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ("user", "user", "id", "content", "created_at", "updated_at",)
        read_only_fields = ("id", "created_at", "updated_at",)
