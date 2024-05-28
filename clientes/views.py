from django.shortcuts import render, redirect
from django.http import HttpRequest
from clientes.models import Empresa, Cuenta_Bancaria
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
def prueba(user):
    return False


@login_required(login_url="login")
def main(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        if empresa.is_registered:
            if (request.user == empresa.user) or (
                request.user in empresa.accountants.all()
            ):
                # hola________________-_-_-_____-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_---_---_-_--_
                return render(request, "clientes/index.html", {"empresa": empresa})
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


@login_required(login_url="login")
def cuentas_bancarias(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        if empresa.is_registered:
            if (request.user == empresa.user) or (
                request.user in empresa.accountants.all()
            ):
                cuentas = Cuenta_Bancaria.objects.filter(empresa=empresa)
                bolivares_total = 0
                dolar_total = 0
                for cuenta in cuentas:
                    if cuenta.moneda == "Bs":
                        bolivares_total += cuenta.balance
                    else:
                        dolar_total += cuenta.balance
                return render(
                    request,
                    "clientes/cuentas_bancarias.html",
                    {
                        "empresa": empresa,
                        "cuentas": cuentas,
                        "dolar": dolar_total,
                        "bolivares": bolivares_total,
                    },
                )
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


@login_required(login_url="login")
def agregar_cuenta(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        if empresa.is_registered:
            if (request.user == empresa.user) or (
                request.user in empresa.accountants.all()
            ):
                if request.method == "POST":

                    cuentas = Cuenta_Bancaria.objects.filter(
                        empresa=empresa,
                        nombre=request.POST["banco"],
                        numero_cuenta=request.POST["numero_cuenta"],
                    )

                    if cuentas.count() < 1:
                        Cuenta_Bancaria.objects.create(
                            empresa=empresa,
                            nombre=request.POST["banco"],
                            numero_cuenta=request.POST["numero_cuenta"],
                            balance=request.POST["saldo"],
                            moneda=request.POST["moneda"],
                        )
                        messages.success(
                            request, "cuenta agregada con exito", "felicidades"
                        )
                    else:
                        messages.error(
                            request, "cuenta bancaria ya existente", "lo sentimos"
                        )
                return redirect("cliente_cuentas", empresa.nombre)
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


@login_required(login_url="login")
def editar_cuenta(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        if empresa.is_registered:
            if (request.user == empresa.user) or (
                request.user in empresa.accountants.all()
            ):
                if request.method == "POST":
                    cuenta_actual = Cuenta_Bancaria.objects.get(id=request.POST["id"])
                    cuentas = Cuenta_Bancaria.objects.filter(empresa=empresa)
                    bolivares_total = 0
                    dolar_total = 0
                    for cuenta in cuentas:
                        if cuenta.moneda == "Bs":
                            bolivares_total += cuenta.balance
                        else:
                            dolar_total += cuenta.balance
                    # hola________________-_-_-_____-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_---_---_-_--_
                    return render(
                        request,
                        "clientes/cuentas_bancarias_editar.html",
                        {
                            "empresa": empresa,
                            "cuentas": cuentas,
                            "dolar": dolar_total,
                            "bolivares": bolivares_total,
                            "cuenta_actual": cuenta_actual,
                        },
                    )
                return redirect("cliente_cuentas", empresa.nombre)
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


@login_required(login_url="login")
def eliminar_cuenta(request: HttpRequest, empresa_nombre):
    try:
        empresa = Empresa.objects.get(nombre=empresa_nombre)
        existe = True
    except Empresa.DoesNotExist:
        existe = False
    if existe:
        if empresa.is_registered:
            if (request.user == empresa.user) or (
                request.user in empresa.accountants.all()
            ):
                if request.method == "POST":
                    eliminar = Cuenta_Bancaria.objects.get(id=request.POST["id"])
                    eliminar.delete()
                    messages.success(
                        request, "cuenta eliminada con exito", "felicidades"
                    )

                return redirect("cliente_cuentas", empresa.nombre)
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


def register(request: HttpRequest, codigo):
    try:
        user = User.objects.get(username=codigo)
        existe = True
    except User.DoesNotExist:
        existe = False
    if existe:
        try:
            empresa = Empresa.objects.get(user=user)
            existe = True
        except Empresa.DoesNotExist:
            existe = False
    if existe:
        if empresa.can_register:
            if "rif" in request.POST:
                user.username = request.POST["user"]
                user.password = request.POST["password"]
                empresa.telefono = request.POST["telefono"]
                empresa.rif = request.POST["rif"]
                empresa.is_registered = True
                empresa.can_register = False
                user.save()
                empresa.save()
                login(request, user)
                return redirect("cliente_main", empresa.nombre)
            elif "user" in request.POST:
                try:
                    User.objects.get(username=request.POST["user"])
                    messages.error(
                        request,
                        "el nombre de usuario ya existe elija otro",
                        "lo sentimos",
                    )
                    existe = "disabled"
                except User.DoesNotExist:
                    existe = ""
                return render(
                    request,
                    "clientes/register.html",
                    {
                        "codigo": codigo,
                        "cuadro": "cuadro2",
                        "username": request.POST["user"],
                        "password": request.POST["password"],
                        "existe": existe,
                    },
                )
            else:
                return render(
                    request,
                    "clientes/register.html",
                    {"codigo": codigo, "cuadro": "cuadro1", "existe": "disabled"},
                )
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")
