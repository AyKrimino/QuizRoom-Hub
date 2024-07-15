from post.models import CoursePost, Comment
from post.tests.test_models_setup import TestSetup


class CoursePostTests(TestSetup):
    def test_create_post_with_manager(self):
        CoursePost.objects.create(**self.course_post_data)
        post = CoursePost.objects.get(**self.course_post_data)
        self.assertEqual(post.title, self.course_post_data["title"])
        self.assertEqual(post.content, self.course_post_data["content"])
        self.assertEqual(post.classroom, self.course_post_data["classroom"])

    def test_create_post_without_manager(self):
        post = CoursePost(**self.course_post_data)
        post.save()
        post.refresh_from_db()
        self.assertEqual(post.title, self.course_post_data["title"])
        self.assertEqual(post.content, self.course_post_data["content"])
        self.assertEqual(post.classroom, self.course_post_data["classroom"])

    def test_update_post(self):
        post = CoursePost(**self.course_post_data)
        post.save()
        post.refresh_from_db()
        post.title = "new title"
        post.save()
        post.refresh_from_db()
        self.assertEqual(post.title, "new title")
        self.assertEqual(post.content, self.course_post_data["content"])
        self.assertEqual(post.classroom, self.course_post_data["classroom"])

    def test_delete_post(self):
        post = CoursePost(**self.course_post_data)
        post.save()
        post.refresh_from_db()
        post.delete()
        self.classroom.refresh_from_db()
        self.assertFalse(CoursePost.objects.filter(**self.course_post_data).exists())
        self.assertIsNotNone(self.classroom)

    def test_delete_classroom_related_to_post(self):
        post = CoursePost(**self.course_post_data)
        post.save()
        post.refresh_from_db()
        self.classroom.delete()
        self.assertFalse(CoursePost.objects.filter(title=self.course_post_data["title"]).exists())

    def test_post_string_representation(self):
        post = CoursePost(**self.course_post_data)
        post.save()
        post.refresh_from_db()
        self.assertEqual(str(post), f"{post.title}-{post.classroom.name}")


class CommentTests(TestSetup):
    def test_create_comment_with_manager(self):
        Comment.objects.create(**self.comment_data)
        comment = Comment.objects.get(**self.comment_data)
        self.assertEqual(comment.content, self.comment_data["content"])
        self.assertEqual(comment.post, self.comment_data["post"])
        self.assertEqual(comment.user, self.comment_data["user"])

    def test_create_comment_without_manager(self):
        comment = Comment(**self.comment_data)
        comment.save()
        comment.refresh_from_db()
        self.assertEqual(comment.content, self.comment_data["content"])
        self.assertEqual(comment.post, self.comment_data["post"])
        self.assertEqual(comment.user, self.comment_data["user"])

    def test_create_comments_with_teacher_and_student_users(self):
        comment_with_teacher_user = Comment.objects.create(
            content="test teacher",
            post=self.post,
            user=self.teacher_user,
        )
        comment_with_student_user = Comment.objects.create(
            content="test student",
            post=self.post,
            user=self.student_user,
        )
        self.assertEqual(comment_with_teacher_user.content, "test teacher")
        self.assertEqual(comment_with_teacher_user.post, self.post)
        self.assertEqual(comment_with_teacher_user.user, self.teacher_user)
        self.assertEqual(comment_with_student_user.content, "test student")
        self.assertEqual(comment_with_student_user.post, self.post)
        self.assertEqual(comment_with_student_user.user, self.student_user)

    def test_update_comment(self):
        comment = Comment.objects.create(**self.comment_data)
        comment.content = "new comment content"
        comment.save()
        comment.refresh_from_db()
        self.assertEqual(comment.content, "new comment content")

    def test_delete_comment(self):
        comment = Comment.objects.create(**self.comment_data)
        comment.delete()
        self.assertFalse(Comment.objects.filter(**self.comment_data).exists())

    def test_delete_user_related_to_comment(self):
        Comment.objects.create(
            content="comment1 test",
            post=self.post,
            user=self.teacher_user,
        )
        self.teacher_user.delete()
        self.assertFalse(Comment.objects.filter(content="comment1 test", post=self.post).exists())

    def test_delete_post_related_to_comment(self):
        Comment.objects.create(
            content="comment1 test",
            post=self.post,
            user=self.teacher_user,
        )
        self.post.delete()
        self.assertFalse(Comment.objects.filter(content="comment1 test", user=self.teacher_user).exists())

    def test_delete_classroom_related_to_comment(self):
        Comment.objects.create(
            content="comment1 test",
            post=self.post,
            user=self.teacher_user,
        )
        self.classroom.delete()
        self.assertFalse(Comment.objects.filter(content="comment1 test", user=self.teacher_user).exists())

    def test_comment_string_representation(self):
        comment = Comment(**self.comment_data)
        comment.save()
        comment.refresh_from_db()
        self.assertEqual(str(comment), f"{comment.content[:10]}...")
