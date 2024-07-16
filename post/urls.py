from django.urls import path
from post import views

app_name = "post"

urlpatterns = [
    path("classrooms/<uuid:classroom_id>/posts/create/", views.CoursePostCreateAPIView.as_view(), name="posts-create"),
    path("classrooms/<uuid:classroom_id>/posts/", views.CoursePostListAPIView.as_view(), name="posts-list"),
    path("classrooms/<uuid:classroom_id>/posts/<uuid:post_id>/", views.CoursePostRetrieveUpdateDestroyAPIView.as_view(),
         name="posts-detail"),
    path("classrooms/<uuid:classroom_id>/posts/<uuid:post_id>/comments/create/", views.CommentCreateAPIView.as_view(),
         name="comments-create"),
    path("classrooms/<uuid:classroom_id>/posts/<uuid:post_id>/comments/", views.CommentListAPIView.as_view(),
         name="comments-list"),
    path("classrooms/<uuid:classroom_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/",
         views.CommentRetrieveUpdateDeleteAPIView.as_view(), name="comments-detail"),
]
