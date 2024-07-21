from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APITestCase

from account.models import TeacherProfile, StudentProfile
from classroom.models import Classroom
from quiz.models import Quiz, Question

User = get_user_model()


class TestSetup(APITestCase):
    def setUp(self):
        self.fake = Faker()

        # teacher
        self.teacher_email = self.fake.email()
        self.teacher_password = self.fake.password()
        self.teacher_user = User.objects.create_user(email=self.teacher_email, password=self.teacher_password,
                                                     is_teacher=True)
        self.teacher_profile = TeacherProfile.objects.get(user=self.teacher_user)

        # classroom
        self.classroom_name = self.fake.name()
        self.classroom = Classroom.objects.create(name=self.classroom_name, teacher=self.teacher_profile)

        # Quiz dummy data
        self.quiz_data = {
            "title": self.fake.language_name(),
            "content": self.fake.text(),
            "classroom": self.classroom,
        }

        # quiz
        self.quiz = Quiz.objects.create(title="quiz1", content="content1", classroom=self.classroom)

        # Question dummy data
        self.question_data = {
            "description": self.fake.text(),
            "quiz": self.quiz,
        }

        # question
        self.question = Question.objects.create(description="desc", quiz=self.quiz)

        # Answer dummy data
        self.answer_data = {
            "description": self.fake.text(),
            "is_valid": self.fake.boolean(),
            "question": self.question,
        }

        # student
        self.student_email = self.fake.email()
        self.student_password = self.fake.password()
        self.student_user = User.objects.create_user(email=self.student_email, password=self.student_password,
                                                     is_teacher=False)
        self.student_profile = StudentProfile.objects.get(user=self.student_user)

        # StudentQuiz dummy data
        self.student_quiz_data = {
            "student": self.student_profile,
            "quiz": self.quiz,
            "mark": 14.99,
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
