from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string

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

    @classmethod
    def register(cls, nombre, email, password):
        """
    Este método crea un nuevo usuario en el sistema con el rol de empresa.

    :param nombre: El nombre completo del usuario.
    :type nombre: str
    :param email: La dirección de correo electrónico del usuario.
    :type email: str
    :param password: La contraseña para la cuenta del usuario.
    :type password: str
    :return: El objeto de usuario recién creado si el registro fue exitoso.
            -1 si la dirección de correo electrónico ya está en uso.
            -2 si ocurre algún error durante el registro.
        """
        if CustomUser.validate_email(email):
            try:
                username_aleatorio=''.join(random.choice(string.ascii_letters)
                                            for _ in range(30))
                usuario = CustomUser.objects.create_user(
                    username= username_aleatorio,
                    nombre= nombre,
                    email = email,
                    password = password,
                    es_empresa = True
                    )
                usuario.save()
                return usuario
            except Exception as e:
                return -2
        return -1

    @classmethod
    def validate_email(cls, email_a_validar):
        """
    Valida si un correo electrónico ya está registrado en la base de datos.

    :param email_a_validar: El correo electrónico que se va a validar.
    :type email_a_validar: str
    :return: True si el correo electrónico ya está registrado, False si no lo está.
    :rtype: bool
    """
        u = CustomUser.objects.all().filter(email = email_a_validar)
        print(u)
        if u is not None:
            return True
        return False


class Empresa(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombre_de_la_empresa= models.CharField(max_length=32)
    foto_de_perfil = models.ImageField(upload_to="fotos/", null=True, blank=True)#models.CharField(max_length=255, null=True, blank=True)
    categoria_de_negocio= models.CharField(max_length=32)
    teléfono= models.IntegerField(null=True)
    correo_electrónico_de_la_empresa= models.CharField(max_length=32)

    @classmethod
    def register(cls, user_id, nombre_de_la_empresa, foto_de_perfil,
                categoria_de_negocio, teléfono, correo_electrónico_de_la_empresa):
        """
    Registra una nueva empresa en el sistema.

    :param user_id: El ID del usuario al que está asociada la empresa.
    :type user_id: int
    :param nombre_de_la_empresa: El nombre de la empresa.
    :type nombre_de_la_empresa: str
    :param foto_de_perfil: La URL o la ruta de la foto de perfil de la empresa.
    :type foto_de_perfil: str
    :param categoria_de_negocio: La categoría de negocio a la que pertenece la empresa.
    :type categoria_de_negocio: str
    :param teléfono: El número de teléfono de contacto de la empresa.
    :type teléfono: str
    :param correo_electrónico_de_la_empresa: El correo electrónico de la empresa.
    :type correo_electrónico_de_la_empresa: str
    :return: La instancia de Empresa creada si el registro fue exitoso.
            -2 si ocurre algún error durante el registro.
        """
        try:
            foto_de_perfil_path = foto_de_perfil.name if foto_de_perfil else None
            empresa = Empresa.objects.create(
                user_id=user_id,
                nombre_de_la_empresa=nombre_de_la_empresa,
                foto_de_perfil=foto_de_perfil_path,
                categoria_de_negocio=categoria_de_negocio,
                teléfono=teléfono,
                correo_electrónico_de_la_empresa=correo_electrónico_de_la_empresa,
            )
            empresa.save()
            return empresa
        except Exception as e:
            print("Exception -> " + str(e))
            return -2

    def es_extension_valida(self, foto):
        """
        Verifica si la extensión de un archivo de imagen es válida.

        Parámetros:
        - self: La referencia a un objeto Empresa.
        - foto (InMemoryUploadedFile): El archivo de imagen que se va a verificar.

        Retorna:
        - bool: True si la extensión del archivo es válida, False de lo contrario.

        Uso:
        - Utiliza este método para validar si la extensión de un archivo de imagen es una de las permitidas.

        """
        extensiones_validas = [".jpg", ".jpeg", ".png", ".gif"]
        return any(
            self.foto_de_perfil.name.lower().endswith(ext) for ext in extensiones_validas
        )

    # Genera un nombre único para el archivo utilizando UUID y conserva la extensión.
    @classmethod
    def generate_unique_filename(cls, file):
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
