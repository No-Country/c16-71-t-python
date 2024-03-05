from django.db import models

# Create your models here.
class Empleado(models.Model):
    nombreEmpleado=models.CharField(max_length=32)
    mailEmpleado=models.CharField(max_length=32)
    telefonoEmpleado=models.IntegerField()
    password=models.CharField(max_length=32
                        
    @classmethod
    def actualizar_empleado(
        cls,
        nombreEmpleado,
        mailEmpleado,
        telefonoEmpleado,
        password,
        
    ):
    
        except cls.DoesNotExist:
            raise Exception("El Empleado no esta registrado.")
                        

    def eliminar_producto(self):
            self.delete()
    

