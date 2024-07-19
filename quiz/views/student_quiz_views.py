from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from authuser.serializers import ErrorResponseSerializer
from classroom.permissions import IsClassroomMember, IsStudent
from quiz.models import StudentQuiz, Quiz
from quiz.serializers import StudentAnswerSerializer, StudentQuizSerializer


class StudentAnswerCreateAPIView(APIView):
    """
    API view to create a new StudentAnswer instance.

    This view handles the creation of new student answers for a specific quiz.
    It requires that the user is authenticated, a member of the classroom, and a student.

    Attributes:
        permission_classes: The list of permission classes required to access this view.

    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to create a new student answer.
    """
    permission_classes = [IsAuthenticated, IsClassroomMember, IsStudent]

    @extend_schema(
        request=StudentAnswerSerializer,
        responses={
            201: StudentAnswerSerializer,
            400: ErrorResponseSerializer,
        },
        description="Create a new student answer for a specific quiz."
    )
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new student answer.

        This method validates the quiz ID from the URL kwargs, checks the user's
        permissions for the associated classroom, and then creates the student answer.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response containing the created student answer details.

        Raises:
            ValidationError: If the quiz does not exist.
        """
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
    """
    API view to create a new StudentQuiz instance.

    This view handles the creation of new student quiz instances. It requires that the user is authenticated,
    a member of the classroom, and a student.

    Attributes:
        queryset: The queryset of StudentQuiz objects.
        serializer_class: The serializer class to handle student quiz creation.
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_serializer_context():
            Adds the 'student' and 'quiz_id' to the serializer context.

        perform_create(serializer):
            Handles the actual saving of the student quiz. Validates the associated quiz and
            checks that the user has the necessary permissions.
    """

    queryset = StudentQuiz.objects.all()
    serializer_class = StudentQuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember, IsStudent]

    def get_serializer_context(self):
        """
        Adds additional context to the serializer.

        This method adds the 'student' from the request user and the 'quiz_id' from the URL kwargs
        to the serializer context, allowing the serializer to access them during validation and saving.

        Returns:
            dict: The updated context dictionary.
        """
        context = super().get_serializer_context()
        context["student"] = self.request.user.student_profile
        context["quiz_id"] = self.kwargs.get("quiz_id")
        return context

    def perform_create(self, serializer):
        """
        Handles the actual saving of the student quiz.

        This method validates the associated quiz and checks that the user has the necessary permissions
        to add a student quiz to the classroom.

        Args:
            serializer (Serializer): The serializer instance containing the validated data.

        Raises:
            ValidationError: If the quiz does not exist.
        """
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
    """
    API view to list StudentQuiz instances.

    This view returns a list of student quizzes for a specific quiz. It requires that the user
    is authenticated and a member of the classroom.

    Attributes:
        serializer_class: The serializer class to handle the student quiz listing.
        permission_classes: The list of permission classes required to access this view.

    Methods:
        get_queryset():
            Returns the queryset of student quizzes associated with the specified quiz.
            If the user is a student, it returns only their student quizzes. If the user
            is a teacher, it returns all student quizzes for the classroom.
    """
    serializer_class = StudentQuizSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        """
        Returns the queryset of student quizzes associated with the specified quiz.

        This method retrieves the quiz by its ID from the URL kwargs, checks the user's
        permissions for the associated classroom, and then returns the appropriate queryset
        based on whether the user is a student or a teacher.

        Returns:
            QuerySet: A queryset of StudentQuiz objects.

        Raises:
            ValidationError: If the quiz does not exist.
        """
        user = self.request.user
        quiz_id = self.kwargs.get("quiz_id")
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
