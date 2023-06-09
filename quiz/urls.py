"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from score.views import create_quiz, get_active_quiz, get_quiz_result, get_all_quizzes

urlpatterns = [
    path('',include('score.urls')),
    path('admin/', admin.site.urls),
    path('quizzes/', create_quiz, name='create-quiz'),
    path('quizzes/active/', get_active_quiz, name='get-active-quiz'),
    path('quizzes/<int:quiz_id>/result/', get_quiz_result, name='get-quiz-result'),
    path('quizzes/all/', get_all_quizzes, name='get-all-quizzes'),
]
