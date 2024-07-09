from rest_framework import status

from quiz.tests.test_setup_views import QuizTestSetup


class QuizCreateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.quizzes_create_url, data=self.quiz_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_user(self):
        teacher2_response = self.client.post(self.quizzes_create_url, data=self.quiz_data,
                                             headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        student_response = self.client.post(self.quizzes_create_url, data=self.quiz_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.post(self.quizzes_create_url, data=self.quiz_data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["classroom_id"], self.quiz_data["classroom_id"])
        self.assertEqual(response.data["title"], self.quiz_data["title"])
        self.assertEqual(response.data["content"], self.quiz_data["content"])

    def test_view_with_authenticated_classroom_owner_with_invalid_classroom_id(self):
        data = self.quiz_data
        data["classroom_id"] = self.fake.uuid4()
        response = self.client.post(self.quizzes_create_url, data=self.quiz_data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Classroom does not exist", response.data)

    def test_view_with_authenticated_classroom_owner_without_classroom_id(self):
        data = self.quiz_data
        del data["classroom_id"]

        response = self.client.post(self.quizzes_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("classroom_id is required.", response.data["non_field_errors"])

    def test_view_with_authenticated_classroom_owner_without_data(self):
        response = self.client.post(self.quizzes_create_url, data={},
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data["title"])


class QuizListAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.quizzes_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_user(self):
        student_response = self.client.get(self.quizzes_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_teacher_user(self):
        teacher_response = self.client.get(self.quizzes_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        teacher2_response = self.client.get(self.quizzes_list_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher2_response.status_code, status.HTTP_200_OK)


class QuizRetrieveAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.quizzes_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        teacher_response = self.client.get(self.quizzes_detail_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.quizzes_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_members(self):
        teacher2_response = self.client.get(self.quizzes_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        student2_response = self.client.get(self.quizzes_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        self.assertEqual(teacher2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student2_response.status_code, status.HTTP_200_OK)


class QuizUpdateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        data = self.quiz_data
        data["content"] = "new content"
        response = self.client.put(self.quizzes_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        data = self.quiz_data
        data["content"] = "new content"
        teacher_response = self.client.put(self.quizzes_detail_url, data=data,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.put(self.quizzes_detail_url, data=data,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        data = self.quiz_data
        data["content"] = "new content"
        classroom_owner_response = self.client.put(self.quizzes_detail_url, data=data,
                                                   headers={"Authorization": f"Bearer {self.teacher2_access_token}"}, )
        self.assertEqual(classroom_owner_response.status_code, status.HTTP_200_OK)
        self.assertEqual(classroom_owner_response.data["content"], data["content"])


class QuizDestroyAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.quizzes_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        teacher_response = self.client.delete(self.quizzes_detail_url,
                                              headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.delete(self.quizzes_detail_url,
                                              headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        classroom_owner_response = self.client.delete(self.quizzes_detail_url,
                                                      headers={
                                                          "Authorization": f"Bearer {self.teacher2_access_token}"}, )
        self.assertEqual(classroom_owner_response.status_code, status.HTTP_204_NO_CONTENT)
