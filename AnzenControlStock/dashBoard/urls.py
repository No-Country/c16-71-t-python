from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("dashboard/", views.main, name="dashboard"),
    path("registro/", views.registro, name="registro"),
    path("registro2/<int:id_user>/", views.registro2, name="registro2"),
    path("cerrar_sesion", views.cerrar_sesion, name="cerrar_sesion"),
    path("inventario/", views.inventario, name="inventario"),
    path("nuevo_producto", views.crear_producto, name="nuevo_producto"),
]
