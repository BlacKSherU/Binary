from django.shortcuts import render
from django.http import HttpRequest


# Create your views here.
def register(request: HttpRequest, codigo):
    return render(request, "clientes/felicidades.html", {"codigo": codigo})
