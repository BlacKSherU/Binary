from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.prueba),
    path("", views.main),
]
