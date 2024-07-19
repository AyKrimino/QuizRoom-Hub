from django.http import Http404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from authuser.serializers import ErrorResponseSerializer
from classroom.models import Classroom
from classroom.permissions import IsClassroomOwner, IsClassroomMember
from post.models import CoursePost, Comment
from post.permissions import IsCommentAuthor
from post.serializers import CoursePostSerializer, CommentSerializer


class CoursePostCreateAPIView(CreateAPIView):
    """
    API view to create a new CoursePost.

    This view handles the creation of a CoursePost object, ensuring that the
    user is authenticated and is the owner of the associated classroom.

    Attributes:
        queryset (QuerySet): A queryset containing all CoursePost objects.
        serializer_class (Serializer): The serializer class to use for
                                       validating and deserializing input, and
                                       for serializing output.
        permission_classes (list): A list of permission classes that the user
                                   must pass to access this view.
    """
    queryset = CoursePost.objects.all()
    serializer_class = CoursePostSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_serializer_context(self):
        """
        Adds additional context to the serializer.

        This method overrides the default get_serializer_context method to add
        the classroom_id from the URL keyword arguments to the serializer context.

        Returns:
            dict: The context for the serializer, including the classroom_id.
        """
        context = super().get_serializer_context()
        context["classroom_id"] = self.kwargs.get("classroom_id", None)
        return context

    def perform_create(self, serializer):
        """
        Perform the creation of a new CoursePost.

        This method overrides the default perform_create method to check object
        permissions for the classroom associated with the CoursePost before
        saving the serializer.

        Args:
            serializer (Serializer): The serializer instance that should be
                                     saved.

        Raises:
            PermissionDenied: If the user does not have permission to create a
                              CoursePost for the classroom.
        """
        classroom = serializer.validated_data["classroom"]
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class CoursePostListAPIView(ListAPIView):
    """
    API view to list all CoursePost objects for a specific classroom.

    This view handles the retrieval of CoursePost objects, ensuring that the
    user is authenticated and is a member of the specified classroom.

    Attributes:
        serializer_class (Serializer): The serializer class to use for
                                       serializing output.
        permission_classes (list): A list of permission classes that the user
                                   must pass to access this view.
    """
    serializer_class = CoursePostSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        """
        Retrieve the queryset of CoursePost objects for the specified classroom.

        This method retrieves the classroom_id from the URL keyword arguments,
        checks if the classroom exists, and then filters the CoursePost objects
        by the classroom. It also ensures that the user has permission to access
        the classroom.

        Returns:
            QuerySet: A queryset of CoursePost objects filtered by the classroom.

        Raises:
            ValidationError: If the specified classroom does not exist.
        """
        classroom_id = self.kwargs.get("classroom_id")
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise ValidationError(_("Classroom does not exist."))

        self.check_object_permissions(self.request, classroom)
        return CoursePost.objects.filter(classroom=classroom)


