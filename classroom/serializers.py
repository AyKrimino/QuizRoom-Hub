from rest_framework import serializers

from account.serializers import TeacherProfileSerializer, StudentProfileSerializer
from .models import Classroom, StudentClassroom

# removing profile_picture field from TeacherProfileSerializer and StudentProfileSerializer
TeacherProfileSerializer.Meta.fields = TeacherProfileSerializer.Meta.fields[:-1]
StudentProfileSerializer.Meta.fields = StudentProfileSerializer.Meta.fields[:-1]


class ClassroomSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = Classroom
        fields = ("id", "name", "teacher", "created_at",)
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }


class StudentClassroomSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = StudentClassroom
        fields = ("id", "student", "classroom", "date_joined",)
        extra_kwargs = {
            "id": {"read_only": True},
            "date_joined": {"read_only": True},
        }
