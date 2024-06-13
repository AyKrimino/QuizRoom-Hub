import datetime

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from faker import Faker
from rest_framework.test import APITestCase


class UserModelTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.fake = Faker()
        self.email = self.fake.email()
        self.password = self.fake.password()
        return super().setUp()

    def test_default_values(self):
        user = self.User.objects.create_user(email=self.email, password=self.password)
        self.assertFalse(user.is_teacher)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_email_uniqueness(self):
        self.User.objects.create_user(email=self.email, password=self.password)
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(email=self.email, password=self.password)

    def test_email_normalization(self):
        email = "tesst@TEST.COM"
        user = self.User.objects.create_user(email=email, password=self.password)
        self.assertEqual(user.email, email.lower())

    def test_str_representation(self):
        user = self.User.objects.create_user(email=self.email, password=self.password)
        self.assertEqual(str(user), self.email)

    def test_date_joined(self):
        user = self.User.objects.create_user(email=self.email, password=self.password)
        date_joined = user.date_joined
        date_now = datetime.datetime.now(tz=datetime.timezone.utc)
        self.assertTrue(date_now - date_joined < datetime.timedelta(seconds=1))
