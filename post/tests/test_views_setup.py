from django.urls import reverse

from classroom.tests.test_setup import TestSetUp
from post.models import CoursePost, Comment


class TestSetup(TestSetUp):
    def setUp(self):
        super().setUp()
        self.posts_create_url = reverse("post:posts-create", kwargs={"classroom_id": str(self.classroom1_id)})
        self.posts_list_url = reverse("post:posts-list", kwargs={"classroom_id": str(self.classroom1_id)})

        self.post_data = {
            "title": self.fake.name(),
            "content": self.fake.text(),
        }

        self.post = CoursePost.objects.create(
            title="title1",
            content="content title1",
            classroom=self.classroom1,
        )
        self.posts_detail_url = reverse("post:posts-detail",
                                        kwargs={"classroom_id": str(self.classroom1_id), "post_id": str(self.post.id)})

        self.comments_create_url = reverse("post:comments-create", kwargs={"classroom_id": str(self.classroom1_id),
                                                                           "post_id": str(self.post.id)})
        self.comments_list_url = reverse("post:comments-list", kwargs={"classroom_id": str(self.classroom1_id),
                                                                       "post_id": str(self.post.id)})

        self.comment_data = {
            "content": self.fake.text(),
        }

        self.teacher_comment = Comment.objects.create(
            content="teacher comment content",
            post=self.post,
            user=self.teacher_profile.user,
        )

        self.student_comment = Comment.objects.create(
            content="student comment content",
            post=self.post,
            user=self.student_profile.user,
        )

        self.comments_detail_url_teacher_comment = reverse("post:comments-detail",
                                                           kwargs={"classroom_id": str(self.classroom1_id),
                                                                   "post_id": str(self.post.id),
                                                                   "comment_id": str(self.teacher_comment.id)})
        self.comments_detail_url_student_comment = reverse("post:comments-detail",
                                                           kwargs={"classroom_id": str(self.classroom1_id),
                                                                   "post_id": str(self.post.id),
                                                                   "comment_id": str(self.student_comment.id)})

    def tearDown(self):
        return super().tearDown()
