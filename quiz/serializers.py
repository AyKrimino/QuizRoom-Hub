from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

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


class StudentAnswerSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    answer_id = serializers.UUIDField()

    def validate(self, data):
        try:
            question = Question.objects.get(id=data["question_id"])
            answer = Answer.objects.get(id=data["answer_id"], question=question)
        except Question.DoesNotExist:
            raise serializers.ValidationError(_("Invalid question_id"))
        except Answer.DoesNotExist:
            raise serializers.ValidationError(_("Invalid answer_id"))

        data["question"] = question
        data["answer"] = answer

        return data


class StudentQuizSerializer(serializers.ModelSerializer):
    student_answers = StudentAnswerSerializer(many=True)
    quiz = QuizSerializer(read_only=True)
    student = StudentProfileSerializerForClassroom(read_only=True)

    class Meta:
        model = StudentQuiz
        fields = ("student", "quiz", "mark", "answered_at", "student_answers",)
        read_only_fields = ("mark", "answered_at",)

    def create(self, validated_data):
        student_answers_data = validated_data.pop("student_answers")
        student = validated_data["student"]
        quiz = validated_data["quiz"]

        total_questions = quiz.questions.count()
        correct_answers = 0

        for answer_data in student_answers_data:
            if answer_data.is_valid:
                correct_answers += 1

        mark = (correct_answers / total_questions) * 100

        student_quiz = StudentQuiz.objects.create(
            student=student,
            quiz=quiz,
            mark=mark,
        )

        return student_quiz
