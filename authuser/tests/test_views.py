from rest_framework import status

from authuser.tests.test_setup import TestSetup


class RegisterUserViewTests(TestSetup):
    def test_register_user_with_valid_data(self):
        self.user_data["password2"] = self.user_data["password"]
        response = self.client.post(self.register_url, self.user_data)
        user = self.User.objects.get(email=self.user_data["email"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_register_user_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["email"][0]), "This field is required.")
        self.assertEqual(str(response.data["password"][0]), "This field is required.")
        self.assertEqual(str(response.data["password2"][0]), "This field is required.")

    def test_register_user_with_invalid_password2(self):
        self.user_data["password2"] = "InvalidPassword2"
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["password"][0]), "password fields didn't match.")

    def test_register_user_with_existing_email(self):
        self.user_data["password2"] = self.user_data["password"]
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["email"][0]), "This field must be unique.")

    def test_register_user_with_weak_password(self):
        self.user_data["password"] = self.user_data["password2"] = "1234"
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This password is too short.", str(response.data["password"]))
        self.assertIn("This password is too common.", str(response.data["password"]))
        self.assertIn("This password is entirely numeric.", str(response.data["password"]))

    def test_register_user_with_invalid_email(self):
        self.user_data["email"] = "invalid-email"
        self.user_data["password2"] = self.user_data["password"]
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["email"][0]), "Enter a valid email address.")


class LoginUserViewTests(TestSetup):
    def test_login_user_with_valid_data(self):
        self.client.post(self.register_url, {**self.user_data, "password2": self.user_data["password"]})
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("tokens" in response.data)
        self.assertTrue("refresh" in response.data["tokens"])
        self.assertTrue("access" in response.data["tokens"])
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_login_user_with_invalid_credentials(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data[0]), "Invalid credentials.")

    def test_login_user_without_email(self):
        response = self.client.post(self.login_url, {"password": self.fake.password()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["email"][0]), "This field is required.")

    def test_login_user_without_password(self):
        response = self.client.post(self.login_url, {"email": self.fake.email()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["password"][0]), "This field is required.")

    def test_login_user_without_password_and_email(self):
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["email"][0]), "This field is required.")
        self.assertEqual(str(response.data["password"][0]), "This field is required.")

    def test_login_user_with_inactive_user(self):
        self.client.post(self.register_url, {**self.user_data, "password2": self.user_data["password"]})
        user = self.User.objects.get(email=self.user_data["email"])
        user.is_active = False
        user.save()
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutUserViewTests(TestSetup):
    def test_logout_user_successfully(self):
        # register user
        self.client.post(self.register_url, {**self.user_data, "password2": self.user_data["password"]})
        # login the user
        response_login = self.client.post(self.login_url, self.user_data)
        refresh_token = response_login.data["tokens"]["refresh"]
        access_token = response_login.data["tokens"]["access"]
        response_logout = self.client.post(self.logout_url, {"refresh": refresh_token},
                                           headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response_logout.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_user_without_refresh_token(self):
        # register user
        self.client.post(self.register_url, {**self.user_data, "password2": self.user_data["password"]})
        # login the user
        response_login = self.client.post(self.login_url, self.user_data)
        access_token = response_login.data["tokens"]["access"]
        response_logout = self.client.post(self.logout_url, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response_logout.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user_without_authorization(self):
        # register user
        self.client.post(self.register_url, {**self.user_data, "password2": self.user_data["password"]})
        # login the user
        response_login = self.client.post(self.login_url, self.user_data)
        refresh_token = response_login.data["tokens"]["refresh"]
        response_logout = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(response_logout.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response_logout.data["detail"]), "Authentication credentials were not provided.")
        self.assertFalse(response_logout.has_header("Authorization"))
