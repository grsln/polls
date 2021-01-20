from django.contrib import admin

from .models import Poll, Choice, Question


class ChoicesInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [ChoicesInline]
    save_on_top = True
    save_as = True


class QuestionsInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Poll)
class PollsAdmin(admin.ModelAdmin):
    model = Poll
    readonly_fields = ("start_date",)
    inlines = [QuestionsInline]
    save_on_top = True
    save_as = True
