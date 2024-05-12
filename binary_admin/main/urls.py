from django.urls import path
from . import views

urlpatterns = [
    path("pruebas/", views.prueba),
    path("", views.main, name="binary_main"),
    path("clientes/<str:empresa_nombre>", views.cliente, name="binary_clientes"),
    path(
        "clientes/<str:empresa_nombre>/registrar",
        views.registrar_empresa,
        name="registrar_empresa",
    ),
    path(
        "clientes/<str:empresa_nombre>/eliminar",
        views.eliminar_empresa,
        name="eliminar_empresa",
    ),
]
