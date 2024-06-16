from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TeacherProfile, StudentProfile
from .permissions import IsProfileOwnerOrReadOnly
from .serializers import TeacherProfileSerializer, StudentProfileSerializer

User = get_user_model()


class TeacherProfileListAPIView(ListAPIView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class TeacherProfileRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            obj = TeacherProfile.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except TeacherProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        teacher_profile = self.get_object(pk)
        serializer = TeacherProfileSerializer(teacher_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        teacher_profile = self.get_object(pk)
        serializer = TeacherProfileSerializer(teacher_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class StudentProfileRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            obj = StudentProfile.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except StudentProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        student_profile = self.get_object(pk)
        serializer = StudentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        student_profile = self.get_object(pk)
        serializer = StudentProfileSerializer(student_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        student_profile = self.get_object(pk)
        user = User.objects.get(id=student_profile.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
