from django.urls import path, include

app_name = "quiz"

urlpatterns = [
    path("quizzes/", include("quiz.urls.quiz_urls", namespace="quiz")),
    path("quizzes/<uuid:quiz_id>/questions/", include("quiz.urls.question_urls", namespace="question")),
    path("quizzes/<uuid:quiz_id>/questions/<uuid:question_id>/answers/",
         include("quiz.urls.answer_urls", namespace="answer")),
    path("quizzes/<uuid:quiz_id>/", include("quiz.urls.student_quiz_urls", namespace="student-quiz")),
]
