from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from ..models import TeacherProfile, StudentProfile

User = get_user_model()


class TestSetup(APITestCase):
    def setUp(self):
        self.fake = Faker()

        self.register_url = reverse("authuser:register")
        self.login_url = reverse("authuser:login")
        self.logout_url = reverse("authuser:logout")
        self.teachers_list_url = reverse("account:teachers-list")
        self.students_list_url = reverse("account:students-list")

        # Admin user
        self.admin_email = self.fake.email()
        self.admin_password = self.fake.password()
        self.admin = User.objects.create_superuser(email=self.admin_email, password=self.admin_password)
        self.login_admin_response = self.client.post(self.login_url,
                                                     {"email": self.admin_email, "password": self.admin_password})
        self.admin_access_token = self.login_admin_response.data["tokens"]["access"]
        self.admin_refresh_token = self.login_admin_response.data["tokens"]["refresh"]

        # Teacher user
        self.teacher_email = self.fake.email()
        self.teacher_password = self.fake.password()
        self.teacher = User.objects.create_user(email=self.teacher_email, password=self.teacher_password,
                                                is_teacher=True)
        self.teacher_profile = TeacherProfile.objects.get(user=self.teacher)
        self.teachers_detail_url = reverse("account:teachers-detail", kwargs={"pk": self.teacher_profile.id})
        self.login_teacher_response = self.client.post(self.login_url,
                                                       {"email": self.teacher_email, "password": self.teacher_password})
        self.teacher_access_token = self.login_teacher_response.data["tokens"]["access"]
        self.teacher_refresh_token = self.login_teacher_response.data["tokens"]["refresh"]

        # Teacher user 2
        self.teacher2_email = self.fake.email()
        self.teacher2_password = self.fake.password()
        self.teacher2 = User.objects.create_user(email=self.teacher2_email, password=self.teacher2_password,
                                                 is_teacher=True)
        self.teacher2_profile = TeacherProfile.objects.get(user=self.teacher2)
        self.teachers2_detail_url = reverse("account:teachers-detail", kwargs={"pk": self.teacher2_profile.id})
        self.login_teacher2_response = self.client.post(self.login_url,
                                                        {"email": self.teacher2_email,
                                                         "password": self.teacher2_password})
        self.teacher2_access_token = self.login_teacher2_response.data["tokens"]["access"]
        self.teacher2_refresh_token = self.login_teacher2_response.data["tokens"]["refresh"]

        # Teacher user 3
        self.teacher3_email = self.fake.email()
        self.teacher3_password = self.fake.password()
        self.teacher3 = User.objects.create_user(email=self.teacher3_email, password=self.teacher3_password,
                                                 is_teacher=True)
        self.teacher3_profile = TeacherProfile.objects.get(user=self.teacher3)
        self.login_teacher3_response = self.client.post(self.login_url,
                                                        {"email": self.teacher3_email,
                                                         "password": self.teacher3_password})
        self.teacher3_access_token = self.login_teacher3_response.data["tokens"]["access"]
        self.teacher3_refresh_token = self.login_teacher3_response.data["tokens"]["refresh"]

        # Student user
        self.student_email = self.fake.email()
        self.student_password = self.fake.password()
        self.student = User.objects.create_user(email=self.student_email, password=self.student_password,
                                                is_teacher=False)
        self.student_profile = StudentProfile.objects.get(user=self.student)
        self.students_detail_url = reverse("account:students-detail", kwargs={"pk": self.student_profile.id})
        self.login_student_response = self.client.post(self.login_url,
                                                       {"email": self.student_email, "password": self.student_password})
        self.student_access_token = self.login_student_response.data["tokens"]["access"]
        self.student_refresh_token = self.login_student_response.data["tokens"]["refresh"]

        # Student user 2
        self.student2_email = self.fake.email()
        self.student2_password = self.fake.password()
        self.student2 = User.objects.create_user(email=self.student2_email, password=self.student2_password,
                                                 is_teacher=False)
        self.student2_profile = StudentProfile.objects.get(user=self.student2)
        self.students2_detail_url = reverse("account:students-detail", kwargs={"pk": self.student2_profile.id})
        self.login_student2_response = self.client.post(self.login_url,
                                                        {"email": self.student2_email,
                                                         "password": self.student2_password})
        self.student2_access_token = self.login_student2_response.data["tokens"]["access"]
        self.student2_refresh_token = self.login_student2_response.data["tokens"]["refresh"]

        # Student user 3
        self.student3_email = self.fake.email()
        self.student3_password = self.fake.password()
        self.student3 = User.objects.create_user(email=self.student3_email, password=self.student3_password,
                                                 is_teacher=False)
        self.student3_profile = StudentProfile.objects.get(user=self.student3)
        self.login_student3_response = self.client.post(self.login_url,
                                                        {"email": self.student3_email,
                                                         "password": self.student3_password})
        self.student3_access_token = self.login_student3_response.data["tokens"]["access"]
        self.student3_refresh_token = self.login_student3_response.data["tokens"]["refresh"]

        return super().setUp()

    def tearDown(self):
        self.client.post(self.logout_url, {"refresh": self.admin_refresh_token},
                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.client.post(self.logout_url, {"refresh": self.teacher_refresh_token},
                         headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.client.post(self.logout_url, {"refresh": self.student_refresh_token},
                         headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.client.post(self.logout_url, {"refresh": self.teacher2_refresh_token},
                         headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.client.post(self.logout_url, {"refresh": self.student2_refresh_token},
                         headers={"Authorization": f"Bearer {self.student2_access_token}"})
        return super().tearDown()

    def get_dummy_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        return file
