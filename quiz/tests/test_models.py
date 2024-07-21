import uuid
from datetime import timedelta

from django.db.utils import IntegrityError
from django.utils import timezone

from quiz.models import Quiz, Question, Answer, StudentQuiz
from quiz.tests.test_setup_models import TestSetup


class QuizTests(TestSetup):
    def test_create_quiz_with_manager(self):
        Quiz.objects.create(**self.quiz_data)
        quiz = Quiz.objects.get(title=self.quiz_data["title"])
        self.assertIsNotNone(quiz)
        self.assertEqual(quiz.title, self.quiz_data["title"])
        self.assertEqual(quiz.content, self.quiz_data["content"])
        self.assertEqual(quiz.classroom, self.classroom)

    def test_create_quiz_without_manager(self):
        quiz = Quiz(**self.quiz_data)
        quiz.save()
        quiz.refresh_from_db()
        self.assertEqual(quiz.title, self.quiz_data["title"])
        self.assertEqual(quiz.content, self.quiz_data["content"])
        self.assertEqual(quiz.classroom, self.classroom)

    def test_quiz_string_representation(self):
        quiz = Quiz.objects.create(**self.quiz_data)
        self.assertEqual(str(quiz), f"{self.quiz_data['title']}-{self.quiz_data['classroom']}")

    def test_create_quiz_without_classroom(self):
        del self.quiz_data["classroom"]
        with self.assertRaises(IntegrityError):
            Quiz.objects.create(**self.quiz_data)

    def test_quiz_uuid_generation(self):
        quiz = Quiz.objects.create(**self.quiz_data)
        self.assertIsNotNone(quiz.id)
        self.assertIsInstance(quiz.id, uuid.UUID)

    def test_quiz_auto_now_add_and_auto_now_fields(self):
        quiz = Quiz.objects.create(**self.quiz_data)
        self.assertIsNotNone(quiz.created_at)
        self.assertIsNotNone(quiz.last_updated)

        # Compare the created_at and last_updated fields with a small allowable difference
        self.assertAlmostEqual(quiz.created_at, quiz.last_updated, delta=timedelta(seconds=1))

        old_last_updated = quiz.last_updated
        old_created_at = quiz.created_at

        quiz.content = self.fake.text()
        quiz.save()
        quiz.refresh_from_db()

        # Ensure that last_updated is updated but created_at remains the same
        self.assertEqual(quiz.created_at, old_created_at)
        self.assertGreater(quiz.last_updated, old_last_updated)

    def test_quiz_null_blank_content(self):
        self.quiz_data['content'] = None
        quiz = Quiz.objects.create(**self.quiz_data)
        self.assertIsNone(quiz.content)

        self.quiz_data['content'] = ''
        quiz = Quiz.objects.create(**self.quiz_data)
        self.assertEqual(quiz.content, '')

    def test_quiz_related_name(self):
        quiz = Quiz.objects.create(**self.quiz_data)
        self.assertIn(quiz, self.classroom.quizzes.all())


class QuestionTests(TestSetup):
    def test_create_question_with_manager(self):
        Question.objects.create(**self.question_data)
        question = Question.objects.get(description=self.question_data["description"])
        self.assertIsNotNone(question)
        self.assertEqual(question.description, self.question_data["description"])
        self.assertEqual(question.quiz, self.quiz)

    def test_create_question_without_manager(self):
        question = Question(**self.question_data)
        question.save()
        question.refresh_from_db()
        self.assertIsNotNone(question)
        self.assertEqual(question.description, self.question_data["description"])
        self.assertEqual(question.quiz, self.quiz)

    def test_create_question_without_quiz(self):
        del self.question_data["quiz"]
        with self.assertRaises(IntegrityError):
            Question.objects.create(**self.question_data)

    def test_question_string_representation(self):
        question = Question.objects.create(**self.question_data)
        self.assertEqual(str(question), f"{self.question_data['description'][:10]}...")

    def test_question_related_name(self):
        question = Question.objects.create(**self.question_data)
        self.assertIn(question, self.quiz.questions.all())

    def test_question_uuid_generation(self):
        question = Question.objects.create(**self.question_data)
        self.assertIsNotNone(question.id)
        self.assertIsInstance(question.id, uuid.UUID)


