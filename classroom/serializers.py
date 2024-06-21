from rest_framework import serializers

from account.models import StudentProfile, TeacherProfile
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
    classroom_id = serializers.UUIDField(source="classroom.id", write_only=True)

    class Meta:
        model = StudentClassroom
        fields = ("id", "student", "classroom", "date_joined", "classroom_id")
        extra_kwargs = {
            "id": {"read_only": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        classroom_data = validated_data.pop('classroom', None)
        classroom_id = classroom_data['id']
        classroom = Classroom.objects.get(id=classroom_id)

        user = self.context['request'].user
        if TeacherProfile.objects.filter(user=user).exists():
            student_id = self.context['request'].data.get('student_id')
            if not student_id:
                raise serializers.ValidationError("student_id is required for teachers.")
            student = StudentProfile.objects.get(id=student_id)
        else:
            student = StudentProfile.objects.get(user=user)

        if StudentClassroom.objects.filter(student=student, classroom=classroom).exists():
            raise serializers.ValidationError("This student is already enrolled in the specified classroom.")

        return StudentClassroom.objects.create(student=student, classroom=classroom, **validated_data)
