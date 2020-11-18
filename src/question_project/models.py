from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserModel(User):
    pass


class Quiz(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()

    def questions(self):
        if self.pk:
            return Question.objects.filter(quiz=self.pk)
        else:
            return None

    def __str__(self):
        return self.name


def validate_list(choice):
    choices = choice.split(",")
    if len(choices) < 2:
        raise ValidationError("This field requires an associated list of choices. Must contain more than 1 choices. Separate with comma.")


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_CHOICES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'select-multiple'),
        (INTEGER, 'integer')
    )

    text = models.CharField(max_length=400)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(choices=QUESTION_CHOICES, default=TEXT, max_length=400)
    choices = models.TextField(
        blank=True,
        null=True,
        help_text="If the question type is not text, then you need to separate variants with comma."
    )

    def clean(self):
        if self.question_type in (Question.RADIO, Question.SELECT, Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super().clean()

    def get_choices(self):
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))

        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __str__(self):
        return self.text


class Response(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    time = models.TextField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    is_anonymous = models.BooleanField(default=False)

    def show_user(self):
        if self.is_anonymous:
            return 'anonymous'
        return self.user

    def __str__(self):
        return f"{self.quiz} by {self.show_user()}"


class AnswerBase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)


class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerInteger(AnswerBase):
    body = models.TextField(blank=True, null=True)


