from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Empleado(User):
    rol= models.CharField(max_length=32)
    fecha_ingreso= models.DateTimeField()

class Empresa(User):
    nombre_de_la_empresa= models.CharField(max_length=32)
    foto_de_perfil= models.CharField(max_length=32)# sacar ?
    categoria_de_negocio= models.CharField(max_length=32)
    teléfono= models.IntegerField()
    correo_electrónico_de_la_empresa= models.CharField(max_length=32)
