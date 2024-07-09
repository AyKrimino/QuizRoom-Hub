from django.urls import reverse

from classroom.tests.test_setup import TestSetUp
from quiz.models import Quiz, Question


class QuizTestSetup(TestSetUp):
    def setUp(self):
        super().setUp()
        self.quizzes_list_url = reverse("quiz:quiz:quizzes-list")
        self.quizzes_create_url = reverse("quiz:quiz:quizzes-create")

        # quiz creation data
        self.quiz_data = {
            "title": self.fake.name(),
            "content": self.fake.text(),
            "classroom_id": str(self.classroom1_id),
        }

        self.quiz = Quiz.objects.create(
            title="quiz1",
            content="content1",
            classroom=self.classroom2,
        )
        self.quizzes_detail_url = reverse("quiz:quiz:quizzes-detail", kwargs={"quiz_id": str(self.quiz.id)})

        self.questions_list_url = reverse("quiz:question:questions-list", kwargs={"quiz_id": str(self.quiz.id), })
        self.questions_create_url = reverse("quiz:question:questions-create", kwargs={"quiz_id": str(self.quiz.id), })

        self.question_data = {
            "description": self.fake.text(),
        }

        self.question = Question.objects.create(
            description="question1 description",
            quiz=self.quiz,
        )

        self.questions_detail_url = reverse("quiz:question:questions-detail",
                                            kwargs={"quiz_id": str(self.quiz.id),
                                                    "question_id": str(self.question.id), })

        # self.answers_list_url = reverse("quiz:answers:answers-list", kwargs={"quiz_id": self.quiz.id, })
        # self.answers_create_url = reverse("quiz:answers:answers-create", kwargs={"quiz_id": self.quiz.id, })
        # self.answers_detail_url = reverse("quiz:answers:answers-detail", kwargs={"quiz_id": self.quiz.id, })

        self.student_answer_create_url = reverse("quiz:student-quiz:student-answer-create",
                                                 kwargs={"quiz_id": str(self.quiz.id), })
        self.student_quiz_list_url = reverse("quiz:student-quiz:student-quiz-list",
                                             kwargs={"quiz_id": str(self.quiz.id), })
        self.student_quiz_create_url = reverse("quiz:student-quiz:student-quiz-create",
                                               kwargs={"quiz_id": str(self.quiz.id), })

    def tearDown(self):
        return super().tearDown()
