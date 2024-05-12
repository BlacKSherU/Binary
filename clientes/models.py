from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=15, default="+000 0000000000")
    Empresa_registrada = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("register_company", "Can register the company"),
        ]
