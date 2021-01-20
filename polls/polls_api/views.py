import datetime
import pytz
from django.conf.global_settings import TIME_ZONE
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Poll, Question, UserPolls, AnswerChoice, AnswerText
from .serializers import PollSerializer, QuestionSerializer, UserPollSerializer, UserAnswerSerializer, \
    CreateUserPollSerializer, TextSerializer, UserChoiceSerializer


class PollViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    def post(self, request):
        poll_data = request.data.get('poll')
        serializer = PollSerializer(data=poll_data, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"poll": serializer.data})

    def put(self, request, pk):
        poll_data = request.data.get('poll')
        poll_saved = get_object_or_404(self.queryset, pk=pk)
        serializer = PollSerializer(instance=poll_saved, data=poll_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"poll": serializer.data})

    def delete(self, request, pk):
        poll = get_object_or_404(self.queryset, pk=pk)
        poll.delete()
        return Response("Опрос удален")


class QuestionViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def post(self, request):
        question_data = request.data.get('question')
        serializer = QuestionSerializer(data=question_data, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"question": serializer.data})

    def put(self, request, pk):
        question_data = request.data.get('question')
        question_saved = get_object_or_404(self.queryset, pk=pk)
        serializer = QuestionSerializer(instance=question_saved, data=question_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"question": serializer.data})

    def delete(self, request, pk):
        question = get_object_or_404(self.queryset, pk=pk)
        question.delete()
        return Response("Вопрос удален")


class PollsViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PollSerializer
    queryset = Poll.objects.filter(end_date__gte=datetime.datetime.now(tz=pytz.timezone(TIME_ZONE)),
                                   start_date__lte=datetime.datetime.now(tz=pytz.timezone(TIME_ZONE)))

    def list(self, request):
        polls_data = self.queryset
        serializer = PollSerializer(polls_data, many=True)
        return Response({"polls": serializer.data})

    def retrieve(self, request, pk):
        poll = get_object_or_404(self.queryset,
                                 pk=pk)
        serializer = UserPollSerializer(poll, many=False)
        return Response({"poll": serializer.data})


class AnswerView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserChoiceSerializer

    def get(self, request, pk):
        userpolls = get_object_or_404(UserPolls, pk=pk)
        serializer = UserAnswerSerializer(userpolls, many=False)
        return Response({"poll": serializer.data})

    def post(self, request, pk):
        user_id = request.data.get('user_id')
        userpoll_id = request.data.get('userpoll')
        question_id = request.data.get('question')
        choices_id = request.data.get('choice')
        text = request.data.get('text')
        userpoll = get_object_or_404(UserPolls, user=user_id, pk=userpoll_id)
        question = get_object_or_404(Question, pk=question_id)
        answer_choice = get_object_or_404(AnswerChoice, userpoll=userpoll, question=question_id)
        if question.type == 1:
            answer_text = get_object_or_404(AnswerText, answer_choice=answer_choice)
            serializer = TextSerializer(instance=answer_text, data={'text': text}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response('Ответ успешно сохранен')
        else:
            if question.type == 2:
                serializer = UserChoiceSerializer(instance=answer_choice, data={'choice': [choices_id[0]]},
                                                  partial=True)
            else:
                serializer = UserChoiceSerializer(instance=answer_choice, data={'choice': choices_id}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response('Ответ успешно сохранен')


class CreateUserPollView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserPollSerializer

    def post(self, request):
        userpoll_data = request.data
        serializer = CreateUserPollSerializer(data=userpoll_data, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"user_poll": serializer.data})


class UserPollsListViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserAnswerSerializer
    queryset = UserPolls.objects.all()

    def get(self, request):
        user_id = request.data.get('user_id')
        userpolls = self.queryset.filter(user=user_id)
        serializer = UserAnswerSerializer(userpolls, many=True)
        return Response({"user_polls": serializer.data})
