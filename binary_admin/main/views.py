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


def registrar_empresa(request: HttpRequest, empresa_nombre):
    empresa = Empresa.objects.get(nombre=empresa_nombre)
    empresa.Empresa_registrada = True
    empresa.save()
    empresa.user.user_permissions.add(
        Permission.objects.get(codename="register_company")
    )
    send_mail(
        "Bienvenido a Binary",
        "felicidades por unirte al equipo de binary pulsa el siguiente enlace para crear su usuario https://firmabinary.pythonanywhere.com"
        + resolve_url("register_cliente", empresa.user.username),
        "firmabinary@gmail.com",
        [
            empresa.user.email,
        ],
        fail_silently=False,
    )
    return redirect("binary_clientes", empresa_nombre)


def eliminar_empresa(request: HttpRequest, empresa_nombre):

    pass
