from django.urls import path
from . import views

urlpatterns = [
    path("pruebas/", views.prueba),
    path("", views.main),
]
