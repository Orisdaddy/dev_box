from django.urls import path
from user import views

urlpatterns = [
    path("user/login", views.Login.as_view()),
    path("user/captcha", views.Captcha.as_view()),
]
