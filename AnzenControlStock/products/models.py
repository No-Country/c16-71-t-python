from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre= models.CharField(max_length=32)
    descripcion= models.CharField(max_length=32)
    precio_unitario = models.IntegerField()
    stock= models.IntegerField()
    fecha_ingreso= models.DateTimeField()
    proveedor = models.CharField(max_length=32)

class Proveedor(models.Model):
    nombre=models.CharField(max_length=32)
    telefono=models.IntegerField()
    correo=models.CharField(max_length=32)