from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from classroom.permissions import IsClassroomOwner
from quiz.models import Answer, Question
from quiz.serializers import AnswerSerializer


class AnswerCreateAPIView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["question_id"] = self.kwargs.get("question_id")
        return context

    def perform_create(self, serializer):
        question = serializer.validated_data["question"]
        classroom = question.quiz.classroom
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class AnswerListAPIView(ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_queryset(self):
        question_id = self.kwargs.get("question_id")

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise Http404

        classroom = question.quiz.classroom
        self.check_object_permissions(self.request, classroom)

        return question.answers.all()


class AnswerRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_object(self, answer_id):
        try:
            answer = Answer.objects.get(id=answer_id)
            classroom = answer.question.quiz.classroom
            self.check_object_permissions(self.request, classroom)
            return answer
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, quiz_id, question_id, answer_id, *args, **kwargs):
        self.check_permissions(request)
        answer = self.get_object(answer_id)
        serializer = AnswerSerializer(answer, context={"quiz_id": quiz_id, "question_id": question_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, quiz_id, question_id, answer_id, *args, **kwargs):
        self.check_permissions(request)
        answer = self.get_object(answer_id)
        serializer = AnswerSerializer(answer, data=request.data,
                                      context={"quiz_id": quiz_id, "question_id": question_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, quiz_id, question_id, answer_id, *args, **kwargs):
        self.check_permissions(request)
        answer = self.get_object(answer_id)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
