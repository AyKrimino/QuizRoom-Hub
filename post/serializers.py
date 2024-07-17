from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from authuser.serializers import UserSerializer
from classroom.serializers import ClassroomSerializer
from post.models import CoursePost, Comment
from classroom.models import Classroom


class CoursePostSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=True, required=False)

    class Meta:
        model = CoursePost
        fields = ("classroom", "id", "title", "content", "created_at", "last_updated",)
        read_only_fields = ("id", "created_at", "last_updated",)

    def validate(self, data):
        classroom_id = self.context.get("classroom_id", None)
        if classroom_id is None:
            raise serializers.ValidationError(_("classroom_id param is required."))
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise serializers.ValidationError(_("Classroom does not exist."))
        data["classroom"] = classroom
        return data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    post = CoursePostSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ("user", "post", "id", "content", "created_at", "updated_at",)
        read_only_fields = ("id", "created_at", "updated_at",)

    def validate(self, data):
        post_id = self.context.get("post_id", None)
        if post_id is None:
            raise serializers.ValidationError(_("post_id param is required."))
        try:
            post = CoursePost.objects.get(id=post_id)
        except CoursePost.DoesNotExist:
            raise serializers.ValidationError(_("Post does not exist."))
        data["post"] = post
        data["user"] = self.context["user"]
        return data
