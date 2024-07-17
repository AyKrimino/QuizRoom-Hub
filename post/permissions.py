from rest_framework.permissions import BasePermission


class IsCommentAuthor(BasePermission):
    """
    Custom permission to only allow authors of a comment to edit it.

    Methods: - has_object_permission(request, view, obj): Returns `True` if the user making the request is the author
    of the comment, `False` otherwise.

    Usage:
    Apply this permission to views where you want to restrict access to actions (such as update or delete) to the author of the comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user making the request is the author of the comment.

        Args:
        - request: The HTTP request object.
        - view: The view that is being accessed.
        - obj: The object being accessed (in this case, a Comment instance).

        Returns:
        - bool: `True` if the request.user is the author of the comment, `False` otherwise.
        """
        return request.user == obj.user
