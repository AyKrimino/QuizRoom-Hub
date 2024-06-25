from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from classroom.permissions import IsClassroomOwner, IsClassroomMember
from quiz.models import Question, Quiz
from quiz.serializers import QuestionSerializer


class QuestionCreateAPIView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]


class QuestionListAPIView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        quiz_id = self.request.GET.get("quiz_id")

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404

        return Question.objects.filter(quiz=quiz)


class QuestionRetrieveUpdateDestroyAPIView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, question_id):
        try:
            obj = Question.objects.get(id=question_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, quiz_id, question_id, *args, **kwargs):
        self.check_permissions(request)
        question = self.get_object(question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, quiz_id, question_id, *args, **kwargs):
        self.check_permissions(request)
        question = self.get_object(question_id)
        serializer = QuestionSerializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, quiz_id, question_id, *args, **kwargs):
        self.check_permissions(request)
        question = self.get_object(question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
