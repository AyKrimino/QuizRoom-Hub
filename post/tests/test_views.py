from rest_framework import status

from post.tests.test_views_setup import TestSetup


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


class CommentCreateAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.comments_create_url, data=self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student2_response = self.client.post(self.comments_create_url, data=self.comment_data,
                                             headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.post(self.comments_create_url, data=self.comment_data,
                                             headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        teacher_response = self.client.post(self.comments_create_url, data=self.comment_data,
                                            headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.post(self.comments_create_url, data=self.comment_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(teacher_response.data["user"]["id"]), str(self.teacher_profile.user.id))
        self.assertEqual(str(teacher_response.data["post"]["classroom"]["id"]), str(self.classroom1_id))
        self.assertEqual(str(teacher_response.data["post"]["id"]), str(self.post.id))
        self.assertEqual(str(teacher_response.data["content"]), self.comment_data["content"])
        self.assertEqual(student_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(student_response.data["user"]["id"]), str(self.student_profile.user.id))
        self.assertEqual(str(student_response.data["post"]["classroom"]["id"]), str(self.classroom1_id))
        self.assertEqual(str(student_response.data["post"]["id"]), str(self.post.id))
        self.assertEqual(str(student_response.data["content"]), self.comment_data["content"])

    def test_view_with_authenticated_classroom_member_user_without_data(self):
        response = self.client.post(self.comments_create_url, data={},
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data["content"])


class CommentListAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.comments_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student2_response = self.client.get(self.comments_list_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.comments_list_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        teacher_response = self.client.get(self.comments_list_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.comments_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response.status_code, status.HTTP_200_OK)


class CommentRetrieveAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.comments_detail_url_teacher_comment)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        student2_response = self.client.get(self.comments_detail_url_teacher_comment,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.comments_detail_url_teacher_comment,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student2_response.data["detail"], "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response.data["detail"], "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_users(self):
        teacher_response_teacher_comment = self.client.get(self.comments_detail_url_teacher_comment,
                                                           headers={
                                                               "Authorization": f"Bearer {self.teacher_access_token}"})
        student_response_teacher_comment = self.client.get(self.comments_detail_url_teacher_comment,
                                                           headers={
                                                               "Authorization": f"Bearer {self.student_access_token}"})
        teacher_response_student_comment = self.client.get(self.comments_detail_url_student_comment,
                                                           headers={
                                                               "Authorization": f"Bearer {self.teacher_access_token}"})
        student_response_student_comment = self.client.get(self.comments_detail_url_student_comment,
                                                           headers={
                                                               "Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response_teacher_comment.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response_teacher_comment.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher_response_student_comment.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response_student_comment.status_code, status.HTTP_200_OK)


class CommentUpdateAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response1 = self.client.put(self.comments_detail_url_teacher_comment, data=self.comment_data)
        response2 = self.client.put(self.comments_detail_url_student_comment, data=self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response1.data["detail"], "Authentication credentials were not provided.")
        self.assertEqual(response2.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_comment_author_users(self):
        teacher_response_student_comment = self.client.put(self.comments_detail_url_student_comment,
                                                           data=self.comment_data,
                                                           headers={
                                                               "Authorization": f"Bearer {self.teacher_access_token}"})
        teacher2_response_student_comment = self.client.put(self.comments_detail_url_student_comment,
                                                            data=self.comment_data,
                                                            headers={
                                                                "Authorization": f"Bearer {self.teacher2_access_token}"})
        student_response_teacher_comment = self.client.put(self.comments_detail_url_teacher_comment,
                                                           data=self.comment_data,
                                                           headers={
                                                               "Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response_teacher_comment = self.client.put(self.comments_detail_url_teacher_comment,
                                                            data=self.comment_data,
                                                            headers={
                                                                "Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(teacher_response_student_comment.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher_response_student_comment.data["detail"],
                         "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response_student_comment.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response_student_comment.data["detail"],
                         "You do not have permission to perform this action.")
        self.assertEqual(student_response_teacher_comment.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response_teacher_comment.data["detail"],
                         "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response_teacher_comment.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(teacher2_response_teacher_comment.data["detail"],
                         "You do not have permission to perform this action.")

    def test_view_with_authenticated_comment_author_users(self):
        teacher_response_teacher_comment = self.client.put(self.comments_detail_url_teacher_comment,
                                                           data=self.comment_data,
                                                           headers={
                                                               "Authorization": f"Bearer {self.teacher_access_token}"})
        student_response_student_comment = self.client.put(self.comments_detail_url_student_comment,
                                                           data=self.comment_data,
                                                           headers={
                                                               "Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response_teacher_comment.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response_student_comment.status_code, status.HTTP_200_OK)


class CommentDeleteAPIViewTests(TestSetup):
    def test_view_with_unauthenticated_user(self):
        response_teacher_comment = self.client.delete(self.comments_detail_url_teacher_comment)
        response_student_comment = self.client.delete(self.comments_detail_url_student_comment)
        self.assertEqual(response_teacher_comment.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_student_comment.data["detail"], "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_or_non_comment_author_users(self):
        student_response_teacher_comment = self.client.delete(self.comments_detail_url_teacher_comment,
                                                              headers={
                                                                  "Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(student_response_teacher_comment.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(student_response_teacher_comment.data["detail"],
                         "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        teacher_response_teacher_comment = self.client.delete(self.comments_detail_url_teacher_comment, headers={
            "Authorization": f"Bearer {self.teacher_access_token}"})
        teacher_response_student_comment = self.client.delete(self.comments_detail_url_student_comment, headers={
            "Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(teacher_response_teacher_comment.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(teacher_response_student_comment.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_with_authenticated_comment_author_users(self):
        teacher_response_teacher_comment = self.client.delete(self.comments_detail_url_teacher_comment, headers={
            "Authorization": f"Bearer {self.teacher_access_token}"})
        student_response_student_comment = self.client.delete(self.comments_detail_url_student_comment, headers={
            "Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response_teacher_comment.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(student_response_student_comment.status_code, status.HTTP_204_NO_CONTENT)
