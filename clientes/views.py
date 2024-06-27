from django.shortcuts import render, redirect
from django.http import HttpRequest
from clientes.models import (
    Empresa,
    Cuenta_Bancaria,
    Factura_Cliente,
    Factura_Proveedor,
    Producto,
    Pedido,
    Categoria_Producto,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from operator import attrgetter
from itertools import chain
import datetime


# Create your views here.
def prueba(user):
    return False


# ---------------------------main---------------------------
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


# ---------------------------cuentas---------------------------
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


# ---------------------------cuentas agregar---------------------------
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


# ---------------------------cuentas editar ---------------------------
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


# ---------------------------cuentas eliminar ---------------------------
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


# --------------------------- registrar empresa ---------------------------
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


# ---------------------------facturas ---------------------------
@login_required(login_url="login")
def facturas(request: HttpRequest, empresa_nombre):
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
                facturas_cliente = Factura_Cliente.objects.filter(empresa=empresa)
                facturas_proveedor = Factura_Proveedor.objects.filter(empresa=empresa)
                productos = Producto.objects.filter(empresa=empresa)
                facturas = sorted(
                    chain(facturas_cliente, facturas_proveedor),
                    key=attrgetter("fecha"),
                    reverse=True,
                )
                return render(
                    request,
                    "clientes/facturas.html",
                    {
                        "empresa": empresa,
                        "facturas": facturas,
                        "productos": productos,
                        "cuentas": cuentas,
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
def agregar_factura(request: HttpRequest, empresa_nombre):
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
                    if request.POST["tipo"] == "cliente":
                        factura = Factura_Cliente.objects.create(
                            empresa=empresa,
                            cuenta_bancaria=Cuenta_Bancaria.objects.get(
                                id=request.POST["banco"]
                            ),
                            fecha=datetime.datetime.now(),
                        )
                        productos = request.POST.getlist("producto")
                        cantidades = request.POST.getlist("productocantidad")
                        for i in range(len(productos)):
                            pedido = Pedido.objects.filter(
                                empresa=empresa,
                                producto=Producto.objects.get(id=productos[i]),
                                cantidad=cantidades[i],
                            )
                            if not pedido:
                                pedido = Pedido.objects.create(
                                    empresa=empresa,
                                    producto=Producto.objects.get(id=productos[i]),
                                    cantidad=cantidades[i],
                                )
                            else:
                                pedido = pedido[0]
                            factura.productos.add(pedido)
                    else:
                        factura = Factura_Proveedor.objects.create(
                            empresa=empresa,
                            cuenta_bancaria=Cuenta_Bancaria.objects.get(
                                id=request.POST["banco"]
                            ),
                            fecha=datetime.datetime.now(),
                        )
                        productos = request.POST.getlist("producto")
                        cantidades = request.POST.getlist("productocantidad")
                        for i in range(len(productos)):
                            pedido = Pedido.objects.filter(
                                empresa=empresa,
                                producto=Producto.objects.get(id=productos[i]),
                                cantidad=cantidades[i],
                            )
                            if not pedido:
                                pedido = Pedido.objects.create(
                                    empresa=empresa,
                                    producto=Producto.objects.get(id=productos[i]),
                                    cantidad=cantidades[i],
                                )
                            else:
                                pedido = pedido[0]
                            factura.productos.add(pedido)
                    cuenta_bancaria = Cuenta_Bancaria.objects.get(
                        id=request.POST["banco"]
                    )
                    cuenta_bancaria.balance += factura.obtener_monto()
                    cuenta_bancaria.save()

                return redirect("facturas", empresa.nombre)
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


# ---------------------------productos---------------------------
@login_required(login_url="login")
def productos(request: HttpRequest, empresa_nombre):
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
                productos = Producto.objects.filter(empresa=empresa)
                categorias = Categoria_Producto.objects.filter(empresa=empresa)
                return render(
                    request,
                    "clientes/productos.html",
                    {
                        "empresa": empresa,
                        "productos": productos,
                        "categorias": categorias,
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
def agregar_categoria(request: HttpRequest, empresa_nombre):
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
                    if Categoria_Producto.objects.filter(
                        empresa=empresa, nombre=request.POST["nombre"]
                    ):
                        messages.error(request, "cagaste", "lo sentimos")
                    else:
                        Categoria_Producto.objects.create(
                            empresa=empresa,
                            nombre=request.POST["nombre"],
                            descripcion=request.POST["descripcion"],
                        )
                        messages.success(
                            request, "categoria agregada con exito", "felicidades"
                        )
                return redirect("productos", empresa.nombre)
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")


@login_required(login_url="login")
def agregar_producto(request: HttpRequest, empresa_nombre):
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
                    if Producto.objects.filter(nombre=request.POST["nombre"]):
                        messages.error(request, "cagaste", "lo sentimos")
                    else:
                        producto = Producto.objects.create(
                            empresa=empresa,
                            nombre=request.POST["nombre"],
                            descripcion=request.POST["descripcion"],
                            precio_compra=request.POST["precio_compra"],
                            precio_venta=request.POST["precio_venta"],
                            producto_antiguo=False,
                        )
                        for categoria in request.POST.getlist("categorias"):
                            producto.categorias.add(
                                Categoria_Producto.objects.get(id=categoria)
                            )
                        producto.save()
                        messages.success(
                            request, "producto agregado con exito", "felicidades"
                        )
                return redirect("productos", empresa.nombre)
            else:
                messages.error(request, "no tiene acceso tontito", "bobito")
                return redirect(reverse("login") + "?next=" + request.path)
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")
