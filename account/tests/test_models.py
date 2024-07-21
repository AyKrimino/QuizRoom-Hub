from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from faker import Faker
from rest_framework.test import APITestCase

from account.models import TeacherProfile, StudentProfile

User = get_user_model()


class TeacherProfileTests(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.user = User.objects.create_user(
            email=self.fake.email(),
            password=self.fake.password(),
            is_teacher=True,
        )
        self.bio = self.fake.text()
        self.birthday = self.fake.date_of_birth(minimum_age=25, maximum_age=90)
        self.experience = 10
        return super().setUp()

    def test_teacher_profile_creation_after_creating_user(self):
        teacher_profile = TeacherProfile.objects.get(user=self.user)
        self.assertIsNotNone(teacher_profile)
        self.assertEqual(teacher_profile.user.id, self.user.id)

    def test_changing_teacher_profile_after_creating_user(self):
        teacher_profile = TeacherProfile.objects.get(user=self.user)
        teacher_profile.bio = self.bio
        teacher_profile.date_of_birth = self.birthday
        teacher_profile.years_of_experience = self.experience
        teacher_profile.save()
        teacher_profile.refresh_from_db()
        self.assertEqual(teacher_profile.bio, self.bio)
        self.assertEqual(teacher_profile.date_of_birth, self.birthday)
        self.assertEqual(teacher_profile.years_of_experience, self.experience)

    def test_student_profile_deletion_when_user_deleted(self):
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(TeacherProfile.DoesNotExist):
            TeacherProfile.objects.get(user_id=user_id)

    def test_creating_multiple_teacher_profiles_with_same_user(self):
        with self.assertRaises(IntegrityError):
            TeacherProfile.objects.create(user=self.user)

    def test_teacher_profile_string_representation(self):
        teacher_profile = TeacherProfile.objects.get(user=self.user)
        self.assertEqual(str(teacher_profile), str(self.user).split("@")[0])


class StudentProfileTests(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.user = User.objects.create_user(
            email=self.fake.email(),
            password=self.fake.password(),
            is_teacher=False,
        )
        self.bio = self.fake.text()
        self.birthday = self.fake.date_of_birth(minimum_age=25, maximum_age=90)
        return super().setUp()

    def test_student_profile_creation_after_creating_user(self):
        student_profile = StudentProfile.objects.get(user=self.user)
        self.assertIsNotNone(student_profile)
        self.assertEqual(student_profile.user.id, self.user.id)

    def test_student_profile_deletion_when_user_deleted(self):
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(StudentProfile.DoesNotExist):
            StudentProfile.objects.get(user_id=user_id)

    def test_changing_student_profile_after_creating_user(self):
        student_profile = StudentProfile.objects.get(user=self.user)
        student_profile.bio = self.bio
        student_profile.date_of_birth = self.birthday
        student_profile.save()
        student_profile.refresh_from_db()
        self.assertEqual(student_profile.bio, self.bio)
        self.assertEqual(student_profile.date_of_birth, self.birthday)

    def test_creating_multiple_student_profiles_with_same_user(self):
        with self.assertRaises(IntegrityError):
            StudentProfile.objects.create(user=self.user)

    def test_student_profile_string_representation(self):
        student_profile = StudentProfile.objects.get(user=self.user)
        self.assertEqual(str(student_profile), str(self.user).split("@")[0])
