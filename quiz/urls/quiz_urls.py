from django.urls import path

from quiz.views import quiz_views

app_name = "quiz"

urlpatterns = [
    path('', quiz_views.QuizListAPIView.as_view(), name='quizzes-list'),
    path('create/', quiz_views.QuizCreateAPIView.as_view(), name='quizzes-create'),
    path('<uuid:quiz_id>/', quiz_views.QuizRetrieveUpdateDestroyAPIView.as_view(), name='quizzes-detail'),
]
