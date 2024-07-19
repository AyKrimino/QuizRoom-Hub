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
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = TeacherProfileFilter


class TeacherProfileRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self, pk):
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
        self.check_permissions(request)
        teacher_profile = self.get_object(pk)
        user = User.objects.get(id=teacher_profile.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentProfileListAPIView(ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = StudentProfileFilter


class StudentProfileRetrieveUpdateDestroyAPIView(APIView):
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
