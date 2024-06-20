from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import StudentProfile, TeacherProfile
from .models import Classroom, StudentClassroom
from .permissions import (IsClassroomMember, IsClassroomOwner, IsTeacher, IsClassroomOwnerOrStudent,
                          IsClassroomOwnerOrClassroomStudentMember, )
from .serializers import ClassroomSerializer, StudentClassroomSerializer


class ClassroomListAPIView(ListAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        teacher = TeacherProfile.objects.get(user=self.request.user)
        return Classroom.objects.filter(teacher=teacher)


class ClassroomCreateAPIView(CreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


class ClassroomRetrieveUpdateDestroyAPIView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, pk):
        try:
            obj = Classroom.objects.get(id=pk)
            return obj
        except Classroom.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        classroom = self.get_object(pk)
        classroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentClassroomListAPIView(ListAPIView):
    queryset = StudentClassroom.objects.all()
    serializer_class = StudentClassroomSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]


class StudentClassroomCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsClassroomOwnerOrStudent]

    def post(self, request, *args, **kwargs):
        serializer = StudentClassroomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentClassroomRetrieveDestroyAPIView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwnerOrClassroomStudentMember]
        return super().get_permissions()

    def get_object(self, student_id, classroom_id):
        try:
            student = StudentProfile.objects.get(id=student_id)
            classroom = Classroom.objects.get(id=classroom_id)
            obj = StudentClassroom.objects.get(student=student, classroom=classroom)
            return obj
        except (StudentProfile.DoesNotExist, Classroom.DoesNotExist, StudentClassroom.DoesNotExist):
            raise Http404

    def get(self, request, student_id, classroom_id, *args, **kwargs):
        student_classroom = self.get_object(student_id, classroom_id)
        serializer = StudentClassroomSerializer(student_classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, student_id, classroom_id, *args, **kwargs):
        student_classroom = self.get_object(student_id, classroom_id)
        student_classroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
