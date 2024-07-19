from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authuser.serializers import ErrorResponseSerializer
from classroom.permissions import IsClassroomOwner
from quiz.models import Answer, Question
from quiz.serializers import AnswerSerializer


class AnswerCreateAPIView(CreateAPIView):
    """
    API view to create a new Answer instance.

    This view handles the creation of new answers associated with a specific question.
    It requires that the user is authenticated and is the owner of the classroom to which
    the question's quiz belongs.

    Attributes:
        queryset: The queryset of Answer objects.
        serializer_class: The serializer class to handle answer creation.
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_serializer_context():
            Adds the 'question_id' from the URL kwargs to the serializer context.

        perform_create(serializer):
            Handles the actual saving of the answer. Validates the associated question and
            checks that the user has the necessary permissions.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_serializer_context(self):
        """
        Adds additional context to the serializer.

        This method adds the 'question_id' from the URL kwargs to the serializer context,
        allowing the serializer to access it during validation and saving.

        Returns:
            dict: The updated context dictionary.
        """
        context = super().get_serializer_context()
        context["question_id"] = self.kwargs.get("question_id")
        return context

    def perform_create(self, serializer):
        """
        Handles the actual saving of the answer.

        This method validates the associated question and checks that the user has
        the necessary permissions to add an answer to the question's classroom.

        Args:
            serializer (Serializer): The serializer instance containing the
            validated data.
        """
        question = serializer.validated_data["question"]
        classroom = question.quiz.classroom
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class AnswerListAPIView(ListAPIView):
    """
    API view to list Answer instances for a specific question.

    This view returns a list of answers associated with a specific question.
    The user must be authenticated and the owner of the classroom to access this view.

    Attributes:
        serializer_class: The serializer class to handle the answer listing.
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_queryset():
            Returns the queryset of answers associated with the specified question.
    """
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_queryset(self):
        """
        Returns the queryset of answers associated with the specified question.

        This method retrieves the question by its ID from the URL kwargs, checks the
        user's permissions for the classroom associated with the question's quiz,
        and then returns the queryset of answers.

        Returns:
            QuerySet: A queryset of Answer objects.

        Raises:
            Http404: If the question does not exist.
        """
        question_id = self.kwargs.get("question_id")

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise Http404

        classroom = question.quiz.classroom
        self.check_object_permissions(self.request, classroom)

        return question.answers.all()


class AnswerRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete an Answer instance.

    This view handles the retrieval, update, and deletion of a specific answer.
    The user must be authenticated and the owner of the classroom to access this view.

    Attributes:
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_object(answer_id):
            Retrieves the answer object by its ID and checks object permissions.
            Raises Http404 if the answer does not exist.

        get(request, quiz_id, question_id, answer_id, *args, **kwargs):
            Handles GET requests to retrieve the answer details.

        put(request, quiz_id, question_id, answer_id, *args, **kwargs):
            Handles PUT requests to update the answer details.

        delete(request, quiz_id, question_id, answer_id, *args, **kwargs):
            Handles DELETE requests to delete the answer.
    """
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_object(self, answer_id):
        """
        Retrieves the answer object by its ID and checks object permissions.

        Args:
            answer_id (UUID): The ID of the answer to be retrieved.

        Returns:
            Answer: The retrieved answer object.

        Raises:
            Http404: If the answer does not exist.
        """
        try:
            answer = Answer.objects.get(id=answer_id)
            classroom = answer.question.quiz.classroom
            self.check_object_permissions(self.request, classroom)
            return answer
        except Answer.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: AnswerSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, quiz_id, question_id, answer_id, *args, **kwargs):
        """
        Handles GET requests to retrieve the answer details.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to which the answer's question belongs.
            question_id (UUID): The ID of the question to which the answer belongs.
            answer_id (UUID): The ID of the answer to be retrieved.

        Returns:
            Response: The response containing the answer details.
        """
        self.check_permissions(request)
        answer = self.get_object(answer_id)
        serializer = AnswerSerializer(answer, context={"quiz_id": quiz_id, "question_id": question_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AnswerSerializer,
        responses={
            200: AnswerSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, quiz_id, question_id, answer_id, *args, **kwargs):
        """
        Handles PUT requests to update the answer details.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to which the answer's question belongs.
            question_id (UUID): The ID of the question to which the answer belongs.
            answer_id (UUID): The ID of the answer to be updated.

        Returns:
            Response: The response containing the updated answer details.
        """
        self.check_permissions(request)
        answer = self.get_object(answer_id)
        serializer = AnswerSerializer(answer, data=request.data,
                                      context={"quiz_id": quiz_id, "question_id": question_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, quiz_id, question_id, answer_id, *args, **kwargs):
        """
        Handles DELETE requests to delete the answer.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to which the answer's question belongs.
            question_id (UUID): The ID of the question to which the answer belongs.
            answer_id (UUID): The ID of the answer to be deleted.

        Returns:
            Response: The response indicating that the answer has been deleted.
        """
        self.check_permissions(request)
        answer = self.get_object(answer_id)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
