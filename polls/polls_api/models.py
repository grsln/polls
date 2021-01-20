from django.db import models
from django.shortcuts import get_object_or_404

TYPE_CHOICES = (
    (1, "Text"),
    (2, "One variant"),
    (3, "Many variants"),)


class Poll(models.Model):
    name = models.CharField('Тема опроса', max_length=200)
    start_date = models.DateTimeField('Начало опроса')
    end_date = models.DateTimeField('Конец опроса')
    description = models.CharField('Описание', max_length=200)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField('Вопрос', max_length=200)
    type = models.PositiveSmallIntegerField('Тип вопроса', choices=TYPE_CHOICES)
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question


class Choice(models.Model):
    choice = models.CharField('Вариант', max_length=200)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

    def __str__(self):
        return '#id {}'.format(self.id)


class UserPolls(models.Model):
    user = models.IntegerField('UserID')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Опросы пользователя"
        verbose_name_plural = "Опросы пользователей"

    def __str__(self):
        return '#id {}'.format(self.id)

    def save(self, *args, **kwargs):
        new_poll = False
        if not self.pk:
            new_poll = True
        super().save(*args, **kwargs)
        if new_poll:
            questions = get_object_or_404(Poll.objects.all(), pk=self.poll.id).questions.all()
            for item in questions:
                answer_choice = AnswerChoice.objects.create(userpoll=self, question=item)
                if item.type == 1:
                    AnswerText.objects.create(answer_choice=answer_choice)


class AnswerChoice(models.Model):
    userpoll = models.ForeignKey(UserPolls, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ManyToManyField(Choice)

    class Meta:
        verbose_name = "Ответ вариантами"
        verbose_name_plural = "Ответы вариантами"

    def __str__(self):
        return '#id {}'.format(self.id)


class AnswerText(models.Model):
    answer_choice = models.ForeignKey(AnswerChoice, related_name='texts', on_delete=models.CASCADE)
    text = models.CharField('Тест ответа', max_length=200)

    class Meta:
        verbose_name = "Ответ текстом"
        verbose_name_plural = "Ответы текстом"

    def __str__(self):
        return '#id {}'.format(self.id)
