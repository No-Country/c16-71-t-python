from django.db import models

class Turno(models.Model):
    nombre = models.CharField(max_length=100)
    horario_inicio = models.TimeField()
    horario_salida = models.TimeField()

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre_completo = models.CharField(max_length=255)
    correo_electronico = models.EmailField()
    contraseña = models.CharField(max_length=255)  # Nota: La contraseña debería ser almacenada de manera segura, esto es solo un ejemplo.
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_inicio_empleo = models.DateField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_completo



