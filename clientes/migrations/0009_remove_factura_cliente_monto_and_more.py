# Generated by Django 5.0.4 on 2024-06-01 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_factura_cliente_fecha_factura_proveedor_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura_cliente',
            name='monto',
        ),
        migrations.RemoveField(
            model_name='factura_proveedor',
            name='monto',
        ),
    ]
