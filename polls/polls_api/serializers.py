from rest_framework import serializers

from .models import Poll, Question, Choice, AnswerChoice, UserPolls, AnswerText


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'name', 'start_date', 'end_date', 'description')

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'type', 'poll')

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('question', instance.question)
        instance.type = validated_data.get('type', instance.type)
        instance.poll = validated_data.get('poll', instance.poll)
        instance.save()
        return instance


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice')


class UserQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question', 'type', 'choices')


class UserPollSerializer(serializers.ModelSerializer):
    questions = UserQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'start_date', 'end_date', 'description', 'questions')


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerText
        fields = ('id', 'text')


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'type')


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionAnswerSerializer(many=False)
    texts = TextSerializer(many=True)

    class Meta:
        model = AnswerChoice
        fields = ('id', 'question', 'choice', 'texts')


class UserChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ('id', 'userpoll', 'question', 'choice')


class UserAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = UserPolls
        fields = ('id', 'user', 'poll', 'answers')


class CreateUserPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolls
        fields = ('id', 'user', 'poll')

    def create(self, validated_data):
        return UserPolls.objects.create(**validated_data)
