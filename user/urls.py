from django.urls import path
from user import views


urlpatterns = [
    path("login", views.Login.as_view()),
    path("captcha", views.Captcha.as_view()),
]
