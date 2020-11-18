from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from . import models


class QuestionInline(admin.TabularInline):
    model = models.Question
    extra = 0


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class AnswerBaseInline(admin.StackedInline):
    fields = ('question', 'body')
    readonly_fields = ('question',)
    extra = 0


class AnswerTextInline(AnswerBaseInline):
    model = models.AnswerText


class AnswerRadioInline(AnswerBaseInline):
    model = models.AnswerRadio


class AnswerSelectInline(AnswerBaseInline):
    model = models.AnswerSelect


class AnswerSelectMultipleInline(AnswerBaseInline):
    model = models.AnswerSelectMultiple


class AnswerIntegerInline(AnswerBaseInline):
    model = models.AnswerInteger


class ResponseAdmin(admin.ModelAdmin):
    fields = ['quiz', 'time', 'show_user']
    inlines = [
        AnswerTextInline,
        AnswerRadioInline,
        AnswerSelectInline,
        AnswerSelectMultipleInline
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Response, ResponseAdmin)
