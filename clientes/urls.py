from django.urls import path
from . import views

urlpatterns = [
    path("<str:codigo>/register", views.register, name="register_cliente"),
]
