from django.db import models
from login.models import CustomUser
from django.utils import timezone

class Proveedor(models.Model):
    user_empresa = (
        models.ForeignKey(  # Usuaro de la empresa a la que pertenece el proveedor
            CustomUser,
            on_delete=models.CASCADE,
        )
    )
    nombre = models.CharField(max_length=32)
    telefono = models.IntegerField()
    correo = models.CharField(max_length=32)

    @classmethod
    def crear_proveedor(cls, user_empresa, nombre, telefono, correo):
        proveedor = cls(user_empresa=user_empresa, nombre=nombre, telefono=telefono, correo=correo)
        proveedor.save()
        return proveedor

    def actualizar_proveedor(self, nombre, telefono, correo):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.save()

    def eliminar_proveedor(self):
        self.delete()


class Producto(models.Model):
    user_empresa = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    nombre= models.CharField(max_length=32)
    descripcion= models.CharField(max_length=32)
    precio_unitario = models.IntegerField()
    stock= models.IntegerField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    # proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    @classmethod
    def create_producto(
        cls, user_empresa_id, nombre, descripcion, precio_unitario, stock
    ):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            producto = cls.objects.create(
                user_empresa=user_empresa,
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                stock=stock,
            )
            return producto
        except Exception as e:
            print("Exception -> " + str(e))
            return -2

    @classmethod
    def actualizar_producto(
        cls,
        producto_id,
        nombre,
        descripcion,
        precio_unitario,
        stock,
        fecha_ingreso,
    ):
        try:
            producto = cls.objects.get(id=producto_id)

            # Actualizar el producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_unitario = precio_unitario
            producto.stock = stock
            producto.fecha_ingreso = fecha_ingreso
            producto.save()

            return producto
        except cls.DoesNotExist:
            raise Exception("El producto no existe.")

    def eliminar_producto(self):
        self.delete()

    @classmethod
    def obtener_productos_por_empresa(cls, user_empresa_id):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            productos = cls.objects.filter(user_empresa=user_empresa)
            return productos
        except Exception as e:
            print("Exception -> " + str(e))
            return None

    @classmethod
    def obtener_producto_por_id_y_empresa(cls, id_producto, id_user_empresa):
        try:
            producto = cls.objects.get(id=id_producto, user_empresa_id=id_user_empresa)
            return producto
        except cls.DoesNotExist:
            return None
