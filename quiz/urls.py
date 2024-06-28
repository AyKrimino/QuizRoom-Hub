from django.urls import path, include

app_name = "quiz"

urlpatterns = [
    path("quizzes/", include("quiz.urls.quiz_urls")),
    path("quizzes/<uuid:quiz_id>/questions/", include("quiz.urls.question_urls")),
    path("quizzes/<uuid:quiz_id>/questions/<uuid:question_id>/answers/", include("quiz.urls.answer_urls")),
    path("quizzes/<uuid:quiz_id>/", include("quiz.urls.student_quiz_urls")),
]
