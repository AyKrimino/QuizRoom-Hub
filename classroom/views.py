from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from account.models import StudentProfile, TeacherProfile
from authuser.serializers import ErrorResponseSerializer
from .models import Classroom, StudentClassroom
from .permissions import (IsClassroomMember, IsClassroomOwner, IsTeacher, IsStudentOrTeacher, )
from .serializers import ClassroomSerializer, StudentClassroomSerializer


class ClassroomListAPIView(ListAPIView):
    """
    API view to retrieve a list of classrooms created by the authenticated teacher.

    This view is accessible only to authenticated users who have a `TeacherProfile`.
    The view will return a list of all classrooms created by the authenticated teacher.

    Permissions:
    - `IsAuthenticated`: Ensures that the user is logged in.
    - `IsTeacher`: Ensures that the user has a `TeacherProfile`.

    Serializer:
    - Uses the `ClassroomSerializer` to serialize the classroom data.

    Methods:
    - `get_queryset`: Retrieves the list of classrooms for the authenticated teacher.
    """
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        """
        Retrieve the list of classrooms created by the authenticated teacher.

        Returns:
            QuerySet: A queryset of classrooms filtered by the authenticated teacher.
        """
        teacher = TeacherProfile.objects.get(user=self.request.user)
        return Classroom.objects.filter(teacher=teacher)


