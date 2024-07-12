from quiz.tests.test_setup_views import QuizTestSetup
from rest_framework import status


class StudentAnswerCreateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.student_answer_create_url, data=self.student_answer_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_student_member_users(self):
        teacher_response = self.client.post(self.student_answer_create_url, data=self.student_answer_data,
                                            headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        teacher2_response = self.client.post(self.student_answer_create_url, data=self.student_answer_data,
                                             headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        student_response = self.client.post(self.student_answer_create_url, data=self.student_answer_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_student_member_user(self):
        response = self.client.post(self.student_answer_create_url, data=self.student_answer_data,
                                    headers={"Authorization": f"Bearer {self.student2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["student"]["id"], str(self.student2_profile.id))
        self.assertEqual(response.data["answer"]["id"], str(self.answer.id))


class StudentQuizCreateAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.student_quiz_create_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_student_member_users(self):
        teacher_response = self.client.post(self.student_quiz_create_url, data={},
                                            headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        teacher2_response = self.client.post(self.student_quiz_create_url, data={},
                                             headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        student_response = self.client.post(self.student_quiz_create_url, data={},
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_student_member_user(self):
        response = self.client.post(self.student_quiz_create_url, data={},
                                    headers={"Authorization": f"Bearer {self.student2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentQuizListAPIViewTests(QuizTestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.student_quiz_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student_response = self.client.get(self.student_quiz_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher_response = self.client.get(self.student_quiz_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(student_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        student2_response = self.client.get(self.student_quiz_list_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.student_quiz_list_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher2_response.status_code, status.HTTP_200_OK)



