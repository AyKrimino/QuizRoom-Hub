from rest_framework import status

from quiz.tests.test_setup_views import QuizTestSetup


class QuestionCreateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.questions_create_url, data=self.question_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.post(self.questions_create_url, data=self.question_data,
                                            headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.post(self.questions_create_url, data=self.question_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        classroom_owner_response = self.client.post(self.questions_create_url, data=self.question_data,
                                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(classroom_owner_response.status_code, status.HTTP_201_CREATED)

    def test_view_with_authenticated_classroom_owner_user_without_data(self):
        classroom_owner_response = self.client.post(self.questions_create_url,
                                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(classroom_owner_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", classroom_owner_response.data["description"])


class QuestionListAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.questions_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student_response = self.client.get(self.questions_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher_response = self.client.get(self.questions_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        student2_response = self.client.get(self.questions_list_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.questions_list_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher2_response.status_code, status.HTTP_200_OK)


class QuestionRetrieveAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.questions_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student_response = self.client.get(self.questions_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher_response = self.client.get(self.questions_detail_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        student2_response = self.client.get(self.questions_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.questions_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher2_response.status_code, status.HTTP_200_OK)


class QuestionUpdateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.put(self.questions_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.put(self.questions_detail_url, data=self.question_data,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.put(self.questions_detail_url, data=self.question_data,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        classroom_owner_response = self.client.put(self.questions_detail_url, data=self.question_data,
                                                   headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(classroom_owner_response.status_code, status.HTTP_200_OK)
        self.assertEqual(classroom_owner_response.data["description"], self.question_data["description"])


class QuestionDestroyAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.questions_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.delete(self.questions_detail_url,
                                              headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.delete(self.questions_detail_url,
                                              headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        classroom_owner_response = self.client.delete(self.questions_detail_url,
                                                      headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(classroom_owner_response.status_code, status.HTTP_204_NO_CONTENT)
