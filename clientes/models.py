from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime


class monedas(models.TextChoices):
    bolivares = "Bs"
    dolares = "$"


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

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=256)
    numero_cuenta = models.CharField(max_length=40)
    balance = models.FloatField()
    moneda = models.CharField(
        max_length=4, choices=monedas.choices, default=monedas.bolivares
    )

    def __str__(self):
        return self.nombre


class Categoria_Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=256)
    descripcion = models.TextField()
    categorias = models.ManyToManyField(Categoria_Producto)
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()
    producto_antiguo = models.BooleanField()
    moneda = models.CharField(
        max_length=4, choices=monedas.choices, default=monedas.bolivares
    )

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()


class Factura_Cliente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    cuenta_bancaria = models.ForeignKey(Cuenta_Bancaria, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Pedido)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)

    def obtener_monto(self):
        monto = 0
        for producto in self.productos.all():
            monto += producto.producto.precio_venta * producto.cantidad
        return monto


class Factura_Proveedor(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    cuenta_bancaria = models.ForeignKey(Cuenta_Bancaria, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Pedido)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)

    def obtener_monto(self):
        monto = 0
        for producto in self.productos.all():
            monto -= producto.producto.precio_compra * producto.cantidad
        return monto
