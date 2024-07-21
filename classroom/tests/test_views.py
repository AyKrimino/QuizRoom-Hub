from rest_framework import status

from classroom.models import Classroom, StudentClassroom
from classroom.tests.test_setup import TestSetUp


class ClassroomCreateAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.classrooms_create_url, data=self.classroom_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_user(self):
        response_admin = self.client.post(self.classrooms_create_url, data=self.classroom_data,
                                          headers={"Authorization": f"Bearer {self.admin_access_token}"})
        response_student = self.client.post(self.classrooms_create_url, data=self.classroom_data,
                                            headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response_admin.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_student.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response_admin.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_student.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_teacher_user(self):
        data = self.classroom_data
        response = self.client.post(self.classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Classroom.objects.filter(name=data["name"]).exists())

    def test_view_with_authenticated_teacher_user_with_empty_data(self):
        response = self.client.post(self.classrooms_create_url, data={},
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["name"][0]), "This field is required.")

    def test_view_with_authenticated_teacher_user_with_invalid_attributes(self):
        data = self.classroom_data
        data["invalid_attribute"] = True
        response = self.client.post(self.classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_fields", response.data)
        self.assertIn("invalid_attribute", response.data["invalid_fields"])

    def test_view_with_authenticated_teacher_user_with_invalid_data_type(self):
        data = {"name": False}
        response = self.client.post(self.classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("Not a valid string.", response.data["name"])


class ClassroomListAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.classrooms_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_user(self):
        response_admin = self.client.get(self.classrooms_list_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        response_student = self.client.get(self.classrooms_list_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response_admin.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_student.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response_admin.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_student.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_teacher_user(self):
        response = self.client.get(self.classrooms_list_url,
                                   headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ClassroomRetrieveAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.classrooms_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_users(self):
        response_admin = self.client.get(self.classrooms_detail_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        response_student2 = self.client.get(self.classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        response_teacher2 = self.client.get(self.classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response_admin.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_student2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_teacher2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response_admin.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_student2.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_teacher2.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_user(self):
        response_teacher = self.client.get(self.classrooms_detail_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        response_student = self.client.get(self.classrooms_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response_teacher.status_code, status.HTTP_200_OK)
        self.assertEqual(response_student.status_code, status.HTTP_200_OK)
        self.assertEqual(response_teacher.data["id"], str(self.classroom1.id))
        self.assertEqual(response_student.data["id"], str(self.classroom1.id))


class ClassroomUpdateAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.put(self.classrooms_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        data = self.classroom_data
        response_admin = self.client.put(self.classrooms_detail_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"}, data=data)
        response_student2 = self.client.put(self.classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"},
                                            data=data)
        response_teacher2 = self.client.put(self.classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"},
                                            data=data)
        self.assertEqual(response_admin.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_student2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_teacher2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response_admin.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_student2.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_teacher2.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        data = self.classroom_data
        response = self.client.put(self.classrooms_detail_url,
                                   headers={"Authorization": f"Bearer {self.teacher_access_token}"}, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.classroom_name)


class ClassroomDestroyAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.classrooms_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        response_admin = self.client.delete(self.classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.admin_access_token}"})
        response_student2 = self.client.delete(self.classrooms_detail_url,
                                               headers={"Authorization": f"Bearer {self.student2_access_token}"}, )
        response_teacher2 = self.client.delete(self.classrooms_detail_url,
                                               headers={"Authorization": f"Bearer {self.teacher2_access_token}"}, )
        self.assertEqual(response_admin.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_student2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_teacher2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response_admin.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_student2.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(str(response_teacher2.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.delete(self.classrooms_detail_url,
                                      headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Classroom.objects.filter(id=self.classroom1_id).exists())


class StudentClassroomCreateAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.post(self.students_classrooms_create_url, data=self.student_classroom_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_or_student_user(self):
        response = self.client.post(self.students_classrooms_create_url, data=self.student_classroom_data,
                                    headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_teacher_who_have_no_classrooms(self):
        data = self.student_classroom_data
        data.update({"student_id": self.student_profile.id})
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher3_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not a valid classroom.", response.data)

    def test_view_with_authenticated_teacher_who_have_classroom(self):
        data = self.student_classroom_data
        data.update({"student_id": self.student_profile.id})
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_with_authenticated_teacher_who_have_classroom_without_student_id(self):
        data = self.student_classroom_data
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("student_id is required for teachers.", response.data)

    def test_view_with_authenticated_teacher_who_have_classroom_with_existing_record(self):
        data = {
            "classroom_id": self.classroom1_id,
            "student_id": self.student_profile.id,
        }
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This student is already enrolled in the specified classroom.", response.data)

    def test_view_with_authenticated_teacher_who_have_classroom_with_invalid_student_id(self):
        invalid_student_id = self.fake.uuid4()
        data = self.student_classroom_data
        data.update({"student_id": invalid_student_id})
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("StudentProfile matching query does not exist.", response.data)

    def test_view_with_authenticated_student(self):
        data = self.student_classroom_data
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_with_authenticated_student_with_existing_data(self):
        data = {
            "classroom_id": self.classroom1_id,
        }
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This student is already enrolled in the specified classroom.", response.data)

    def test_view_with_authenticated_student_with_invalid_classroom_id(self):
        invalid_classroom_id = self.fake.uuid4()
        data = {
            "classroom_id": invalid_classroom_id,
        }
        response = self.client.post(self.students_classrooms_create_url, data=data,
                                    headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Classroom matching query does not exist.", response.data)


class StudentClassroomListAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.students_classrooms_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_teacher_or_student_user(self):
        response = self.client.get(self.students_classrooms_list_url,
                                   headers={"Authorization": f"Bearer {self.admin_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_student(self):
        response = self.client.get(self.students_classrooms_list_url,
                                   headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_with_authenticated_student_who_had_not_joined_classrooms(self):
        response = self.client.get(self.students_classrooms_list_url,
                                   headers={"Authorization": f"Bearer {self.student3_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_view_with_authenticated_teacher(self):
        response = self.client.get(self.students_classrooms_list_url,
                                   headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_with_authenticated_teacher_who_have_no_classrooms(self):
        response = self.client.get(self.students_classrooms_list_url,
                                   headers={"Authorization": f"Bearer {self.teacher3_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class StudentClassroomRetrieveAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.get(self.students_classrooms_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_member_user(self):
        admin_response = self.client.get(self.students_classrooms_detail_url,
                                         headers={"Authorization": f"Bearer {self.admin_access_token}"})
        student2_response = self.client.get(self.students_classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.student2_access_token}"})
        teacher2_response = self.client.get(self.students_classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(admin_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(student2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(student2_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(teacher2_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_member_user(self):
        teacher_response = self.client.get(self.students_classrooms_detail_url,
                                           headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        student_response = self.client.get(self.students_classrooms_detail_url,
                                           headers={"Authorization": f"Bearer {self.student_access_token}"})
        self.assertEqual(teacher_response.status_code, status.HTTP_200_OK)
        self.assertEqual(student_response.status_code, status.HTTP_200_OK)


class StudentClassroomDestroyAPIViewTests(TestSetUp):
    def test_view_with_unauthenticated_user(self):
        response = self.client.delete(self.students_classrooms_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_view_with_authenticated_non_classroom_owner_users(self):
        admin_response = self.client.delete(self.students_classrooms_detail_url,
                                            headers={"Authorization": f"Bearer {self.admin_access_token}"})
        student_response = self.client.delete(self.students_classrooms_detail_url,
                                              headers={"Authorization": f"Bearer {self.student_access_token}"})
        teacher2_response = self.client.delete(self.students_classrooms_detail_url,
                                               headers={"Authorization": f"Bearer {self.teacher2_access_token}"})
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(admin_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(student_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(student_response.data["detail"]), "You do not have permission to perform this action.")
        self.assertEqual(teacher2_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(teacher2_response.data["detail"]), "You do not have permission to perform this action.")

    def test_view_with_authenticated_classroom_owner_user(self):
        response = self.client.delete(self.students_classrooms_detail_url,
                                      headers={"Authorization": f"Bearer {self.teacher_access_token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            StudentClassroom.objects.filter(student=self.student_profile, classroom=self.classroom1).exists())
