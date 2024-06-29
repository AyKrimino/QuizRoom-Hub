from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from account.models import TeacherProfile
from classroom.models import Classroom
from classroom.permissions import IsClassroomOwner, IsTeacher, IsClassroomMember
from quiz.models import Quiz
from quiz.serializers import QuizSerializer


class QuizCreateAPIView(CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def perform_create(self, serializer):
        classroom_id = serializer.validated_data["classroom_id"]

        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise ValidationError(_("Classroom does not exist"))

        self.check_object_permissions(self.request, classroom)

        serializer.save()


class QuizListAPIView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        teacher = TeacherProfile.objects.get(user=user)
        return Quiz.objects.filter(classroom__in=teacher.classrooms.all())


class QuizRetrieveUpdateDestroyAPIView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            classroom = quiz.classroom
            self.check_object_permissions(self.request, classroom)
            return quiz
        except Quiz.DoesNotExist:
            raise Http404

    def get(self, request, quiz_id, *args, **kwargs):
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, quiz_id, *args, **kwargs):
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        serializer = QuizSerializer(quiz, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, quiz_id, *args, **kwargs):
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
