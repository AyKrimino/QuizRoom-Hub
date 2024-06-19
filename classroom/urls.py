from django.urls import path

from .views import (ClassroomListAPIView, ClassroomCreateAPIView, ClassroomRetrieveUpdateDestroyAPIView,
                    StudentClassroomListAPIView,
                    StudentClassroomCreateAPIView, StudentClassroomRetrieveDestroyAPIView)

app_name = "classroom"

urlpatterns = [
    path("classrooms/", ClassroomListAPIView, name="classrooms-list"),
    path("classrooms/create/", ClassroomCreateAPIView, name="classrooms-create"),
    path("classrooms/<uuid:pk>/", ClassroomRetrieveUpdateDestroyAPIView, name="classroom-detail"),
    path("students-classrooms/", StudentClassroomListAPIView, name="students-classrooms-list"),
    path("students-classrooms/create/", StudentClassroomCreateAPIView, name="students-classrooms-create"),
    path("students-classrooms/<uuid:student_id>/<uuid:classroom_id>/", StudentClassroomRetrieveDestroyAPIView,
         name="students-classrooms-detail"),
]
