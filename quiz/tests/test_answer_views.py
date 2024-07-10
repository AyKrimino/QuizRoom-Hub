from rest_framework import status

from quiz.tests.test_setup_views import QuizTestSetup


class AnswerCreateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.answers_create_url, data=self.answer_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.post(self.answers_create_url, data=self.answer_data,
                                            headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.post(self.answers_create_url, data=self.answer_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        data = self.answer_data
        response = self.client.post(self.answers_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["is_valid"], data["is_valid"])

    def test_view_with_authenticated_classroom_owner_user_without_data(self):
        response = self.client.post(self.answers_create_url, data={},
                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data["description"])
        self.assertIn("This field is required.", response.data["is_valid"])

    def test_view_with_authenticated_classroom_owner_user_with_invalid_data_type(self):
        data = self.answer_data
        data["is_valid"] = "No"
        response = self.client.post(self.answers_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["is_valid"], "Not a valid boolean.")


class AnswerListAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.answers_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.get(self.answers_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.answers_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.get(self.answers_list_url,
                                   headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnswerRetrieveAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.answers_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.get(self.answers_detail_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.answers_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.get(self.answers_detail_url,
                                   headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.answer.id))


class AnswerUpdateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.put(self.answers_detail_url, data={"description": "test", "is_valid": True})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.put(self.answers_detail_url, data={"description": "test", "is_valid": True},
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.put(self.answers_detail_url, data={"description": "test", "is_valid": True},
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        data = {"description": "test", "is_valid": True}
        response = self.client.put(self.answers_detail_url, data=data,
                                   headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.answer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.answer.description, data["description"])
        self.assertEqual(self.answer.is_valid, data["is_valid"])


class AnswerDestroyAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.answers_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        teacher_response = self.client.delete(self.answers_detail_url,
                                              headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.delete(self.answers_detail_url,
                                              headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.delete(self.answers_detail_url,
                                      headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
