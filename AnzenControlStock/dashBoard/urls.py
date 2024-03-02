from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="dashboard-inicio"),
    path("main/", views.main, name="dashboard-main"),
    path("registro/", views.registro, name="dashboard-registro"),
    path("registro2/<int:id_user>/", views.registro2, name="dashboard-registro2"),
    path("registro_empleado/", views.registro, name="dashboard-registro_empleado"),
    path("rvista_empleados/", views.registro, name="dashboard-vista_empleados"),
]
