from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from faker import Faker
from rest_framework.test import APITestCase


class UserManagerTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.fake = Faker()
        self.email = self.fake.email()
        self.password = self.fake.password()
        return super().setUp()

    def test_create_user_with_email_password(self):
        user = self.User.objects.create_user(email=self.email, password=self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_teacher)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as cm:
            self.User.objects.create_user(email=None, password=self.password)
        self.assertEqual(str(cm.exception), "Users must have an email address")

    def test_create_user_without_password(self):
        user = self.User.objects.create_user(email=self.email)
        self.assertFalse(user.has_usable_password())

    def test_create_user_without_data(self):
        with self.assertRaises(TypeError) as cm:
            self.User.objects.create_user()
        self.assertEqual(str(cm.exception), "UserManager.create_user() missing 1 required positional argument: 'email'")

    def test_create_user_with_existing_email(self):
        self.User.objects.create_user(email=self.email, password=self.password)
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(email=self.email, password="Fake123")

    def test_create_user_with_is_teacher_true(self):
        user = self.User.objects.create_user(email=self.email, password=self.password, is_teacher=True)
        self.assertTrue(user.is_teacher)
        self.assertTrue(hasattr(user, "teacher_profile"))
        self.assertFalse(hasattr(user, "student_profile"))

    def test_create_user_with_is_teacher_false(self):
        user = self.User.objects.create_user(email=self.email, password=self.password, is_teacher=False)
        self.assertFalse(user.is_teacher)
        self.assertTrue(hasattr(user, "student_profile"))
        self.assertFalse(hasattr(user, "teacher_profile"))

    def test_create_superuser_with_email_password(self):
        user = self.User.objects.create_superuser(email=self.email, password=self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_teacher)
        self.assertIsNone(user.username)

    def test_create_superuser_without_email(self):
        with self.assertRaises(ValueError) as cm:
            self.User.objects.create_superuser(email=None, password=self.password)
        self.assertEqual(str(cm.exception), "Users must have an email address")

    def test_create_superuser_without_password(self):
        user = self.User.objects.create_superuser(email=self.email)
        self.assertFalse(user.has_usable_password())

    def test_create_superuser_without_data(self):
        with self.assertRaises(TypeError) as cm:
            self.User.objects.create_superuser()
        self.assertEqual(str(cm.exception), "UserManager.create_superuser() missing 1 required positional argument: "
                                            "'email'")

    def test_create_superuser_with_existing_email(self):
        self.User.objects.create_superuser(email=self.email, password=self.password)
        with self.assertRaises(IntegrityError):
            self.User.objects.create_superuser(email=self.email, password=self.password)

    def test_create_superuser_with_is_teacher_true(self):
        user = self.User.objects.create_superuser(email=self.email, password=self.password, is_teacher=True)
        self.assertTrue(user.is_teacher)
        self.assertFalse(hasattr(user, "teacher_profile"))

    def test_create_superuser_with_is_teacher_false(self):
        user = None
        with self.assertRaises(ValueError) as cm:
            user = self.User.objects.create_superuser(email=self.email, password=self.password, is_teacher=False)
        self.assertEqual(str(cm.exception), "Superuser must have is_teacher=True.")
        self.assertFalse(hasattr(user, "student_profile"))

    def test_create_superuser_with_is_staff_false(self):
        with self.assertRaises(ValueError) as cm:
            self.User.objects.create_superuser(email=self.email, password=self.password, is_staff=False)
        self.assertEqual(str(cm.exception), "Superuser must have is_staff=True.")

    def test_create_superuser_with_is_superuser_false(self):
        with self.assertRaises(ValueError) as cm:
            self.User.objects.create_superuser(email=self.email, password=self.password, is_superuser=False)
        self.assertEqual(str(cm.exception), "Superuser must have is_superuser=True.")
