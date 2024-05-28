from django.shortcuts import render
from django.http import HttpRequest
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
import string
import random
from clientes.models import Empresa


# Create your views here.
def inicio(request: HttpRequest):
    if request.method == "POST":
        """try:
            User.objects.get(email=request.POST["registro-email"])
            existe = True
            messages.error(request, "el correo ya esta registrado", "lo sentimos")
        except User.DoesNotExist:
            existe = False"""
        try:
            Empresa.objects.get(telefono=request.POST["registro-telefono"])
            existe = True
            messages.error(request, "el telefono ya esta registrado", "lo sentimos")
        except Empresa.DoesNotExist:
            """if not existe:"""
            existe = False
        try:
            Empresa.objects.get(nombre=request.POST["registro-nombre"])
            existe = True
            messages.error(request, "el nombre ya esta registrado", "lo sentimos")
        except Empresa.DoesNotExist:
            if not existe:
                existe = False
        if not existe:
            send_mail(
                "Bienvenido a Binary",
                "hola "
                + request.POST["registro-nombre"]
                + "  porfavor envie su comprobante de pago al correo firmbanibary@gmail.com una vez realizado el pago tedra acceso al sistema",
                request.POST["registro-email"],
                [
                    request.POST["registro-email"],
                ],
                fail_silently=False,
            )
            while True:
                random_name = "".join(
                    [
                        random.choice(string.ascii_letters + string.digits)
                        for i in range(16)
                    ]
                )
                try:
                    User.objects.get(username=random_name)
                    existe = True
                except User.DoesNotExist:
                    existe = False
                if not existe:
                    break
            usuario = User.objects.create_user(
                random_name,
                request.POST["registro-email"],
                random_name,
            )
            Empresa.objects.create(
                user=usuario,
                nombre=request.POST["registro-nombre"],
                telefono=request.POST["registro-telefono"],
            )
            messages.success(request, "solicitud enviada con exito 🥵", "felicidades")
        return render(request, "inicio/index.html")
    else:
        return render(request, "inicio/index.html")


def no_lo_olvides(request: HttpRequest):
    return render(request, "inicio/noloolvides.html")