class ClassroomCreateAPIView(CreateAPIView):
    """
    API view to create a new classroom.

    This view is accessible only to authenticated users who have a `TeacherProfile`.
    The view allows the authenticated teacher to create a new classroom.

    Permissions:
    - `IsAuthenticated`: Ensures that the user is logged in.
    - `IsTeacher`: Ensures that the user has a `TeacherProfile`.

    Serializer:
    - Uses the `ClassroomSerializer` to serialize the classroom data.

    Methods:
    - `perform_create`: Associates the new classroom with the authenticated teacher.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        """
        Save the new classroom instance with the authenticated teacher.

        Args:
            serializer (ClassroomSerializer): The serializer instance containing the validated data.

        Returns:
            None
        """
        teacher = TeacherProfile.objects.get(user=self.request.user)
        serializer.save(teacher=teacher)


class ClassroomRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific classroom.

    This view is accessible to authenticated users who are either members of the classroom
    (students or the teacher who created it) or the owner of the classroom (the teacher who
    created it).

    Permissions:
    - `IsAuthenticated`: Ensures that the user is logged in.
    - `IsClassroomMember`: Allows access to retrieve the classroom if the user is a member
      (either a student or the teacher who created it).
    - `IsClassroomOwner`: Allows access to update or delete the classroom if the user is the
      teacher who created it.

    Methods:
    - `get_permissions`: Sets appropriate permissions based on the HTTP method. Members of
      the classroom can view (`GET` method), while the owner can update or delete (`PUT` and
      `DELETE` methods).
    - `get_object`: Retrieves the classroom object based on the provided `pk`.
    - `get`: Handles `GET` requests to retrieve the classroom details.
    - `put`: Handles `PUT` requests to update the classroom details.
    - `delete`: Handles `DELETE` requests to delete the classroom.
    """

    def get_permissions(self):
        """
        Set permissions based on the HTTP method.

        Members of the classroom can view (`GET` method), while the owner can
        update or delete (`PUT` and `DELETE` methods).
        """
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, pk):
        """
        Retrieve the classroom object based on the provided primary key (`pk`).

        Args:
            pk (uuid): Primary key of the classroom to retrieve.

        Returns:
            Classroom: The retrieved classroom object.

        Raises:
            Http404: If the classroom with the provided `pk` does not exist.
        """
        try:
            obj = Classroom.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Classroom.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: ClassroomSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, pk, *args, **kwargs):
        """
        Handle GET requests to retrieve the details of a specific classroom.

        Args:
            request: The HTTP request object.
            pk (uuid): Primary key of the classroom to retrieve.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response object containing serialized classroom data.

        Raises:
            Http404: If the classroom with the provided `pk` does not exist.
        """
        self.check_permissions(request)
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ClassroomSerializer,
        responses={
            200: ClassroomSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, pk, *args, **kwargs):
        """
        Handle PUT requests to update a specific classroom.

        Args:
            request: The HTTP request object.
            pk (uuid): Primary key of the classroom to update.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response object containing serialized updated classroom data.

        Raises:
            Http404: If the classroom with the provided `pk` does not exist.
        """
        self.check_permissions(request)
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, pk, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific classroom.

        Args:
            request: The HTTP request object.
            pk (uuid): Primary key of the classroom to delete.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response object with status HTTP_204_NO_CONTENT.

        Raises:
            Http404: If the classroom with the provided `pk` does not exist.
        """
        self.check_permissions(request)
        classroom = self.get_object(pk)
        classroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentClassroomListAPIView(ListAPIView):
    """
    API view to list student classroom relationships based on user type.

    This view is accessible to authenticated users who are either students or teachers.
    Students will see classrooms they are enrolled in, while teachers will see classrooms
    they created along with the students enrolled in each classroom.

    Permissions:
    - `IsAuthenticated`: Ensures that the user is logged in.
    - `IsStudentOrTeacher`: Allows access to either students or teachers.

    Methods:
    - `get_queryset`: Returns a queryset based on whether the user is a student or teacher.
      Students get classrooms they are enrolled in, while teachers get classrooms they created
      along with student enrollment details.
    """
    serializer_class = StudentClassroomSerializer
    permission_classes = [IsAuthenticated, IsStudentOrTeacher]

    def get_queryset(self):
        """
        Return the queryset based on the type of user (student or teacher).

        Returns:
        - For students: Queryset of student classroom relationships they are enrolled in.
        - For teachers: Queryset of student classroom relationships for classrooms they created,
          including student details for each classroom.
        """
        user = self.request.user
        if StudentProfile.objects.filter(user=user).exists():
            student = StudentProfile.objects.get(user=user)
            return StudentClassroom.objects.filter(student=student)
        else:  # user is a teacher
            teacher = TeacherProfile.objects.get(user=user)
            classrooms = teacher.classrooms.all()
            return StudentClassroom.objects.filter(classroom__in=classrooms)


class StudentClassroomCreateAPIView(APIView):
    """
    API view to create student classroom relationships.

    This view allows authenticated users who are either students or teachers to create
    student classroom relationships. Teachers can add students to their classrooms by
    passing the classroom_id and student_id in the request data. Students can join any
    classroom by passing the classroom_id (uuid field) in the request body.

    Permissions:
    - `IsAuthenticated`: Ensures that the user is logged in.
    - `IsStudentOrTeacher`: Allows access to either students or teachers.

    Methods:
    - `post`: Handles POST requests to create a student classroom relationship. Checks
      permissions, validates serializer data, and saves the relationship.
    - `perform_create`: Performs the creation of the student classroom relationship. Checks
      if the user is a teacher to validate the classroom ownership before saving.

    Raises:
    - `ValidationError`: Raised if a teacher tries to add a student to a classroom they do
      not own.

    Attributes:
    - `permission_classes`: List of permission classes required for accessing this view.
    """
    permission_classes = [IsAuthenticated, IsStudentOrTeacher]

    @extend_schema(
        request=StudentClassroomSerializer,
        responses={
            201: StudentClassroomSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a student classroom relationship.

        Args:
        - request: HTTP request object containing data to create the relationship.

        Returns:
        - Response: JSON response with serialized data of the created relationship and
          HTTP status code.

        Raises:
        - Http404: If the classroom or student profile does not exist.
        """
        self.check_permissions(request)
        serializer = StudentClassroomSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Perform the creation of the student classroom relationship.

        Args:
        - serializer: Serializer instance containing validated data to create the relationship.

        Raises:
        - ValidationError: If the teacher tries to add a student to a classroom they do not own.
        """
        user = self.request.user

        if TeacherProfile.objects.filter(user=user).exists():
            classroom_id = serializer.validated_data['classroom']['id']
            teacher = TeacherProfile.objects.get(user=user)
            if not Classroom.objects.filter(id=classroom_id, teacher=teacher).exists():
                raise ValidationError("Not a valid classroom.")
        serializer.save()


class StudentClassroomRetrieveDestroyAPIView(APIView):
    """
    API view to retrieve and delete a student classroom relationship.

    This view allows authenticated users to retrieve details of a student classroom
    relationship if they are a member of the classroom (for safe methods) or the owner
    of the classroom (for unsafe methods like DELETE). The relationships are identified
    using the student_id and classroom_id.

    Permissions:
    - `IsAuthenticated`: Ensures that the user is logged in.
    - `IsClassroomMember`: Allows access to retrieve details of the relationship if
      the user is a member of the classroom (for safe methods).
    - `IsClassroomOwner`: Allows access to delete the relationship if the user is the
      owner of the classroom (for unsafe methods).

    Methods:
    - `get_permissions`: Determines the permission classes based on the HTTP method.
    - `get_object`: Retrieves the student classroom relationship based on the provided
      student_id and classroom_id.
    - `get`: Handles GET requests to retrieve details of the student classroom relationship.
    - `delete`: Handles DELETE requests to delete the student classroom relationship.

    Raises:
    - `Http404`: If the student profile, classroom, or student classroom relationship
      does not exist.
    """

    def get_permissions(self):
        """
        Returns the list of permissions based on the HTTP method.

        For safe methods (GET), uses `IsClassroomMember` permission.
        For unsafe methods (DELETE), uses `IsClassroomOwner` permission.

        Returns:
        - List: List of permission classes based on the HTTP method.
        """
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, student_id, classroom_id):
        """
        Retrieve the student classroom relationship object.

        Args:
        - student_id: UUID of the student profile.
        - classroom_id: UUID of the classroom.

        Returns:
        - StudentClassroom: StudentClassroom object representing the relationship.

        Raises:
        - Http404: If the student profile, classroom, or student classroom relationship
          does not exist.
        """
        try:
            student = StudentProfile.objects.get(id=student_id)
            classroom = Classroom.objects.get(id=classroom_id)
            obj = StudentClassroom.objects.get(student=student, classroom=classroom)
            self.check_object_permissions(self.request, classroom)
            return obj
        except (StudentProfile.DoesNotExist, Classroom.DoesNotExist, StudentClassroom.DoesNotExist):
            raise Http404

    @extend_schema(
        responses={
            200: StudentClassroomSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, student_id, classroom_id, *args, **kwargs):
        """
        Handle GET requests to retrieve details of the student classroom relationship.

        Args:
        - request: HTTP request object.
        - student_id: UUID of the student profile.
        - classroom_id: UUID of the classroom.

        Returns:
        - Response: JSON response with serialized data of the student classroom relationship
          and HTTP status code.
        """
        self.check_permissions(request)
        student_classroom = self.get_object(student_id, classroom_id)
        serializer = StudentClassroomSerializer(student_classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, student_id, classroom_id, *args, **kwargs):
        """
        Handle DELETE requests to delete the student classroom relationship.

        Args:
        - request: HTTP request object.
        - student_id: UUID of the student profile.
        - classroom_id: UUID of the classroom.

        Returns:
        - Response: Empty response with HTTP status code indicating successful deletion.
        """
        self.check_permissions(request)
        student_classroom = self.get_object(student_id, classroom_id)
        student_classroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
