from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse("authuser:register")
        self.login_url = reverse("authuser:login")
        self.logout_url = reverse("authuser:logout")
        self.fake = Faker()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.user_data = {
            "email": self.email,
            "password": self.password,
        }
        self.User = get_user_model()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
