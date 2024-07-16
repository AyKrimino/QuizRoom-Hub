from rest_framework.permissions import BasePermission
from classroom.permissions import IsClassroomOwner


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass


IsClassroomOwnerOrCommentAuthor = IsClassroomOwner | IsCommentAuthor
