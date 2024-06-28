from django.shortcuts import render, redirect, resolve_url
from clientes.models import Empresa
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import User, Permission
from django.core.mail import send_mail


# Create your views here.
def prueba(request):
    return render(request, "base/base.html")


def is_staff(user: User):
    return user.is_staff


@user_passes_test(is_staff, "login")
def main(request):
    empresas = Empresa.objects.all()
    return render(
        request,
        "binary_admin/main/index.html",
        {
            "empresas": empresas,
        },
    )


@user_passes_test(is_staff, "login")
def cliente(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        empresas = Empresa.objects.all()
        return render(
            request,
            "binary_admin/main/clientes.html",
            {"empresas": empresas, "empresa_actual": empresa},
        )
    else:
        return redirect("binary_main")


@user_passes_test(is_staff, "login")
def registrar_empresa(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        if not empresa.is_registered:
            empresa.can_register = True
            empresa.save()
            send_mail(
                "Acceso al Sistema de Binary CA",
                f"""
Estimado/a {empresa.nombre},

¡Es un placer informarle que su cuenta ha sido configurada exitosamente en nuestro sistema! A continuación, ingrese al enlace que está a continuación para acceder:

https://firmabinary.pythonanywhere.com{resolve_url("register_cliente", empresa.user.username)}

Por motivos de seguridad, le recomendamos NO compartir este link con terceros

Si tiene algún problema para iniciar sesión o necesita asistencia adicional, no dude en comunicarse con nuestro equipo.

Gracias por confiar en Binary CA para sus necesidades contables y financieras. Estamos aquí para ayudarle en cada paso del camino.

Saludos cordiales,
Equipo de Binary CA

Binary CA
Calle 23 entre carreras 17 y 18 Torre Binary. 
Municipio Iribarren. Barquisimeto. Estado Lara. Venezuela.
""",
                "firmabinary@gmail.com",
                [
                    empresa.user.email,
                ],
                fail_silently=False,
            )
        return redirect("binary_clientes", empresa_nombre)
    else:
        return redirect("binary_main")


@user_passes_test(is_staff, "login")
def eliminar_empresa(request: HttpRequest, empresa_nombre):
    pass
