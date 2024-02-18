from django.contrib import admin
from .models import CustomUser, Empleado, Empresa

# Register your models here.

admin.site.register(Empleado)
admin.site.register(CustomUser)
admin.site.register(Empresa)