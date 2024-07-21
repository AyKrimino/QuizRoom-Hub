from rest_framework import status

from account.tests.test_setup import TestSetup


class TeacherProfileListAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.teachers_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_admin_user(self):
        teacher_response = self.client.get(self.teachers_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.teachers_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})

        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(teacher_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(student_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_admin_user(self):
        response = self.client.get(self.teachers_list_url,
                                   headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_with_not_allowed_http_methods(self):
        post_response = self.client.post(self.teachers_list_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        put_response = self.client.put(self.teachers_list_url,
                                       headers={"Authorization": f"Bearer {self.admin_access_token}"})
        patch_response = self.client.patch(self.teachers_list_url,
                                           headers={"Authorization": f"Bearer {self.admin_access_token}"})
        delete_response = self.client.delete(self.teachers_list_url,
                                             headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(post_response.data["detail"]), "Method \"POST\" not allowed.")
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(put_response.data["detail"]), "Method \"PUT\" not allowed.")
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(patch_response.data["detail"]), "Method \"PATCH\" not allowed.")
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(delete_response.data["detail"]), "Method \"DELETE\" not allowed.")


class TeacherProfileRetrieveAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.teachers_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_profile_owner_users(self):
        admin_response = self.client.get(self.teachers_detail_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        student_response = self.client.get(self.teachers_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.get(self.teachers_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher2_response.status_code, status.HTTP_200_OK)

    def test_view_with_authenticated_teacher_profile_owner_user(self):
        response = self.client.get(self.teachers_detail_url,
                                   headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeacherProfileUpdateAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.put(self.teachers_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_profile_owner_users(self):
        admin_response = self.client.put(self.teachers_detail_url, data={},
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        student_response = self.client.put(self.teachers_detail_url, data={},
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.put(self.teachers_detail_url, data={},
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(admin_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(student_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(teacher2_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_teacher_profile_owner(self):
        data = {"user_first_name": self.fake.first_name(), "user_last_name": self.fake.last_name(),
                "bio": self.fake.text(), "profile_picture": self.get_dummy_image()}
        response = self.client.put(self.teachers_detail_url, data=data, format='multipart',
                                   HTTP_AUTHORIZATION=f"Bearer {self.teacher_access_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_with_authenticated_teacher_profile_owner_with_invalid_data_attributes(self):
        data = {"invalid_attribute": True, "bio": "test"}
        response = self.client.put(self.teachers_detail_url, data=data,
                                   HTTP_AUTHORIZATION=f"Bearer {self.teacher_access_token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_with_authenticated_teacher_profile_owner_with_invalid_attribute_data_types(self):
        data = {"bio": True, "user_first_name": False, "years_of_experience": "hello world",
                "date_of_birth": "wrong_data"}
        response = self.client.put(self.teachers_detail_url, data=data,
                                   HTTP_AUTHORIZATION=f"Bearer {self.teacher_access_token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bio", response.data)
        self.assertIn("user_first_name", response.data)
        self.assertIn("years_of_experience", response.data)
        self.assertIn("date_of_birth", response.data)


class TeacherProfileDestroyAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.teachers_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_profile_owner_users(self):
        admin_response = self.client.delete(self.teachers_detail_url,
                                            headers={"Authorization": f"Bearer {self.admin_access_token}"})
        student_response = self.client.delete(self.teachers_detail_url,
                                              headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.delete(self.teachers_detail_url,
                                               headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(admin_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(student_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(teacher2_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_teacher_profile_owner(self):
        response = self.client.delete(self.teachers_detail_url,
                                      HTTP_AUTHORIZATION=f"Bearer {self.teacher_access_token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# student tests
class StudentProfileListAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.students_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_admin_user(self):
        teacher_response = self.client.get(self.students_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.teachers_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})

        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(teacher_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(student_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_admin_user(self):
        response = self.client.get(self.students_list_url,
                                   headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_with_not_allowed_http_methods(self):
        post_response = self.client.post(self.students_list_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        put_response = self.client.put(self.students_list_url,
                                       headers={"Authorization": f"Bearer {self.admin_access_token}"})
        patch_response = self.client.patch(self.students_list_url,
                                           headers={"Authorization": f"Bearer {self.admin_access_token}"})
        delete_response = self.client.delete(self.students_list_url,
                                             headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(post_response.data["detail"]), "Method \"POST\" not allowed.")
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(put_response.data["detail"]), "Method \"PUT\" not allowed.")
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(patch_response.data["detail"]), "Method \"PATCH\" not allowed.")
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str(delete_response.data["detail"]), "Method \"DELETE\" not allowed.")


class StudentProfileRetrieveAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.students_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_student_profile_owner_users(self):
        admin_response = self.client.get(self.students_detail_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        teacher_response = self.client.get(self.students_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        student2_response = self.client.get(self.students_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student2_response.status_code, status.HTTP_200_OK)

    def test_view_with_authenticated_student_profile_owner_user(self):
        response = self.client.get(self.students_detail_url,
                                   headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentProfileUpdateAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.put(self.students_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_student_profile_owner_users(self):
        admin_response = self.client.put(self.students_detail_url, data={},
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        teacher_response = self.client.put(self.students_detail_url, data={},
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student2_response = self.client.put(self.students_detail_url, data={},
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(admin_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(teacher_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(student2_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_student_profile_owner(self):
        data = {"user_first_name": self.fake.first_name(), "user_last_name": self.fake.last_name(),
                "bio": self.fake.text(), "profile_picture": self.get_dummy_image()}
        response = self.client.put(self.students_detail_url, data=data, format='multipart',
                                   HTTP_AUTHORIZATION=f"Bearer {self.student_access_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_with_authenticated_student_profile_owner_with_invalid_data_attributes(self):
        data = {"invalid_attribute": True, "bio": "test"}
        response = self.client.put(self.students_detail_url, data=data,
                                   HTTP_AUTHORIZATION=f"Bearer {self.student_access_token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_with_authenticated_student_profile_owner_with_invalid_attribute_data_types(self):
        data = {"bio": True, "user_first_name": False, "date_of_birth": "wrong_data"}
        response = self.client.put(self.students_detail_url, data=data,
                                   HTTP_AUTHORIZATION=f"Bearer {self.student_access_token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bio", response.data)
        self.assertIn("user_first_name", response.data)
        self.assertIn("date_of_birth", response.data)


class StudentProfileDestroyAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.students_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_student_profile_owner_users(self):
        admin_response = self.client.delete(self.students_detail_url,
                                            headers={"Authorization": f"Bearer {self.admin_access_token}"})
        teacher_response = self.client.delete(self.students_detail_url,
                                              headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student2_response = self.client.delete(self.students_detail_url,
                                               headers={"Authorization": f"Bearer {self.student2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(admin_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(teacher_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(student2_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_student_profile_owner(self):
        response = self.client.delete(self.students_detail_url,
                                      HTTP_AUTHORIZATION=f"Bearer {self.student_access_token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
