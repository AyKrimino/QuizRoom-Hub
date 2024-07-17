from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from classroom.models import Classroom
from classroom.permissions import IsClassroomOwner, IsClassroomMember
from post.models import CoursePost, Comment
from post.permissions import IsCommentAuthor
from post.serializers import CoursePostSerializer, CommentSerializer


class CoursePostCreateAPIView(CreateAPIView):
    queryset = CoursePost.objects.all()
    serializer_class = CoursePostSerializer
    permission_classes = [IsAuthenticated, IsClassroomOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["classroom_id"] = self.kwargs.get("classroom_id", None)
        return context

    def perform_create(self, serializer):
        classroom = serializer.validated_data["classroom"]
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class CoursePostListAPIView(ListAPIView):
    serializer_class = CoursePostSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        classroom_id = self.kwargs.get("classroom_id")
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise ValidationError(_("Classroom does not exist."))

        self.check_object_permissions(self.request, classroom)
        return CoursePost.objects.filter(classroom=classroom)


class CoursePostRetrieveUpdateDestroyAPIView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        else:
            self.permission_classes = [IsAuthenticated, IsClassroomOwner]
        return super().get_permissions()

    def get_object(self, post_id):
        try:
            post = CoursePost.objects.get(id=post_id)
            classroom = post.classroom
            self.check_object_permissions(self.request, classroom)
            return post
        except CoursePost.DoesNotExist:
            raise Http404

    def get(self, request, classroom_id, post_id, *args, **kwargs):
        self.check_permissions(request)
        post = self.get_object(post_id)
        serializer = CoursePostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, classroom_id, post_id, *args, **kwargs):
        self.check_permissions(request)
        post = self.get_object(post_id)
        serializer = CoursePostSerializer(post, data=request.data, context={"classroom_id": classroom_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, classroom_id, post_id, *args, **kwargs):
        self.check_permissions(request)
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id", None)
        context["user"] = self.request.user
        return context

    def perform_create(self, serializer):
        post = serializer.validated_data["post"]
        classroom = post.classroom
        self.check_object_permissions(self.request, classroom)
        serializer.save()


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsClassroomMember]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        try:
            post = CoursePost.objects.get(id=post_id)
        except CoursePost.DoesNotExist:
            raise ValidationError(_("Post does not exist."))

        classroom = post.classroom
        self.check_object_permissions(self.request, classroom)
        return post.comments.all()


class CommentRetrieveUpdateDeleteAPIView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsClassroomMember]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAuthenticated, IsCommentAuthor]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            classroom = comment.post.classroom
            self.check_permissions_for_classroom_and_comment(classroom, comment)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def check_permissions_for_classroom_and_comment(self, classroom, comment):
        if self.request.method in SAFE_METHODS:
            self.check_object_permissions(self.request, classroom)
        elif self.request.method == "PUT":
            self.check_object_permissions(self.request, comment)
        elif self.request.method == "DELETE":
            if not IsClassroomOwner().has_object_permission(self.request, self,
                                                            classroom) and not IsCommentAuthor().has_object_permission(
                self.request, self, comment):
                self.permission_denied(self.request, message=_("You do not have permission to perform this action."))

    def get(self, request, classroom_id, post_id, comment_id, *args, **kwargs):
        self.check_permissions(request)
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, classroom_id, post_id, comment_id, *args, **kwargs):
        self.check_permissions(request)
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data, context={"post_id": post_id, "user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, classroom_id, post_id, comment_id, *args, **kwargs):
        self.check_permissions(request)
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
