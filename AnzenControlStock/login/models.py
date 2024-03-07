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
    def register(cls, nombre, email, password, es_empresa):
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
                    es_empresa = es_empresa
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

    @classmethod
    def obtener_usuario_por_id(cls, id_usuario):
        try:
            usuario = cls.objects.get(id=id_usuario)
            return usuario
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def modificar_usuario(cls,user_id , nombre, email, password):      
        try:
            user = cls.objects.get(id=user_id)
            # Actualizar el usuario
            if CustomUser.validate_email(email):
                user.email = email
            else:
                return -1  
            user.nombre = nombre
            user.set_password = password
            user.save()
            return user
        except cls.DoesNotExist:
            raise Exception("El usuario no existe.")
        except Exception as e :
            return -2
        
    def eliminar_usuario(self):
        self.delete()



class Empresa(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombre_de_la_empresa= models.CharField(max_length=32)
    categoria_de_negocio= models.CharField(max_length=32)
    teléfono= models.IntegerField(null=True)
    correo_electrónico_de_la_empresa= models.CharField(max_length=32)

    @classmethod
    def register(cls, user_id, nombre_de_la_empresa, categoria_de_negocio,
                teléfono, correo_electrónico_de_la_empresa):
        """
    Registra una nueva empresa en el sistema.

    :param user_id: El ID del usuario al que está asociada la empresa.
    :type user_id: int
    :param nombre_de_la_empresa: El nombre de la empresa.
    :type nombre_de_la_empresa: str
    :param foto_de_perfil: La URL o la ruta de la foto de perfil de la empresa.
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
            empresa = Empresa.objects.create(
                user_id=user_id,
                nombre_de_la_empresa=nombre_de_la_empresa,
                categoria_de_negocio=categoria_de_negocio,
                teléfono=teléfono,
                correo_electrónico_de_la_empresa=correo_electrónico_de_la_empresa,
            )
            empresa.save()
            return empresa
        except Exception as e:
            print("Exception -> " + str(e))
            return -2
    
    @classmethod
    def obtener_empresa_por_id(cls, id_usuario):
        try:
            empresa = cls.objects.get(user=id_usuario)
            return empresa
        except cls.DoesNotExist:
            return None

    @classmethod
    def modificar_empresa(cls,user_id , nombre_de_la_empresa, categoria_de_negocio,
                          teléfono, correo_electrónico_de_la_empresa):      
        try:
            empresa = cls.objects.get(user_id=user_id)

            # Actualizar la empresa
            empresa.nombre_de_la_empresa = nombre_de_la_empresa
            empresa.categoria_de_negocio = categoria_de_negocio
            empresa.teléfono = teléfono
            empresa.correo_electrónico_de_la_empresa = correo_electrónico_de_la_empresa
            empresa.save()
            return empresa     
        except cls.DoesNotExist:
            raise Exception("El usuario no existe.")
        except Exception as e :
            return -2
        
    def eliminar_empresa(self):
        self.delete()

class Empleado(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    telefono = models.IntegerField(null=True)
    rol = models.CharField(max_length=32)
    id_empresa = models.IntegerField(null=True)

    @classmethod
    def register(cls, user_id, rol,telefono , id_user_empresa):
        """
    :return: La instancia de empleado creada si el registro fue exitoso.
            -2 si ocurre algún error durante el registro.
        """
        try:
            empleado = Empleado.objects.create(
                user_id=user_id,
                rol=rol,
                telefono=telefono,
                id_empresa = id_user_empresa
            )
            empleado.save()
            return empleado
        except Exception as e:
            print("Exception -> " + str(e))
            return -2
    
    @classmethod
    def obtener_empleado_por_id(cls, id_usuario):
        try:
            empleado = cls.objects.get(user=id_usuario)
            return empleado
        except cls.DoesNotExist:
            return None

    @classmethod
    def modificar_empleado(cls,user_id , rol, telefono):      
        try:
            empleado = cls.objects.get(id=user_id)

            # Actualizar la empresa
            empleado.rol = rol
            empleado.telefono = telefono
            empleado.save()
            return empleado     
        except cls.DoesNotExist:
            raise Exception("El usuario no existe.")
        except Exception as e :
            return -2
        
    def eliminar_empleado(self):
        self.delete()

    @classmethod
    def obtener_empleado_por_empresa(cls, user_empresa_id):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            empleados = cls.objects.filter(id_empresa=user_empresa.id)
            return empleados
        except Exception as e:
            print("Exception -> " + str(e))
            return None

    @classmethod
    def obtener_empleado_por_id_y_empresa(cls, id_empleado, id_user_empresa):
        try:
            empleado = cls.objects.get(user_id=id_empleado, id_empresa=id_user_empresa)
            return empleado
        except cls.DoesNotExist:
            return None