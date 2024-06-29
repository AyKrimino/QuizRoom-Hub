from django.urls import path

from quiz.views import question_views

app_name = "question"

urlpatterns = [
    path('', question_views.QuestionListAPIView.as_view(), name='questions-list'),
    path('create/', question_views.QuestionCreateAPIView.as_view(), name='questions-create'),
    path('<uuid:question_id>/', question_views.QuestionRetrieveUpdateDestroyAPIView.as_view(), name='questions-detail'),
]
