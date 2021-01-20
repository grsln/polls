from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AnswerView, CreateUserPollView, QuestionViewSet, PollViewSet, \
    PollsViewSet, UserPollsListViewSet

app_name = 'polls_api'
router = DefaultRouter()
router.register('poll', PollViewSet, basename='api')
router.register('question', QuestionViewSet, basename='api')
router.register('polls', PollsViewSet, basename='api')
router.register('user/polls', UserPollsListViewSet, basename='api')
urlpatterns = [
    path("user/poll/<int:pk>/", AnswerView.as_view(), name="user_poll"),
    path("user/poll/create/", CreateUserPollView.as_view(), name="user_poll_create"),
]
urlpatterns += router.urls
