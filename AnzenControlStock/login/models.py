from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nombre= models.CharField(max_length=32)
    es_empresa = models.BooleanField(null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Empresa(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombre_de_la_empresa= models.CharField(max_length=32)
    foto_de_perfil= models.CharField(max_length=32)# sacar ? , o modificar depende la forma de ingresar la imagen en el front
    categoria_de_negocio= models.CharField(max_length=32)
    teléfono= models.IntegerField(null=True)
    correo_electrónico_de_la_empresa= models.CharField(max_length=32)


class Empleado(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    rol = models.CharField(max_length=32)


