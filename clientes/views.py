from django.shortcuts import render, redirect
from django.http import HttpRequest
from clientes.models import Empresa
from django.contrib.auth.models import User


# Create your views here.
def register(request: HttpRequest, codigo):
    print(codigo)
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
        if empresa.Empresa_registrada:
            return render(request, "clientes/felicidades.html", {"codigo": codigo})
        else:
            return redirect("inicio")
    else:
        return redirect("inicio")
