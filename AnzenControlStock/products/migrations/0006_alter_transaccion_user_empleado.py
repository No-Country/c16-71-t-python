# Generated by Django 4.2 on 2024-03-08 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_proveedor_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='user_empleado',
            field=models.CharField(max_length=32),
        ),
    ]
