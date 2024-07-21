from django.urls import reverse

from account.tests.test_setup import TestSetup
from classroom.models import Classroom, StudentClassroom


class TestSetUp(TestSetup):
    def setUp(self):
        super().setUp()
        self.classrooms_list_url = reverse("classroom:classrooms-list")
        self.classrooms_create_url = reverse("classroom:classrooms-create")
        self.students_classrooms_list_url = reverse("classroom:students-classrooms-list")
        self.students_classrooms_create_url = reverse("classroom:students-classrooms-create")

        # classroom dummy data
        self.classroom_name = self.fake.name()
        self.classroom_data = {
            "name": self.classroom_name,
        }

        # classroom1
        self.classroom1_name = self.fake.name()
        self.classroom1_data = {
            "teacher": self.teacher_profile,
            "name": self.classroom1_name,
        }
        self.classroom1 = Classroom.objects.create(**self.classroom1_data)
        self.classroom1_id = self.classroom1.id
        self.classrooms_detail_url = reverse("classroom:classrooms-detail", kwargs={"pk": self.classroom1.id})

        # classroom2
        self.classroom2_name = self.fake.name()
        self.classroom2_data = {
            "teacher": self.teacher2_profile,
            "name": self.classroom2_name,
        }
        self.classroom2 = Classroom.objects.create(**self.classroom2_data)

        # classroom3
        self.classroom3_name = self.fake.name()
        self.classroom3_data = {
            "teacher": self.teacher_profile,
            "name": self.classroom3_name,
        }
        self.classroom3 = Classroom.objects.create(**self.classroom3_data)

        self.student_classroom1 = StudentClassroom.objects.create(student=self.student_profile,
                                                                  classroom=self.classroom1)
        self.student2_classroom2 = StudentClassroom.objects.create(student=self.student2_profile,
                                                                   classroom=self.classroom2)
        self.students_classrooms_detail_url = reverse("classroom:students-classrooms-detail",
                                                      kwargs={"student_id": self.student_profile.id,
                                                              "classroom_id": self.classroom1_id})
        self.student_classroom3 = StudentClassroom.objects.create(student=self.student_profile,
                                                                  classroom=self.classroom3)

        self.student_classroom_data = {
            "classroom_id": self.classroom2.id,
        }

    def tearDown(self):
        return super().tearDown()
