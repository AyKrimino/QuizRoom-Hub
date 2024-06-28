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

        serializer = StudentAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentQuizCreateAPIView(CreateAPIView):
    queryset = StudentQuiz.objects.all()
    serializer_class = StudentQuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember, IsStudent]


class StudentQuizListAPIView(ListAPIView):
    serializer_class = StudentQuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        user = self.request.user
        quiz_id = self.request.GET.get("quiz_id")

        if hasattr(user, "student_profile"):
            return StudentQuiz.objects.filter(student=user.student_profile)
        else:  # user is a teacher
            try:
                quiz = Quiz.objects.get(id=quiz_id)
            except Quiz.DoesNotExist:
                raise ValidationError(_("Quiz does not exist."))

            return StudentQuiz.objects.filter(quiz__classroom=quiz.classroom)
