from django.urls import path
from . import views

urlpatterns = [
    path("user/prueba", views.prueba, name="prueba"),
    path("user/register", views.register, name="register"),
]
