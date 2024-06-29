from django.urls import path

from quiz.views import answer_views

app_name = "answer"

urlpatterns = [
    path('', answer_views.AnswerListAPIView.as_view(), name='answers-list'),
    path('create/', answer_views.AnswerCreateAPIView.as_view(), name='answers-create'),
    path('<uuid:answer_id>/', answer_views.AnswerRetrieveUpdateDestroyAPIView.as_view(), name='answers-detail'),
]
