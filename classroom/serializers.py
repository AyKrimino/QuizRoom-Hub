from rest_framework import serializers

from account.models import StudentProfile, TeacherProfile
from account.serializers import TeacherProfileSerializer, StudentProfileSerializer
from .models import Classroom, StudentClassroom


class TeacherProfileSerializerForClassroom(TeacherProfileSerializer):
    class Meta(TeacherProfileSerializer.Meta):
        fields = [field for field in TeacherProfileSerializer.Meta.fields if field != 'profile_picture']


class StudentProfileSerializerForClassroom(StudentProfileSerializer):
    class Meta(StudentProfileSerializer.Meta):
        fields = [field for field in StudentProfileSerializer.Meta.fields if field != 'profile_picture']


class ClassroomSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializerForClassroom(read_only=True)

    class Meta:
        model = Classroom
        fields = ("id", "name", "teacher", "created_at",)
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

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


class StudentClassroomSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializerForClassroom(read_only=True)
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
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise serializers.ValidationError("Classroom matching query does not exist.")

        user = self.context['request'].user
        if TeacherProfile.objects.filter(user=user).exists():
            student_id = self.context['request'].data.get('student_id')
            if not student_id:
                raise serializers.ValidationError("student_id is required for teachers.")
            try:
                student = StudentProfile.objects.get(id=student_id)
            except StudentProfile.DoesNotExist:
                raise serializers.ValidationError("StudentProfile matching query does not exist.")
        else:
            student = StudentProfile.objects.get(user=user)

        if StudentClassroom.objects.filter(student=student, classroom=classroom).exists():
            raise serializers.ValidationError("This student is already enrolled in the specified classroom.")

        return StudentClassroom.objects.create(student=student, classroom=classroom, **validated_data)
