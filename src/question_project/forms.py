from django import forms
from django.forms import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from datetime import timedelta

from .models import (
    UserModel,
    Response,
    Question,
    AnswerText,
    AnswerRadio,
    AnswerSelect,
    AnswerSelectMultiple,
    AnswerInteger
)


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError('This user already exists.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password.")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        return password2


class LoginForm(AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


class ResponseForm(models.ModelForm):
    class Meta:
        model = Response
        fields = ['is_anonymous']

    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')
        user = UserModel.objects.get(id=kwargs.pop('user_id'))
        self.time = kwargs.pop('time')
        self.user = user
        self.quiz = quiz
        super(ResponseForm, self).__init__(*args, **kwargs)

        data = kwargs.get('data')
        for q in quiz.questions():
            if q.question_type == Question.TEXT:
                self.fields["question_%d" % q.pk] = forms.CharField(label=q.text,
                                                                    widget=forms.Textarea)
            elif q.question_type == Question.RADIO:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
                                                                      widget=forms.RadioSelect,
                                                                      choices=question_choices)
            elif q.question_type == Question.SELECT:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
                                                                      widget=forms.Select, choices=question_choices)
            elif q.question_type == Question.SELECT_MULTIPLE:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.text,
                                                                              widget=forms.CheckboxSelectMultiple,
                                                                              choices=question_choices)
            elif q.question_type == Question.INTEGER:
                self.fields["question_%d" % q.pk] = forms.IntegerField(label=q.text)

            if data:
                self.fields["question_%d" % q.pk].initial = data.get('question_%d' % q.pk)

    def save(self, commit=True):
        response = super(ResponseForm, self).save(commit=False)
        response.quiz = self.quiz
        response.user = self.user
        response.time = str(timedelta(milliseconds=int(self.time)))
        print(response.time)
        response.save()

        print(self.cleaned_data)
        for field_name, field_value in self.cleaned_data.items():
            print(field_name)
            if field_name.startswith('question_'):
                q_id = int(field_name.split('_')[1])
                q = Question.objects.get(pk=q_id)

                if q.question_type == Question.TEXT:
                    a = AnswerText(question=q)
                    a.body = field_value
                elif q.question_type == Question.RADIO:
                    a = AnswerRadio(question=q)
                    a.body = field_value
                elif q.question_type == Question.SELECT:
                    a = AnswerSelect(question=q)
                    a.body = field_value
                elif q.question_type == Question.SELECT_MULTIPLE:
                    a = AnswerSelectMultiple(question=q)
                    a.body = field_value
                elif q.question_type == Question.INTEGER:
                    a = AnswerInteger(question=q)
                    a.body = field_value

                a.response = response
                a.save()

        return response
