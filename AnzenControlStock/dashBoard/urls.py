from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("dashboard/", views.main, name="dashboard"),
    path("registro/", views.registro, name="registro"),
    path("registro2/<int:id_user>/", views.registro2, name="registro2"),
    path("editar_perfil/", views.editar_perfil, name="editar_perfil"),
    path("cerrar_sesion", views.cerrar_sesion, name="cerrar_sesion"),
    path("inventario/", views.inventario, name="inventario"),
    path("nuevo_producto/", views.crear_producto, name="nuevo_producto"),
    path("editar_producto/<int:id>/", views.editar_producto, name="editar_producto"),
    path("eliminar_producto/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
    path("proveedores/", views.proveedores, name="proveedores"),
]
