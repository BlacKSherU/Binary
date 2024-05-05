from django.shortcuts import render


# Create your views here.
def prueba(request):
    return render(request, "base/base.html")


def main(request):
    return render(request, "binary_admin/main/index.html")
