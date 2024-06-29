from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from classroom.permissions import IsClassroomMember, IsStudent
from quiz.models import StudentQuiz, Quiz
from quiz.serializers import StudentAnswerSerializer, StudentQuizSerializer


class StudentAnswerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsClassroomMember, IsStudent]

    def post(self, request, *args, **kwargs):
        self.check_permissions(request)

        quiz_id = self.kwargs.get("quiz_id")
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise ValidationError(_("Quiz does not exist"))
        classroom = quiz.classroom
        self.check_object_permissions(request, classroom)

        serializer = StudentAnswerSerializer(data=request.data,
                                             context={"quiz_id": quiz_id, "student": request.user.student_profile})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentQuizCreateAPIView(CreateAPIView):
    queryset = StudentQuiz.objects.all()
    serializer_class = StudentQuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember, IsStudent]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["student"] = self.request.user.student_profile
        context["quiz_id"] = self.kwargs.get("quiz_id")
        return context

    def perform_create(self, serializer):
        quiz_id = self.kwargs.get("quiz_id")
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise ValidationError(_("Quiz does not exist."))
        classroom = quiz.classroom

        self.check_permissions(self.request)
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class StudentQuizListAPIView(ListAPIView):
    serializer_class = StudentQuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        user = self.request.user
        quiz_id = self.kwargs.get("quiz_id")
        print(f"{quiz_id=}")
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise ValidationError(_("Quiz does not exist."))
        classroom = quiz.classroom
        self.check_object_permissions(self.request, classroom)

        if hasattr(user, "student_profile"):
            return StudentQuiz.objects.filter(student=user.student_profile)
        else:  # user is a teacher
            return StudentQuiz.objects.filter(quiz__classroom=quiz.classroom)
