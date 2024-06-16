from django.urls import path

from .views import (TeacherProfileListAPIView,
                    TeacherProfileRetrieveUpdateDestroyAPIView,
                    StudentProfileListAPIView,
                    StudentProfileRetrieveUpdateDestroyAPIView)

app_name = "account"

urlpatterns = [
    path("profiles/teachers/", TeacherProfileListAPIView.as_view(), name="teachers-list"),
    path("profiles/teachers/<uuid:pk>/", TeacherProfileRetrieveUpdateDestroyAPIView.as_view(), name="teachers-detail"),
    path("profiles/students/", StudentProfileListAPIView.as_view(), name="students-list"),
    path("profiles/students/<uuid:pk>/", StudentProfileRetrieveUpdateDestroyAPIView.as_view(), name="students-detail"),
]
