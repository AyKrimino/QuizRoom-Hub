from rest_framework.permissions import BasePermission


class IsClassroomMember(BasePermission):
    pass


class IsClassroomOwner(BasePermission):
    pass


class IsStudent(BasePermission):
    pass


class IsTeacher(BasePermission):
    pass
