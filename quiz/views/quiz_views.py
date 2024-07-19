from django.http import Http404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from account.models import TeacherProfile
from authuser.serializers import ErrorResponseSerializer
from classroom.models import Classroom
from classroom.permissions import IsClassroomOwner, IsTeacher, IsClassroomMember
from quiz.models import Quiz
from quiz.serializers import QuizSerializer


class QuizCreateAPIView(CreateAPIView):
    """
    API view to create a new Quiz instance.

    This view handles the creation of new quizzes. It requires that the user
    is authenticated and is the owner of the classroom to which the quiz is
    being added. The view ensures that the classroom specified in the request
    exists and that the user has the necessary permissions to add a quiz to
    that classroom.

    Attributes:
        queryset: The queryset of Quiz objects.
        serializer_class: The serializer class to handle quiz creation.
        permission_classes: The list of permission classes required to access
            this view.

    Methods:
        perform_create(serializer):
            Handles the actual saving of the quiz. Validates the classroom ID
            and checks that the classroom exists. Also ensures the user has the
            required permissions.
    """
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
    """
    API view to list Quiz instances.

    This view returns a list of quizzes that are associated with the classrooms
    of the authenticated teacher. The user must be authenticated and have a
    teacher profile.

    Attributes:
        serializer_class: The serializer class to handle the quiz listing.
        permission_classes: The list of permission classes required to access
            this view.

    Methods:
        get_queryset():
            Returns the queryset of quizzes associated with the teacher's
            classrooms.
    """
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        """
        Returns the queryset of quizzes associated with the teacher's classrooms.

        The queryset is filtered to include only the quizzes that are linked
        to the classrooms managed by the authenticated teacher.

        Returns:
            QuerySet: A queryset of Quiz objects.
        """
        user = self.request.user
        teacher = TeacherProfile.objects.get(user=user)
        return Quiz.objects.filter(classroom__in=teacher.classrooms.all())


class QuizRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete a Quiz instance.

    This view handles the retrieval, update, and deletion of a specific quiz.
    The user must be authenticated to access this view. The permissions vary
    depending on the request method:
    - SAFE_METHODS (GET): The user must be a member of the classroom.
    - Non-SAFE_METHODS (PUT, DELETE): The user must be the owner of the classroom.

    Methods:
        get_permissions():
            Determines the permission classes based on the request method.

        get_object(quiz_id):
            Retrieves the quiz object by its ID and checks object permissions.
            Raises Http404 if the quiz does not exist.

        get(request, quiz_id, *args, **kwargs):
            Handles GET requests to retrieve the quiz details.

        put(request, quiz_id, *args, **kwargs):
            Handles PUT requests to update the quiz details.

        delete(request, quiz_id, *args, **kwargs):
            Handles DELETE requests to delete the quiz.
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

    def get_object(self, quiz_id):
        """
        Retrieves the quiz object by its ID and checks object permissions.

        Args:
            quiz_id (UUID): The ID of the quiz to be retrieved.

        Returns:
            Quiz: The retrieved quiz object.

        Raises:
            Http404: If the quiz does not exist.
        """
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            classroom = quiz.classroom
            self.check_object_permissions(self.request, classroom)
            return quiz
        except Quiz.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: QuizSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, quiz_id, *args, **kwargs):
        """
        Handles GET requests to retrieve the quiz details.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to be retrieved.

        Returns:
            Response: The response containing the quiz details.
        """
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=QuizSerializer,
        responses={
            200: QuizSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, quiz_id, *args, **kwargs):
        """
        Handles PUT requests to update the quiz details.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to be updated.

        Returns:
            Response: The response containing the updated quiz details.
        """
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        serializer = QuizSerializer(quiz, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, quiz_id, *args, **kwargs):
        """
        Handles DELETE requests to delete the quiz.

        Args:
            request (Request): The HTTP request object.
            quiz_id (UUID): The ID of the quiz to be deleted.

        Returns:
            Response: The response indicating that the quiz has been deleted.
        """
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
