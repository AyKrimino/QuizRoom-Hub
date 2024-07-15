from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from account.models import TeacherProfile, StudentProfile
from classroom.models import Classroom, StudentClassroom
from post.models import CoursePost

User = get_user_model()


class TestSetup(APITestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(
            email="teacher@teacher.com",
            password="Django123",
            is_teacher=True,
        )
        self.teacher_profile = TeacherProfile.objects.get(
            user=self.teacher_user,
        )

        self.student_user = User.objects.create_user(
            email="a@student.com",
            password="Django123",
            is_teacher=False,
        )
        self.student_profile = StudentProfile.objects.get(
            user=self.student_user,
        )

        self.classroom = Classroom.objects.create(
            name="classroom",
            teacher=self.teacher_profile,
        )

        self.student_classroom = StudentClassroom.objects.create(
            student=self.student_profile,
            classroom=self.classroom,
        )

        self.course_post_data = {
            "title": "title",
            "content": "content test",
            "classroom": self.classroom,
        }

        self.post = CoursePost.objects.create(**{"title": "t1", "content": "content t1", "classroom": self.classroom})

        self.comment_data = {
            "content": "content test",
            "post": self.post,
            "user": self.teacher_user,
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
