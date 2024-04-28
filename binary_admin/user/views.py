from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def prueba(request):
    return render(request, "helloworld.html")


def register(request: HttpRequest):
    if request.method == "POST":
        try:
            User.objects.get(username=request.POST["user"])
        except User.DoesNotExist:
            no_existe = True
        else:
            no_existe = False
            messages.error(
                request,
                "El nombre de usuario ya existe elija otro",
                "usuario_existente",
            )
        try:
            User.objects.get(email=request.POST["email"])
        except User.DoesNotExist:
            if no_existe:
                no_existe = True
        else:
            no_existe = False
            messages.error(
                request,
                "El correo ya se encuentra registrado elija otro",
                "correo_existente",
            )
        if no_existe:
            u = User.objects.create_user(
                username=request.POST["user"],
                password=request.POST["password"],
                email=request.POST["email"],
            )
            messages.success(request, "usuario creado con exito")
            login(request, u)
            return redirect("prueba")
        else:
            return render(request, "binary_admin/user/register.html")
    else:
        return render(request, "binary_admin/user/register.html")
