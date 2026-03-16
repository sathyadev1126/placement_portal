from django.urls import path
from . import views

urlpatterns = [
path('',views.home,name='home'),
path('dashboard/',views.dashboard,name='dashboard'),
path('quiz/',views.quiz,name='quiz'),
path('result/',views.result,name='result'),
path('signup/',views.signup,name='signup'),
path('login/',views.login_user,name='login'),
path('leaderboard/', views.leaderboard, name='leaderboard'),
path('logout/', views.logout_user, name='logout'),
path('profile/', views.profile, name='profile'),
path('mocktest/', views.company_tests, name='company_tests'),
path('mocktest/<str:company>/', views.mocktest, name='mocktest'),
path('section/<str:company>/<str:section>/', views.section_test),
path('profile/', views.profile, name='profile'),
path('performance/', views.performance, name='performance'),
]