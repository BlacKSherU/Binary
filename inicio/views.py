from django.shortcuts import render
from django.http import HttpRequest
from django.core.mail import send_mail


# Create your views here.
def inicio(request: HttpRequest):
    if request.method == "POST":
        print(
            "hola" + request.POST["registro-telefono"] + request.POST["registro-nombre"]
        )
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
        return render(request, "inicio/index.html")
    else:
        return render(request, "inicio/index.html")
