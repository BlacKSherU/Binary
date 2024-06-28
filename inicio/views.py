from django.shortcuts import render
from django.http import HttpRequest
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
import string
import random
from clientes.models import Empresa
import datetime


# Create your views here.
def inicio(request: HttpRequest):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST["registro-email"])
            existe = True
            messages.error(request, "el correo ya esta registrado", "lo sentimos")
        except User.DoesNotExist:
            existe = False
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
                last_name=request.POST["marialadilla"]
            )
            empresaXD = Empresa.objects.create(
                user=usuario,
                nombre=request.POST["registro-nombre"],
                telefono=request.POST["registro-telefono"],
            )
            send_mail(
                "Envío de Factura y Métodos de Pago",
                f"""Estimado/a {request.POST['registro-nombre']}, Se adjunta a este correo la factura correspondiente a los servicios solicitados a Binary CA.

Factura N.º: {empresaXD.id}
Monto: 100$
Fecha de Vencimiento: {(datetime.datetime.now() + datetime.timedelta(days=10)).date()}

Para su conveniencia, a continuación, detallamos los métodos de pago disponibles:
o	Transferencia bancaria / Pago Movil:
o	Banco: Banesco
o	BINARY CA
o	RIF: J-89457109
o	Telefono: 04129872828
o	Pago con tarjeta de crédito: Puede realizar el pago a través de nuestro portal seguro en [URL del Portal de Pago].
o	Pago en divisas:
o	Zelle 
o	firmabinary@gmail.com 

Una vez realizado el pago, envíe el comprobante correspondiente a firmabinary@gmail.com Esto nos permitirá verificar el pago y completar su proceso de configuración de su acceso al sistema de Binary CA

Si tiene alguna pregunta o necesita asistencia adicional, no dude en ponerse en contacto con nosotros.

Gracias por su atención y cooperación.
Saludos cordiales,
El equipo de Binary CA

Política de Privacidad y Seguridad | Términos y Condiciones | Contáctanos
Binary CA
Calle 23 entre carreras 17 y 18 Torre Binary. 
Municipio Iribarren. Barquisimeto. Estado Lara. Venezuela

""",
                request.POST["registro-email"],
                [
                    request.POST["registro-email"],
                ],
                fail_silently=False,
            )
            messages.success(request, "solicitud enviada con exito 🥵", "felicidades")
        return render(request, "inicio/index.html")
    else:
        return render(request, "inicio/index.html")


def no_lo_olvides(request: HttpRequest):
    return render(request, "inicio/noloolvides.html")


def emailprueba(request):
    return render(request, "emails/email1.html")
