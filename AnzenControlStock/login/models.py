from django.db import models
from django.contrib.auth.models import AbstractUser

import os
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile

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
    foto_de_perfil = models.ImageField(upload_to="fotos/", null=True, blank=True)
    categoria_de_negocio= models.CharField(max_length=32)
    teléfono= models.IntegerField(null=True)
    correo_electrónico_de_la_empresa= models.CharField(max_length=32)

    def es_extension_valida(self):
        extensiones_validas = [".jpg", ".jpeg", ".png", ".gif"]
        return any(
            self.foto_perfil.name.lower().endswith(ext) for ext in extensiones_validas
        )

    # Genera un nombre único para el archivo utilizando UUID y conserva la extensión.
    @classmethod
    def generate_unique_filename(file):
        """
        Genera un nombre de archivo único para un archivo de imagen.

        Parámetros:
        - file (InMemoryUploadedFile): El archivo de imagen proporcionado desde el frontend,
                                        típicamente obtenido con request.FILES.get("id").

        Retorna:
        - SimpleUploadedFile: Un nuevo archivo de imagen con un nombre único generado.

        Uso en el Frontend:
        -   #Importar modulo Empresa
            foto_de_perfil = request.FILES.get("foto_de_perfil")    #Suponiendo que "foto_de_perfil"
                                                                    sea el id del input tipo file
            if foto_de_perfil:
                foto_de_perfil = Empresa.generate_unique_filename(foto_de_perfil) #Sobreescribir con el nombre generado

            #Por ultimo debe pasarse todos los datos (incluido foto_de_perfil) al metodo del backend para
            guardar todo en la base de datos
        """

        extension = os.path.splitext(file.name)[1]
        unique_name = f"{uuid.uuid4()}{extension}"
        return SimpleUploadedFile(unique_name, file.read())


class Empleado(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    rol = models.CharField(max_length=32)
