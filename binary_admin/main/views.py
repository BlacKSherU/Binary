from django.shortcuts import render


# Create your views here.
def prueba(request):
    return render(request, "helloworld.html")


def main(request):
    return render(request, "binary_admin/main/index.html")
