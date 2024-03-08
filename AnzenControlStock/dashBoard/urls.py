from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("dashboard/", views.main, name="dashboard"),
    path("registro/", views.registro, name="registro"),
    path("registro2/<int:id_user>/", views.registro2, name="registro2"),
    path("editar_perfil/", views.editar_perfil, name="editar_perfil"),
    path("eliminar_empresa/<int:id>/", views.eliminar_empresa, name="eliminar_empresa"),
    path("cerrar_sesion", views.cerrar_sesion, name="cerrar_sesion"),

    path("inventario/", views.inventario, name="inventario"),
    path("nuevo_producto/", views.crear_producto, name="nuevo_producto"),
    path("editar_producto/<int:id>/", views.editar_producto, name="editar_producto"),
    path("eliminar_producto/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
    path("vender_producto/<int:id>/", views.vender_producto, name="vender_producto"),
    path("comprar_producto/<int:id>/", views.comprar_producto, name="comprar_producto"),

    path("registro_empleado/", views.registro_empleado, name="registro_empleado"),
    path("vista_empleados/", views.vista_empleados, name="vista_empleados"),
    path('editar_empleado/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),

    path("proveedores/", views.proveedores, name="proveedores"),
    path("nuevo_proveedor/", views.crear_proveedor, name="nuevo_proveedor"),
    path("editar_proveedor/<int:id>/", views.editar_proveedor, name="editar_proveedor"),
    path("eliminar_proveedor/<int:id>/", views.eliminar_proveedor, name="eliminar_proveedor"),

]