class AnswerTests(TestSetup):
    def test_create_answer_with_manager(self):
        Answer.objects.create(**self.answer_data)
        answer = Answer.objects.get(description=self.answer_data["description"])
        self.assertIsNotNone(answer)
        self.assertEqual(answer.description, self.answer_data["description"])
        self.assertEqual(answer.is_valid, self.answer_data["is_valid"])
        self.assertEqual(answer.question, self.answer_data["question"])

    def test_create_answer_without_manager(self):
        answer = Answer(**self.answer_data)
        answer.save()
        answer.refresh_from_db()
        self.assertIsNotNone(answer)
        self.assertEqual(answer.description, self.answer_data["description"])
        self.assertEqual(answer.is_valid, self.answer_data["is_valid"])
        self.assertEqual(answer.question, self.answer_data["question"])

    def test_create_answer_without_question(self):
        del self.answer_data["question"]

        with self.assertRaises(IntegrityError):
            Answer.objects.create(**self.answer_data)

    def test_answer_string_representation(self):
        answer = Answer.objects.create(**self.answer_data)
        self.assertEqual(str(answer), f"{self.answer_data['description'][:10]}")

    def test_answer_uuid_generation(self):
        answer = Answer.objects.create(**self.answer_data)
        self.assertIsNotNone(answer.id)
        self.assertIsInstance(answer.id, uuid.UUID)

    def test_answer_related_name(self):
        answer = Answer.objects.create(**self.answer_data)
        self.assertIn(answer, self.question.answers.all())


class StudentQuizTests(TestSetup):
    def test_create_student_quiz_with_manager(self):
        StudentQuiz.objects.create(**self.student_quiz_data)
        student_quiz = StudentQuiz.objects.get(student=self.student_profile, quiz=self.quiz)
        self.assertIsNotNone(student_quiz)
        self.assertEqual(student_quiz.student, self.student_profile)
        self.assertEqual(student_quiz.quiz, self.quiz)
        self.assertEqual(float(student_quiz.mark), 14.99)

    def test_create_student_quiz_without_manager(self):
        student_quiz = StudentQuiz(**self.student_quiz_data)
        student_quiz.save()
        student_quiz.refresh_from_db()
        self.assertIsNotNone(student_quiz)
        self.assertEqual(student_quiz.student, self.student_profile)
        self.assertEqual(student_quiz.quiz, self.quiz)
        self.assertEqual(float(student_quiz.mark), 14.99)

    def test_student_quiz_auto_now_add_field(self):
        student_quiz = StudentQuiz.objects.create(**self.student_quiz_data)
        self.assertIsNotNone(student_quiz.answered_at)

        self.assertAlmostEqual(student_quiz.answered_at, timezone.now(), delta=timedelta(seconds=1))

        old_answered_at = student_quiz.answered_at

        student_quiz.mark = 15.99
        student_quiz.save()
        student_quiz.refresh_from_db()

        self.assertEqual(student_quiz.answered_at, old_answered_at)

    def test_student_quiz_string_representation(self):
        student_quiz = StudentQuiz.objects.create(**self.student_quiz_data)
        self.assertEqual(str(student_quiz), f"{self.student_profile}-{self.quiz} -> {self.student_quiz_data['mark']}")

    def test_student_quiz_related_names(self):
        student_quiz = StudentQuiz.objects.create(**self.student_quiz_data)
        self.assertIn(student_quiz, self.student_profile.submitted_quizzes.all())
        self.assertIn(student_quiz, self.quiz.student_answers.all())

    def test_create_student_quiz_with_same_student_and_quiz_twice(self):
        with self.assertRaises(IntegrityError):
            StudentQuiz.objects.create(**self.student_quiz_data)
            StudentQuiz.objects.create(**self.student_quiz_data)
