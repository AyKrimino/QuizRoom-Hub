from django.urls import path

from quiz.views import student_quiz_views

app_name = "student-quiz"

urlpatterns = [
    path("student-answer/", student_quiz_views.StudentAnswerCreateAPIView.as_view(), name="student-answer-create"),
    path("student-quiz/", student_quiz_views.StudentQuizListAPIView.as_view(), name="student-quiz-list"),
    path("student-quiz/submit/", student_quiz_views.StudentQuizCreateAPIView.as_view(), name="student-quiz-create"),
]
