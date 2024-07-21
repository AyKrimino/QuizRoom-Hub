from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from faker import Faker
from rest_framework.test import APITestCase

from account.models import TeacherProfile, StudentProfile
from classroom.models import Classroom, StudentClassroom

User = get_user_model()


class ClassroomTests(APITestCase):

    def setUp(self):
        self.fake = Faker()
        self.name = self.fake.name()
        self.name2 = self.fake.name()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.user = User.objects.create_user(email=self.email, password=self.password, is_teacher=True)
        self.teacher = TeacherProfile.objects.get(user=self.user)
        return super().setUp()

    def test_create_classroom_with_manager(self):
        Classroom.objects.create(
            name=self.name,
            teacher=self.teacher,
        )
        classroom = Classroom.objects.get(teacher=self.teacher)
        self.assertIsNotNone(classroom)
        self.assertEqual(classroom.name, self.name)
        self.assertEqual(classroom.teacher, self.teacher)

    def test_create_classroom_without_manager(self):
        classroom = Classroom(
            name=self.name,
            teacher=self.teacher,
        )
        classroom.save()
        classroom.refresh_from_db()
        self.assertEqual(classroom.name, self.name)
        self.assertEqual(classroom.teacher, self.teacher)

    def test_create_classroom_without_teacher_field(self):
        with self.assertRaises(IntegrityError):
            Classroom.objects.create(name=self.name)

    def test_create_classroom_without_name_fields(self):
        with self.assertRaises(ValueError) as cm:
            Classroom.objects.create(teacher=self.teacher)
        self.assertEqual(str(cm.exception), "The name field cannot be blank or null.")

    def test_teacher_can_create_multiple_classrooms(self):
        classroom1 = Classroom.objects.create(name=self.name, teacher=self.teacher)
        classroom2 = Classroom.objects.create(name=self.name2, teacher=self.teacher)
        self.assertEqual(classroom1.name, self.name)
        self.assertEqual(classroom2.name, self.name2)
        self.assertEqual(classroom1.teacher, self.teacher)
        self.assertEqual(classroom2.teacher, self.teacher)
        self.assertIn(classroom1, self.teacher.classrooms.all())
        self.assertIn(classroom2, self.teacher.classrooms.all())

    def test_classroom_string_representation(self):
        classroom = Classroom.objects.create(name=self.name, teacher=self.teacher)
        self.assertEqual(str(classroom), self.name)


class StudentClassroomTests(APITestCase):
    def setUp(self):
        self.fake = Faker()

        # teacher
        self.teacher_email = self.fake.email()
        self.teacher_password = self.fake.password()
        self.teacher_user = User.objects.create_user(email=self.teacher_email, password=self.teacher_password,
                                                     is_teacher=True)
        self.teacher = TeacherProfile.objects.get(user=self.teacher_user)
        # classroom
        self.classroom_name = self.fake.name()
        self.classroom_name2 = self.fake.name()
        self.classroom = Classroom.objects.create(name=self.classroom_name, teacher=self.teacher)
        self.classroom2 = Classroom.objects.create(name=self.classroom_name2, teacher=self.teacher)
        # student
        self.student_email = self.fake.email()
        self.student_password = self.fake.password()
        self.student_email2 = self.fake.email()
        self.student_password2 = self.fake.password()
        self.student_user = User.objects.create_user(email=self.student_email, password=self.student_password)
        self.student = StudentProfile.objects.get(user=self.student_user)
        self.student_user2 = User.objects.create_user(email=self.student_email2, password=self.student_password2)
        self.student2 = StudentProfile.objects.get(user=self.student_user2)

        return super().setUp()

    def test_create_student_classroom_with_manager(self):
        StudentClassroom.objects.create(
            student=self.student,
            classroom=self.classroom
        )
        student_classroom = StudentClassroom.objects.get(student=self.student, classroom=self.classroom)
        self.assertIsNotNone(student_classroom)
        self.assertEqual(student_classroom.student, self.student)
        self.assertEqual(student_classroom.classroom, self.classroom)

    def test_create_student_classroom_without_manager(self):
        student_classroom = StudentClassroom(
            student=self.student,
            classroom=self.classroom,
        )
        student_classroom.save()
        student_classroom.refresh_from_db()
        self.assertEqual(student_classroom.student, self.student)
        self.assertEqual(student_classroom.classroom, self.classroom)

    def test_create_student_classroom_without_student(self):
        with self.assertRaises(IntegrityError):
            StudentClassroom.objects.create(classroom=self.classroom)

    def test_create_student_classroom_without_classroom(self):
        with self.assertRaises(IntegrityError):
            StudentClassroom.objects.create(student=self.student)

    def test_create_student_classroom_without_student_and_classroom(self):
        with self.assertRaises(IntegrityError):
            StudentClassroom.objects.create()

    def test_create_student_classroom_with_multiple_students_and_classrooms(self):
        student_classroom1 = StudentClassroom.objects.create(
            student=self.student,
            classroom=self.classroom,
        )
        student_classroom2 = StudentClassroom.objects.create(
            student=self.student2,
            classroom=self.classroom,
        )
        student_classroom3 = StudentClassroom.objects.create(
            student=self.student,
            classroom=self.classroom2,
        )
        self.assertEqual(student_classroom1.student, self.student)
        self.assertEqual(student_classroom1.classroom, self.classroom)
        self.assertEqual(student_classroom2.student, self.student2)
        self.assertEqual(student_classroom2.classroom, self.classroom)
        self.assertEqual(student_classroom3.student, self.student)
        self.assertEqual(student_classroom3.classroom, self.classroom2)

    def test_create_student_classroom_without_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            StudentClassroom.objects.create(student=self.student, classroom=self.classroom)
            StudentClassroom.objects.create(student=self.student, classroom=self.classroom)

    def test_create_student_classroom_string_representation(self):
        student_classroom = StudentClassroom.objects.create(student=self.student, classroom=self.classroom)
        self.assertEqual(str(student_classroom), f"{self.student}-{self.classroom.name}")
