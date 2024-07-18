from classroom.tests.test_setup import TestSetUp
from django.urls import reverse
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

        # self.comments_create_url = reverse("post:comments-create")
        # self.comments_list_url = reverse("post:comments-list")
        # self.comments_detail_url = reverse("post:comments-list")

    def tearDown(self):
        return super().tearDown()
