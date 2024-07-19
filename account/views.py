from django.contrib.auth import get_user_model
from django.http import Http404
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.filters import TeacherProfileFilter, StudentProfileFilter
from account.models import TeacherProfile, StudentProfile
from account.permissions import IsProfileOwnerOrReadOnly
from account.serializers import TeacherProfileSerializer, StudentProfileSerializer
from authuser.serializers import ErrorResponseSerializer

User = get_user_model()


class TeacherProfileListAPIView(ListAPIView):
    """
    API view to list TeacherProfile instances.

    This view provides a list of all teacher profiles. It supports filtering based on various
    profile attributes and requires that the user is authenticated and an admin.

    Permissions:
        - `IsAuthenticated`: The user must be authenticated to access this view.
        - `IsAdminUser`: The user must be an admin to access this view.

    Filter:
        - `TeacherProfileFilter`: Allows filtering of teacher profiles by attributes such as email,
          first name, last name, date of birth, and years of experience.

    Attributes:
        queryset: The queryset used to retrieve the teacher profiles.
        serializer_class: The serializer class used to serialize the teacher profile data.
        permission_classes: The list of permission classes required to access this view.
        filter_backends: The list of filter backends used for filtering teacher profiles.
        filterset_class: The filter set class used to define the filter criteria.

    Methods:
        get(request, *args, **kwargs):
            Handles GET requests to retrieve a list of teacher profiles based on the provided filters.

    Request:
        - Query parameters can be used to filter the teacher profiles based on various attributes.

    Responses:
        - `200 OK`: Successfully retrieved the list of teacher profiles.
        - `403 Forbidden`: If the user does not have the required permissions to access the view.
    """
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = TeacherProfileFilter


class TeacherProfileRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific TeacherProfile instance.

    This view handles the retrieval, update, and deletion of a teacher profile. The user must be authenticated
    and must either be the owner of the profile or have read-only access.

    Permissions: - `IsAuthenticated`: The user must be authenticated to access this view. -
    `IsProfileOwnerOrReadOnly`: The user must be the owner of the profile to modify it; otherwise, read-only access
    is allowed.

    Methods:
        get_object(pk):
            Retrieves a TeacherProfile instance by its ID (pk) and checks object permissions.
            Raises Http404 if the profile does not exist.

        get(request, pk, *args, **kwargs):
            Handles GET requests to retrieve the details of a specific teacher profile.

        put(request, pk, *args, **kwargs):
            Handles PUT requests to update the details of a specific teacher profile.

        delete(request, pk, *args, **kwargs):
            Handles DELETE requests to delete a specific teacher profile.

    Attributes:
        permission_classes: The list of permission classes required to access this view.

    Request:
        - GET: Retrieves the profile details.
        - PUT: Updates the profile details. Requires the full profile data.
        - DELETE: Deletes the profile and associated user account.

    Responses:
        - `200 OK`: Successfully retrieved or updated the profile.
        - `204 No Content`: Successfully deleted the profile.
        - `400 Bad Request`: Invalid request data.
        - `404 Not Found`: Profile not found or user not found for deletion.
    """
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self, pk):
        """
        Retrieves a TeacherProfile instance by its ID and checks object permissions.

        Args:
            pk (UUID): The ID of the teacher profile to be retrieved.

        Returns:
            TeacherProfile: The retrieved teacher profile instance.

        Raises:
            Http404: If the profile does not exist.
        """
        try:
            obj = TeacherProfile.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except TeacherProfile.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: TeacherProfileSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, pk, *args, **kwargs):
        """
        Handles GET requests to retrieve the details of a specific teacher profile.

        Args:
            request (Request): The HTTP request object.
            pk (UUID): The ID of the teacher profile to be retrieved.

        Returns:
            Response: The response containing the teacher profile details.
        """
        self.check_permissions(request)
        teacher_profile = self.get_object(pk)
        serializer = TeacherProfileSerializer(teacher_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=TeacherProfileSerializer,
        responses={
            200: TeacherProfileSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, pk, *args, **kwargs):
        """
        Handles PUT requests to update the details of a specific teacher profile.

        Args:
            request (Request): The HTTP request object containing updated profile data.
            pk (UUID): The ID of the teacher profile to be updated.

        Returns:
            Response: The response containing the updated teacher profile details.
        """
        self.check_permissions(request)
        teacher_profile = self.get_object(pk)
        serializer = TeacherProfileSerializer(teacher_profile, data=request.data)
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
        Handles DELETE requests to delete a specific teacher profile and associated user account.

        Args:
            request (Request): The HTTP request object.
            pk (UUID): The ID of the teacher profile to be deleted.

        Returns:
            Response: The response indicating that the profile has been deleted.
        """
        self.check_permissions(request)
        teacher_profile = self.get_object(pk)
        user = User.objects.get(id=teacher_profile.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentProfileListAPIView(ListAPIView):
    """
    API view to list all StudentProfile instances.

    This view handles the retrieval of a list of student profiles. It requires that the user is authenticated
    and has admin privileges.

    Permissions:
        - `IsAuthenticated`: The user must be authenticated to access this view.
        - `IsAdminUser`: The user must have admin privileges to access this view.

    Methods:
        get(request, *args, **kwargs):
            Handles GET requests to list student profiles, with optional filtering.

    Attributes:
        queryset: The queryset of StudentProfile instances to be listed.
        serializer_class: The serializer class used to serialize the student profile data.
        permission_classes: The list of permission classes required to access this view.
        filter_backends: The filter backends used to filter the queryset.
        filterset_class: The filterset class used to filter student profiles based on query parameters.

    Request:
        - GET: Retrieves a list of student profiles, with optional filters.

    Responses:
        - `200 OK`: Successfully retrieved the list of student profiles.
        - `401 Unauthorized`: If the user is not authenticated.
        - `403 Forbidden`: If the user does not have admin privileges.
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = StudentProfileFilter


class StudentProfileRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific StudentProfile instance.

    This view handles retrieving, updating, and deleting student profiles. It requires that the user is
    authenticated and either owns the profile or has read-only access.

    Permissions:
        - `IsAuthenticated`: The user must be authenticated to access this view.
        - `IsProfileOwnerOrReadOnly`: The user must either be the owner of the profile or have read-only access.

    Methods:
        get_object(pk):
            Retrieves the StudentProfile instance with the given primary key (pk).

        get(request, pk, *args, **kwargs):
            Handles GET requests to retrieve the details of a specific student profile.

        put(request, pk, *args, **kwargs):
            Handles PUT requests to update a specific student profile.

        delete(request, pk, *args, **kwargs):
            Handles DELETE requests to delete a specific student profile.

    Attributes:
        permission_classes: The list of permission classes required to access this view.

    Request:
        - GET: Retrieves the details of a specific student profile.
        - PUT: Updates the details of a specific student profile.
        - DELETE: Deletes a specific student profile.

    Responses:
        - `200 OK`: Successfully retrieved or updated the student profile.
        - `204 No Content`: Successfully deleted the student profile.
        - `400 Bad Request`: If there is a validation error with the request data.
        - `404 Not Found`: If the student profile does not exist.
    """
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            obj = StudentProfile.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except StudentProfile.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: StudentProfileSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        student_profile = self.get_object(pk)
        serializer = StudentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=StudentProfileSerializer,
        responses={
            200: StudentProfileSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        student_profile = self.get_object(pk)
        serializer = StudentProfileSerializer(student_profile, data=request.data)
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
        self.check_permissions(request)
        student_profile = self.get_object(pk)
        user = User.objects.get(id=student_profile.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
