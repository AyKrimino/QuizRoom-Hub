from rest_framework import serializers

from .models import Quiz, Question, Answer, StudentQuiz
from classroom.serializers import ClassroomSerializer, StudentProfileSerializerForClassroom


class QuizSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ("id", "title", "content", "created_at", "last_updated", "classroom",)
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "last_updated": {"read_only": True},
        }


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ("id", "description", "quiz",)
        extra_kwargs = {
            "id": {"read_only": True},
        }


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "description", "is_valid", "question",)
        extra_kwargs = {
            "id": {"read_only": True},
        }


class StudentQuizSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializerForClassroom(read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = StudentQuiz
        fields = ("id", "student", "quiz", "mark", "answered_at",)
        extra_kwargs = {
            "id": {"read_only": True},
            "mark": {"read_only": True},
            "answered_at": {"read_only": True},
        }
