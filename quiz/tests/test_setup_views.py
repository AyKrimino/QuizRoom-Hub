from decimal import Decimal

from django.urls import reverse

from classroom.tests.test_setup import TestSetUp
from quiz.models import Quiz, Question, Answer, StudentAnswer, StudentQuiz


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

        self.answers_list_url = reverse("quiz:answer:answers-list", kwargs={"quiz_id": str(self.quiz.id),
                                                                            "question_id": str(self.question.id), })
        self.answers_create_url = reverse("quiz:answer:answers-create", kwargs={"quiz_id": str(self.quiz.id),
                                                                                "question_id": str(
                                                                                    self.question.id), })

        self.answer_data = {
            "description": self.fake.text(),
            "is_valid": True,
        }

        self.answer = Answer.objects.create(
            description="answer description",
            is_valid=False,
            question=self.question,
        )

        self.answer2 = Answer.objects.create(
            description="Answer 2 description",
            is_valid=True,
            question=self.question,
        )

        self.answers_detail_url = reverse("quiz:answer:answers-detail",
                                          kwargs={"quiz_id": str(self.quiz.id), "question_id": str(self.question.id),
                                                  "answer_id": str(self.answer.id)})

        self.student_answer_create_url = reverse("quiz:student-quiz:student-answer-create",
                                                 kwargs={"quiz_id": str(self.quiz.id), })

        self.student_answer_data = {
            "question_id": str(self.question.id),
            "answer_id": str(self.answer.id),
        }

        self.student_answer = StudentAnswer.objects.create(
            student=self.student2_profile,
            answer=self.answer2,
        )

        self.student_quiz = StudentQuiz.objects.create(
            student=self.student_profile,
            quiz=self.quiz,
            mark=Decimal('100.00'),
        )

        self.student_quiz_list_url = reverse("quiz:student-quiz:student-quiz-list",
                                             kwargs={"quiz_id": str(self.quiz.id), })
        self.student_quiz_create_url = reverse("quiz:student-quiz:student-quiz-create",
                                               kwargs={"quiz_id": str(self.quiz.id), })

    def tearDown(self):
        return super().tearDown()
