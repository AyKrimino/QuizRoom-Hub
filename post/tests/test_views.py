from post.tests.test_views_setup import TestSetup
from rest_framework import status


class CoursePostCreateAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.posts_create_url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        student_response = self.client.post(self.posts_create_url, data=self.post_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.post(self.posts_create_url, data=self.post_data,
                                             headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.post(self.posts_create_url, data=self.post_data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["classroom"]["id"], str(self.classroom1_id))
        self.assertEqual(response.data["title"], self.post_data["title"])
        self.assertEqual(response.data["content"], self.post_data["content"])

    def test_view_with_authenticated_classroom_owner_user_without_data(self):
        response = self.client.post(self.posts_create_url, data={},
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data["title"])
        self.assertIn("This field is required.", response.data["content"])


class CoursePostListAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.posts_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student2_response = self.client.get(self.posts_list_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.posts_list_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        teacher_response = self.client.get(self.posts_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.posts_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response.status_code, status.HTTP_200_OK)


class CoursePostRetrieveAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.posts_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student2_response = self.client.get(self.posts_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.posts_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        teacher_response = self.client.get(self.posts_detail_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.posts_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response.status_code, status.HTTP_200_OK)


class CoursePostUpdateAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.put(self.posts_detail_url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        student_response = self.client.put(self.posts_detail_url, data=self.post_data,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.put(self.posts_detail_url, data=self.post_data,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.put(self.posts_detail_url, data=self.post_data,
                                   headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CoursePostDestroyAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.posts_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        student_response = self.client.delete(self.posts_detail_url,
                                              headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.delete(self.posts_detail_url,
                                               headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.delete(self.posts_detail_url,
                                      headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
