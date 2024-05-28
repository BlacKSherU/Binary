from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=15, default="+000 0000000000")
    rif = models.CharField(max_length=10, default="v000000000")
    can_register = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    accountants = models.ManyToManyField(User, blank=True, related_name="accountant")

    def __str__(self):
        return self.nombre

    class Meta:
        permissions = [
            ("register_company", "Can register the company"),
        ]


class Cuenta_Bancaria(models.Model):
    class monedas(models.TextChoices):
        bolivares = "Bs"
        dolares = "$"

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=256)
    numero_cuenta = models.CharField(max_length=40)
    balance = models.FloatField()
    moneda = models.CharField(
        max_length=4, choices=monedas.choices, default=monedas.bolivares
    )

    def __str__(self):
        return self.nombre

    def update(self, monto):
        self.balance += monto

    def mostrar_balance(self):
        return str(round(self.balance, 2))


"""
class Categoria_Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripccion = models.TextField()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=256)
    descripccion = models.TextField()
    categorias = models.ManyToManyField(Categoria_Producto)
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()
    producto_antiguo = models.BooleanField()
    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    pass


class factura_cliente(models.Model):
    cuenta_bancaria = models.ForeignKey(Cuenta_Bancaria, on_delete=models.CASCADE)
    monto = models.FloatField()
    productos = models.ManyToManyField(Pedido)

class factura_proveedor(models.Model):
    pass
"""
