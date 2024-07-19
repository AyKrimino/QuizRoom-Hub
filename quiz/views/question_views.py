from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from authuser.serializers import ErrorResponseSerializer
from classroom.permissions import IsClassroomOwner, IsClassroomMember
from quiz.models import Question, Quiz
from quiz.serializers import QuestionSerializer


class QuestionCreateAPIView(CreateAPIView):
    """
    API view to create a new Question instance.

    This view handles the creation of new questions associated with a specific quiz.
    It requires that the user is authenticated and is the owner of the classroom to which
    the quiz belongs.

    Attributes:
        queryset: The queryset of Question objects.
        serializer_class: The serializer class to handle question creation.
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_serializer_context():
            Adds the 'quiz_id' from the URL kwargs to the serializer context.

        perform_create(serializer):
            Handles the actual saving of the question. Validates the associated quiz and
            checks that the user has the necessary permissions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_serializer_context(self):
        """
        Adds additional context to the serializer.

        This method adds the 'quiz_id' from the URL kwargs to the serializer context,
        allowing the serializer to access it during validation and saving.

        Returns:
            dict: The updated context dictionary.
        """
        context = super().get_serializer_context()
        context['quiz_id'] = self.kwargs.get('quiz_id')
        return context

    def perform_create(self, serializer):
        """
        Handles the actual saving of the question.

        This method validates the associated quiz and checks that the user has
        the necessary permissions to add a question to the quiz's classroom.

        Args:
            serializer (Serializer): The serializer instance containing the
            validated data.
        """
        quiz = serializer.validated_data["quiz"]
        self.check_object_permissions(self.request, quiz.classroom)
        serializer.save()


class QuestionListAPIView(ListAPIView):
    """
    API view to list Question instances for a specific quiz.

    This view returns a list of questions associated with a specific quiz.
    The user must be authenticated and a member of the classroom to access this view.

    Attributes:
        serializer_class: The serializer class to handle the question listing.
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_queryset():
            Returns the queryset of questions associated with the specified quiz.
    """
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        """
        Returns the queryset of questions associated with the specified quiz.

        This method retrieves the quiz by its ID from the URL kwargs, checks the
        user's permissions for the classroom associated with the quiz, and then
        returns the queryset of questions.

        Returns:
            QuerySet: A queryset of Question objects.

        Raises:
            Http404: If the quiz does not exist.
        """
        quiz_id = self.kwargs.get("quiz_id")

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, quiz.classroom)

        return quiz.questions.all()


class QuestionRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete a Question instance.

    This view handles the retrieval, update, and deletion of a specific question.
    The user must be authenticated to access this view. The permissions vary
    depending on the request method:
    - SAFE_METHODS (GET): The user must be a member of the classroom.
    - Non-SAFE_METHODS (PUT, DELETE): The user must be the owner of the classroom.

    Methods:
        get_permissions():
            Determines the permission classes based on the request method.

        get_object(question_id):
            Retrieves the question object by its ID and checks object permissions.
            Raises Http404 if the question does not exist.

        get(request, quiz_id, question_id, *args, **kwargs):
            Handles GET requests to retrieve the question details.

        put(request, quiz_id, question_id, *args, **kwargs):
            Handles PUT requests to update the question details.

        delete(request, quiz_id, question_id, *args, **kwargs):
            Handles DELETE requests to delete the question.
    """

    def get_permissions(self):
        """
        Sets the permission classes based on the request method.

        For SAFE_METHODS (GET), the user must be a classroom member.
        For non-SAFE_METHODS (PUT, DELETE), the user must be the classroom owner.

        Returns:
            list: The list of permission classes.
        """
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, question_id):
        """
        Retrieves the question object by its ID and checks object permissions.

        Args:
            question_id (UUID): The ID of the question to be retrieved.

        Returns:
            Question: The retrieved question object.

        Raises:
            Http404: If the question does not exist.
        """
        try:
            question = Question.objects.get(id=question_id)
            self.check_object_permissions(self.request, question.quiz.classroom)
            return question
        except Question.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: QuestionSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, quiz_id, question_id, *args, **kwargs):
        """
        Handles GET requests to retrieve the question details.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to which the question belongs.
            question_id (UUID): The ID of the question to be retrieved.

        Returns:
            Response: The response containing the question details.
        """
        self.check_permissions(request)
        question = self.get_object(question_id)
        serializer = QuestionSerializer(question, context={'quiz_id': quiz_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=QuestionSerializer,
        responses={
            200: QuestionSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, quiz_id, question_id, *args, **kwargs):
        """
        Handles PUT requests to update the question details.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to which the question belongs.
            question_id (UUID): The ID of the question to be updated.

        Returns:
            Response: The response containing the updated question details.
        """
        self.check_permissions(request)
        question = self.get_object(question_id)
        serializer = QuestionSerializer(question, data=request.data, context={'quiz_id': quiz_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, quiz_id, question_id, *args, **kwargs):
        """
        Handles DELETE requests to delete the question.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to which the question belongs.
            question_id (UUID): The ID of the question to be deleted.

        Returns:
            Response: The response indicating that the question has been deleted.
        """
        self.check_permissions(request)
        question = self.get_object(question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
