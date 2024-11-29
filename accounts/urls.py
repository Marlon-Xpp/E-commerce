from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.login , name="login"),
    path("signup/", views.signup , name="signup"),
    path("verify/code/", views.verify_code, name="verify_code"),
]
