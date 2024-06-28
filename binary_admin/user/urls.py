from django.urls import path
from . import views

urlpatterns = [
    path("user/register", views.register, name="register"),
    path("user/login", views.binary_login, name="login"),
    path("user/logininicio", views.binary_logininicio, name="logininicio"),
]
