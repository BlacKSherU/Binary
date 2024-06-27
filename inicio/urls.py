from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("motivacion", views.no_lo_olvides, name="noloolvides"),
]
