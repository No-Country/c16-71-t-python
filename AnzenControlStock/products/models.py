from django.db import models
from login.models import CustomUser
from django.db.models import Q

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


class Categoria(models.Model):
    nombre = models.CharField(max_length=32)


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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    # proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    @classmethod
    def create_producto(
        cls, user_empresa_id, nombre, descripcion, precio_unitario, stock, categoria_id
    ):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            categoria = Categoria.objects.get(id=categoria_id)
            producto = cls.objects.create(
                user_empresa=user_empresa,
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                stock=stock,
                categoria= categoria,
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
        categoria_id,
    ):
        try:
            producto = cls.objects.get(id=producto_id)
            categoria = Categoria.objects.get(id=categoria_id)

            # Actualizar el producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_unitario = precio_unitario
            producto.stock = stock
            producto.fecha_ingreso = fecha_ingreso
            producto.categoria = categoria
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

    @classmethod
    def filtrar_por_categoria(cls, productos, categoria_id):
        return productos.filter(categoria_id=categoria_id)

    @classmethod
    def filtrar_por_cantidad(cls, productos, cantidad_maxima):
        return productos.filter(stock__lte=cantidad_maxima)

    @classmethod
    def filtrar_por_texto(cls, productos, texto):
        return productos.filter(
            Q(nombre__icontains=texto) | Q(descripcion__icontains=texto)
        )

    @classmethod
    def filtrar(cls, productos, texto=None, por_cantidad=False, id_categoria=None):
        # Aplicar filtrado por texto
        if texto:
            productos = cls.filtrar_por_texto(productos, texto)

        # Aplicar filtrado por cantidad
        if por_cantidad:
            productos = cls.filtrar_por_cantidad(
                productos, 20
            )

        # Aplicar filtrado por categoría
        if id_categoria is not None:
            productos = cls.filtrar_por_categoria(productos, id_categoria)

        return productos
