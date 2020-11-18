from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

from .forms import LoginForm, RegisterForm, ResponseForm
from .models import Quiz, Response


def home(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        all_quizes = Quiz.objects.all()
        finished_quizes = [r.quiz for r in Response.objects.filter(user=user)]
        print(finished_quizes)
        unfinished_quizes = list(set(all_quizes) - set(finished_quizes))
        print(unfinished_quizes)
        context['unfinished_quizes'] = unfinished_quizes
        context['finished_quizes'] = finished_quizes

    return render(request, "home.html", context)


def quiz(request, quiz_id):
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            num_response = Response.objects.filter(user=user).count()
            if num_response == 0:
                quizz = Quiz.objects.get(id=quiz_id)
                start_t = 0
                form = ResponseForm(quiz=quizz, user_id=user.id, time=start_t)
                context['form'] = form
                context['quiz_id'] = quiz_id
                return render(request, 'quiz.html', context)
            else:
                return redirect('home')
    else:
        user = request.user
        time = request.POST.get('time')
        quizz = Quiz.objects.get(id=quiz_id)
        form = ResponseForm(request.POST, quiz=quizz, user_id=user.id, time=time)
        form.save()
        return redirect('home')


def login_view(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            context['errors'] = 'Please enter correct username and password.'
    return render(request, 'login.html', context)


def register_view(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            context['errors'] = form.errors
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

