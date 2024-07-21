from decimal import Decimal

from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from classroom.models import Classroom
from classroom.serializers import StudentProfileSerializerForClassroom
from quiz.models import Quiz, Question, Answer, StudentAnswer, StudentQuiz


class QuizSerializer(serializers.ModelSerializer):
    classroom_id = serializers.UUIDField(required=False)

    class Meta:
        model = Quiz
        fields = ("id", "title", "content", "created_at", "last_updated", "classroom_id",)
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "last_updated": {"read_only": True},
        }

    def validate(self, data):
        classroom_id = data.get("classroom_id", None)
        if classroom_id is None:
            raise serializers.ValidationError(_("classroom_id is required."))

        title = data.get("title", None)
        if title is None:
            raise serializers.ValidationError(_("title is required."))

        return data

    def create(self, validated_data):
        classroom_id = validated_data.get("classroom_id")
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise serializers.ValidationError(_("Classroom does not exist"))

        title = validated_data.get("title")
        content = validated_data.get("content", None)

        quiz = Quiz.objects.create(
            title=title,
            content=content,
            classroom=classroom,
        )

        return quiz


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "description", "quiz",)
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate(self, data):
        quiz_id = self.context.get('quiz_id', None)
        if quiz_id is None:
            raise serializers.ValidationError(_("quiz_id param is required."))

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError(_("Quiz does not exist"))

        data["quiz"] = quiz
        return data

    def create(self, validated_data):
        description = validated_data["description"]
        quiz = validated_data["quiz"]
        question = Question.objects.create(description=description, quiz=quiz)
        return question


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True, required=False)

    class Meta:
        model = Answer
        fields = ("id", "description", "is_valid", "question",)
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def to_internal_value(self, data):
        if "is_valid" in data and not isinstance(data["is_valid"], bool):
            raise serializers.ValidationError({"is_valid": _("Not a valid boolean.")})
        return super().to_internal_value(data)

    def validate(self, data):
        question_id = self.context.get('question_id', None)
        if question_id is None:
            raise serializers.ValidationError(_("question_id param is required."))

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError(_("Question does not exist"))

        data["question"] = question
        return data

    def create(self, validated_data):
        description = validated_data["description"]
        is_valid = validated_data["is_valid"]
        question = validated_data["question"]
        answer = Answer.objects.create(description=description, is_valid=is_valid, question=question)
        return answer


class StudentAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.UUIDField(write_only=True)
    answer_id = serializers.UUIDField(write_only=True)
    student = StudentProfileSerializerForClassroom(read_only=True, required=False)
    answer = AnswerSerializer(read_only=True, required=False)
    question = QuestionSerializer(read_only=True, required=False)

    class Meta:
        model = StudentAnswer
        fields = ("student", "answer", "question", "question_id", "answer_id",)

    def validate(self, data):
        quiz_id = self.context.get("quiz_id", None)
        if quiz_id is None:
            raise serializers.ValidationError(_("quiz_id param is required."))

        student = self.context.get("student", None)
        if student is None:
            raise serializers.ValidationError(_("student not found."))

        try:
            quiz = Quiz.objects.get(id=quiz_id)
            question = Question.objects.get(id=data["question_id"])
            answer = Answer.objects.get(id=data["answer_id"], question=question)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError(_("Quiz does not exist."))
        except Question.DoesNotExist:
            raise serializers.ValidationError(_("Question does not exist."))
        except Answer.DoesNotExist:
            raise serializers.ValidationError(_("Answer does not exist."))

        del data["question_id"]
        del data["answer_id"]
        data["quiz"] = quiz
        data["question"] = question
        data["answer"] = answer
        data["student"] = student

        return data

    def create(self, validated_data):
        student = validated_data["student"]
        answer = validated_data["answer"]
        try:
            student_answer = StudentAnswer.objects.create(
                student=student,
                answer=answer,
            )
        except IntegrityError:
            raise serializers.ValidationError(_("Student cannot answer the same question again."))

        return student_answer


class StudentQuizSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True, required=False)
    student = StudentProfileSerializerForClassroom(read_only=True, required=False)

    class Meta:
        model = StudentQuiz
        fields = ("student", "quiz", "mark", "answered_at",)
        read_only_fields = ("mark", "answered_at",)

    def validate(self, data):
        quiz_id = self.context.get("quiz_id", None)
        if quiz_id is None:
            raise serializers.ValidationError(_("quiz_id param is required."))

        student = self.context.get("student", None)
        if student is None:
            raise serializers.ValidationError(_("student not found."))

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError(_("Quiz does not exist."))

        data["student_answers"] = student.student_answers.filter(answer__question__quiz=quiz)
        data["quiz"] = quiz
        data["student"] = student
        return data

    def create(self, validated_data):
        student_answers_data = validated_data.pop("student_answers")
        student = validated_data["student"]
        quiz = validated_data["quiz"]

        total_questions = quiz.questions.count()
        correct_answers = 0

        for answer_data in student_answers_data:
            if answer_data.answer.is_valid:
                correct_answers += 1

        if total_questions == 0:
            raise serializers.ValidationError(_("Quiz has no questions."))

        mark = Decimal((correct_answers / total_questions) * 100).quantize(Decimal('0.00'))

        student_quiz = StudentQuiz.objects.create(
            student=student,
            quiz=quiz,
            mark=mark,
        )

        return student_quiz
