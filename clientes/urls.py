from django.urls import path
from . import views

urlpatterns = [
    path("<str:codigo>/register", views.register, name="register_cliente"),
    path("<str:empresa_nombre>", views.main, name="cliente_main"),
    path(
        "<str:empresa_nombre>/cuentas", views.cuentas_bancarias, name="cliente_cuentas"
    ),
    path(
        "<str:empresa_nombre>/cuentas/agregar",
        views.agregar_cuenta,
        name="cliente_cuentas_agregar",
    ),
    path(
        "<str:empresa_nombre>/cuentas/editar",
        views.editar_cuenta,
        name="cliente_cuentas_editar",
    ),
    path(
        "<str:empresa_nombre>/cuentas/eliminar",
        views.eliminar_cuenta,
        name="cliente_cuentas_eliminar",
    ),
]
