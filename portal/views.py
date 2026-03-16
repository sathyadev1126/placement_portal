from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Question, Score
from django.db.models import Avg, Count
from django.db.models import Avg, Max
from .models import Score
import random
from django.contrib.auth.decorators import login_required

from .models import Score

def home(request):
    return render(request, 'home.html')


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):

    scores = Score.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'scores': scores
    })


# ---------------- QUIZ ----------------

@login_required
def quiz(request):

    questions = Question.objects.all()

    return render(request,'quiz.html',{
        'questions':questions
    })


# ---------------- RESULT ----------------

@login_required
def result(request):

    question_ids = request.POST.getlist('question_ids')

    questions = Question.objects.filter(id__in=question_ids)

    score = 0
    unanswered = 0

    for q in questions:

        selected = request.POST.get(str(q.id))

        if not selected:
            unanswered += 1

        elif selected == q.answer:
            score += 1

    total = questions.count()
    wrong = total - score - unanswered

    percentage = 0
    if total > 0:
        percentage = round((score / total) * 100, 2)

    Score.objects.create(
        user=request.user,
        score=score,
        total=total
    )

    return render(request, 'result.html', {
        'score': score,
        'total': total,
        'wrong': wrong,
        'unanswered': unanswered,
        'percentage': percentage
    })
@login_required
def section_test(request, company, section):

    questions = Question.objects.filter(company=company, section=section)

    return render(request,'quiz.html',{
        'questions':questions,
        'company':company,
        'section':section
    })


@login_required
def profile(request):

    scores = Score.objects.filter(user=request.user)

    total_tests = scores.count()
    highest_score = scores.aggregate(Max('score'))['score__max']
    average_score = scores.aggregate(Avg('score'))['score__avg']

    return render(request,'profile.html',{
        'total_tests': total_tests,
        'highest_score': highest_score,
        'average_score': average_score
    })


@login_required
def mocktest(request, company):

    quant = Question.objects.filter(company=company, section='QUANT').order_by('?')[:5]
    reasoning = Question.objects.filter(company=company, section='REASON').order_by('?')[:3]
    verbal = Question.objects.filter(company=company, section='VERBAL').order_by('?')[:2]

    questions = list(quant) + list(reasoning) + list(verbal)
    Question.objects.filter(company=company)
    return render(request, "mocktest.html", {
        "questions": questions,
        "company": company
    })

@login_required
def company_tests(request):
    return render(request, "company_test.html")
# ---------------- ADMIN LEADERBOARD ----------------

def admin_check(user):
    return user.is_superuser


@user_passes_test(admin_check)
def leaderboard(request):

    scores = Score.objects.select_related('user').order_by('-score')

    total_students = Score.objects.values('user').distinct().count()
    total_tests = Score.objects.count()
    avg_score = Score.objects.aggregate(Avg('score'))['score__avg']

    return render(request,'leaderboard.html',{
        'scores':scores,
        'total_students': total_students,
        'total_tests': total_tests,
        'avg_score': avg_score
    })


# ---------------- SIGNUP ----------------

def signup(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login')

    return render(request, 'signup.html')


# ---------------- LOGIN ----------------

def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            # Admin goes to leaderboard
            if user.is_superuser:
                return redirect('/leaderboard')

            # Student goes to dashboard
            else:
                return redirect('/dashboard')

    return render(request, 'login.html')
# ---------------- LOGOUT ----------------

@login_required
def logout_user(request):

    logout(request)

    return redirect('/login')

@login_required
def profile(request):

    scores = Score.objects.filter(user=request.user).order_by('-id')

    total_tests = scores.count()

    best_score = 0
    avg_percentage = 0

    percentages = []

    for s in scores:
        p = round((s.score / s.total) * 100, 2) if s.total > 0 else 0
        percentages.append(p)

    if percentages:
        best_score = max(percentages)
        avg_percentage = round(sum(percentages)/len(percentages),2)

    return render(request,'profile.html',{
        'scores':scores,
        'total_tests':total_tests,
        'best_score':best_score,
        'avg_percentage':avg_percentage
    })

@login_required
def performance(request):

    scores = Score.objects.filter(user=request.user).order_by('-created_at')

    best_score = 0
    avg_score = 0

    if scores.exists():
        best_score = max([s.score for s in scores])
        avg_score = round(sum([s.score for s in scores]) / scores.count(),2)

    return render(request,"performance.html",{
        "scores":scores,
        "best_score":best_score,
        "avg_score":avg_score
    })