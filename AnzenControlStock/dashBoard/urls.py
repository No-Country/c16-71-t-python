from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="dashboard-inicio"),
    path("main/", views.main, name="dashboard-main"),
    path("registro/", views.registro, name="dashboard-registro"),
    path("registro2/<int:id_user>/", views.registro2, name="dashboard-registro2"),
    path("registro_empleado/", views.registro_empleado, name="dashboard-registro_empleado"),
    path("vista_empleados/", views.vista_empleados, name="dashboard-vista_empleados"),
    path('editar_empleado/', views.editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/', views.eliminar_empleado, name='eliminar_empleado')
]