class CoursePostRetrieveUpdateDestroyAPIView(APIView):
    """
    API view to retrieve, update, or delete a CoursePost object.

    This view handles GET, PUT, and DELETE requests for a CoursePost object,
    ensuring that the user is authenticated and has the appropriate permissions
    for the requested operation.

    Methods:
        get_permissions: Determines the required permissions based on the request method.
        get_object: Retrieves the CoursePost object by its ID and checks permissions.
        get: Handles GET requests to retrieve the CoursePost object.
        put: Handles PUT requests to update the CoursePost object.
        delete: Handles DELETE requests to delete the CoursePost object.
    """

    def get_permissions(self):
        """
        Determines the required permissions based on the request method.

        Returns:
            list: A list of permission classes that the user must pass to access this view.
        """
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, post_id):
        """
        Retrieves the CoursePost object by its ID and checks permissions.

        Args:
            post_id (uuid): The ID of the CoursePost object to retrieve.

        Returns:
            CoursePost: The retrieved CoursePost object.

        Raises:
            Http404: If the CoursePost object does not exist.
        """
        try:
            post = CoursePost.objects.get(id=post_id)
            classroom = post.classroom
            self.check_object_permissions(self.request, classroom)
            return post
        except CoursePost.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={
            200: CoursePostSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, classroom_id, post_id, *args, **kwargs):
        """
        Handles GET requests to retrieve the CoursePost object.

        Args:
            request (Request): The HTTP request object.
            classroom_id (uuid): The ID of the classroom.
            post_id (uuid): The ID of the CoursePost object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The serialized CoursePost object and a 200 OK status.
        """
        self.check_permissions(request)
        post = self.get_object(post_id)
        serializer = CoursePostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CoursePostSerializer,
        responses={
            200: CoursePostSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, classroom_id, post_id, *args, **kwargs):
        """
        Handles PUT requests to update the CoursePost object.

        Args:
            request (Request): The HTTP request object.
            classroom_id (uuid): The ID of the classroom.
            post_id (uuid): The ID of the CoursePost object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The serialized updated CoursePost object and a 200 OK status.
        """
        self.check_permissions(request)
        post = self.get_object(post_id)
        serializer = CoursePostSerializer(post, data=request.data, context={"classroom_id": classroom_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, classroom_id, post_id, *args, **kwargs):
        """
        Handles DELETE requests to delete the CoursePost object.

        Args:
            request (Request): The HTTP request object.
            classroom_id (uuid): The ID of the classroom.
            post_id (uuid): The ID of the CoursePost object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A 204 No Content status.
        """
        self.check_permissions(request)
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateAPIView(CreateAPIView):
    """
    API view to create a new Comment object.

    This view handles POST requests to create a new Comment object, ensuring that the user is authenticated
    and a member of the classroom associated with the post.

    Attributes:
        queryset (QuerySet): The queryset of Comment objects.
        serializer_class (Serializer): The serializer class for Comment objects.
        permission_classes (list): The list of permission classes that the user must pass to access this view.

    Methods:
        get_serializer_context: Adds additional context to the serializer.
        perform_create: Performs the creation of the Comment object and checks permissions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_serializer_context(self):
        """
        Adds additional context to the serializer.

        This method adds the post ID and the user making the request to the serializer context.

        Returns:
            dict: The context dictionary for the serializer.
        """
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id", None)
        context["user"] = self.request.user
        return context

    def perform_create(self, serializer):
        """
        Performs the creation of the Comment object and checks permissions.

        This method checks if the user has the appropriate permissions to create a comment in the classroom
        associated with the post, and then saves the serializer.

        Args:
            serializer (Serializer): The serializer for the Comment object.
        """
        post = serializer.validated_data["post"]
        classroom = post.classroom
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class CommentListAPIView(ListAPIView):
    """
    API view to retrieve a list of Comment objects for a specific post.

    This view handles GET requests to list all comments associated with a specific post,
    ensuring that the user is authenticated and a member of the classroom associated with the post.

    Attributes:
        serializer_class (Serializer): The serializer class for Comment objects.
        permission_classes (list): The list of permission classes that the user must pass to access this view.

    Methods:
        get_queryset: Retrieves the queryset of comments for the specified post, ensuring that the post exists
                      and that the user has the appropriate permissions.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        """
        Retrieves the queryset of comments for the specified post.

        This method checks if the post exists and if the user has the appropriate permissions
        to access the comments for the post. If the post does not exist, a validation error is raised.

        Returns:
            QuerySet: The queryset of comments for the specified post.

        Raises:
            ValidationError: If the post does not exist.
        """
        post_id = self.kwargs.get("post_id")
        try:
            post = CoursePost.objects.get(id=post_id)
        except CoursePost.DoesNotExist:
            raise ValidationError(_("Post does not exist."))

        classroom = post.classroom
        self.check_object_permissions(self.request, classroom)
        return post.comments.all()


class CommentRetrieveUpdateDeleteAPIView(APIView):
    """
    API view to retrieve, update, or delete a Comment object.

    This view handles GET, PUT, and DELETE requests for a specific comment,
    ensuring that the user is authenticated and has the appropriate permissions
    based on the request method.

    Methods: get_permissions: Sets the appropriate permission classes based on the request method. get_object:
    Retrieves the comment object and checks permissions for both the classroom and the comment.
    check_permissions_for_classroom_and_comment: Checks permissions for both the classroom and the comment based on
    the request method. get: Handles GET requests to retrieve the comment. put: Handles PUT requests to update the
    comment. delete: Handles DELETE requests to delete the comment.
    """

    def get_permissions(self):
        """
        Sets the appropriate permission classes based on the request method.

        For GET requests, requires the user to be authenticated and a classroom member.
        For PUT requests, requires the user to be authenticated and the comment author.
        For DELETE requests, requires the user to be authenticated.

        Returns:
            list: List of permission classes.
        """
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAuthenticated, IsCommentAuthor]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self, comment_id):
        """
        Retrieves the comment object and checks permissions for both the classroom and the comment.

        Args:
            comment_id (uuid): The ID of the comment.

        Returns:
            Comment: The retrieved comment object.

        Raises:
            Http404: If the comment does not exist.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            classroom = comment.post.classroom
            self.check_permissions_for_classroom_and_comment(classroom, comment)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def check_permissions_for_classroom_and_comment(self, classroom, comment):
        """
        Checks permissions for both the classroom and the comment based on the request method.

        Args:
            classroom (Classroom): The classroom object associated with the comment.
            comment (Comment): The comment object.

        Raises:
            PermissionDenied: If the user does not have permission to perform the action.
        """
        if self.request.method in SAFE_METHODS:
            self.check_object_permissions(self.request, classroom)
        elif self.request.method == "PUT":
            self.check_object_permissions(self.request, comment)
        elif self.request.method == "DELETE":
            if not IsClassroomOwner().has_object_permission(self.request, self, classroom):
                if not IsCommentAuthor().has_object_permission(self.request, self, comment):
                    self.permission_denied(self.request,
                                           message=_("You do not have permission to perform this action."))

    @extend_schema(
        responses={
            200: CommentSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, classroom_id, post_id, comment_id, *args, **kwargs):
        """
        Handles GET requests to retrieve the comment.

        Args:
            request (Request): The HTTP request object.
            classroom_id (uuid): The ID of the classroom.
            post_id (uuid): The ID of the post.
            comment_id (uuid): The ID of the comment.

        Returns:
            Response: The response containing the serialized comment data and HTTP status 200 OK.
        """
        self.check_permissions(request)
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def put(self, request, classroom_id, post_id, comment_id, *args, **kwargs):
        """
        Handles PUT requests to update the comment.

        Args:
            request (Request): The HTTP request object.
            classroom_id (uuid): The ID of the classroom.
            post_id (uuid): The ID of the post.
            comment_id (uuid): The ID of the comment.

        Returns:
            Response: The response containing the serialized updated comment data and HTTP status 200 OK.
        """
        self.check_permissions(request)
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data, context={"post_id": post_id, "user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: ErrorResponseSerializer,
        },
    )
    def delete(self, request, classroom_id, post_id, comment_id, *args, **kwargs):
        """
        Handles DELETE requests to delete the comment.

        Args:
            request (Request): The HTTP request object.
            classroom_id (uuid): The ID of the classroom.
            post_id (uuid): The ID of the post.
            comment_id (uuid): The ID of the comment.

        Returns:
            Response: The response with HTTP status 204 NO CONTENT.
        """
        self.check_permissions(request)
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
