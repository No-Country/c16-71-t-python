from django.urls import path
from .views import *

urlpatterns = [
    path('empleados/', EmpleadoList.as_view(), name='empleados'),
    path('empleado/<int:pk>/', EmpleadoDetail.as_view(), name='empleado'),
    path('crear_empleado/', EmpleadoCreate.as_view(), name='crear_empleado'),
    path('modificar_empleado/<int:pk>/', EmpleadoUpdate.as_view(), name='modificar_empleado'),
    path('borrar_empleado/<int:pk>/', EmpleadoDelete.as_view(), name='borrar_empleado'),
    
   
]