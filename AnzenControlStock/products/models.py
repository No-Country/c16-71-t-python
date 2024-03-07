from django.db import models
from login.models import CustomUser, Empleado
from django.db.models import Q
from datetime import datetime

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
    def crear_proveedor(cls, user_empresa_id, nombre, telefono, correo):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            proveedor = cls(user_empresa=user_empresa, nombre=nombre, telefono=telefono, correo=correo)
            proveedor.save()
            return proveedor
        except Exception as e:
            print("Exception -> " + str(e))
            return -2

    @classmethod
    def actualizar_proveedor(cls, id_proveedor, nombre, telefono, correo):
        proveedor = cls.objects.get(id=id_proveedor)
        proveedor.nombre = nombre
        proveedor.telefono = telefono
        proveedor.correo = correo
        proveedor.save()

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
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    @classmethod
    def create_producto(
        cls, user_empresa_id, nombre, descripcion, precio_unitario, stock, categoria_id, proveedor_id
    ):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            categoria = Categoria.objects.get(id=categoria_id)
            proveedor = Proveedor.objects.get(id=proveedor_id)
            print("Proveedor a utilizar,", proveedor)
            producto = cls.objects.create(
                user_empresa=user_empresa,
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                stock=stock,
                categoria= categoria,
                proveedor = proveedor,
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
        proveedor_id,
    ):
        try:
            producto = cls.objects.get(id=producto_id)
            categoria = Categoria.objects.get(id=categoria_id)
            proveedor = Proveedor.objects.get(id=proveedor_id)

            # Actualizar el producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_unitario = precio_unitario
            producto.stock = stock
            producto.fecha_ingreso = fecha_ingreso
            producto.categoria = categoria
            producto.proveedor = proveedor
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
            print("-------", productos)
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
        result = productos.filter(
            Q(nombre__icontains=texto) | Q(descripcion__icontains=texto)
        )
        # print("Resultado de busqueda del texto ", result)
        return result

    @classmethod
    def filtrar(cls, productos, texto=None, por_cantidad=False, id_categoria=None):
        # Inicia con todos los productos
        filtrados = productos

        # Aplicar filtrado por texto
        if texto:
            filtrados = cls.filtrar_por_texto(filtrados, texto)
            print("Resultado de busqueda del texto ", filtrados)

        # Aplicar filtrado por cantidad
        if por_cantidad==2:
            filtrados = cls.filtrar_por_cantidad(filtrados, 0)
            print("Resultado de busqueda de cantidad ", filtrados)
        elif por_cantidad:
            filtrados = cls.filtrar_por_cantidad(filtrados, 10)
            print("Resultado de busqueda de cantidad ", filtrados)

        # Aplicar filtrado por categoría
        if id_categoria is not None:
            filtrados = cls.filtrar_por_categoria(filtrados, id_categoria)
            print("Resultado de busqueda de categoria ", filtrados)

        return filtrados
    
class Transaccion(models.Model):
    user_empresa = (
        models.ForeignKey(  # Usuaro de la empresa a la que pertenece el proveedor
            CustomUser,
            on_delete=models.CASCADE,
        )
    )
    user_empleado = (
        models.ForeignKey(  # El empleado que hace el movimiento
            Empleado,
            on_delete=models.CASCADE,
        )
    )
    tipo_de_transaccion = models.CharField(max_length=32)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=32)
    fecha_y_hora = models.DateTimeField()

    @classmethod
    def create_transaccion(
        cls, user_empresa_id, user_empleado_id, tipo_de_transaccion, cantidad, descripcion, 
    ):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            user_empleado = Empleado.objects.get(user_id=user_empleado_id)
            print("Empleado a utilizar,", user_empleado.nombre)
            transaccion = cls.objects.create(
                user_empresa=user_empresa,
                user_empleado=user_empleado,
                tipo_de_transaccion=tipo_de_transaccion,
                cantidad=cantidad,
                descripcion=descripcion,
                fecha_y_hora = datetime.now()
            )
            return transaccion
        except Exception as e:
            print("Exception -> " + str(e))
            return -2
        
    @classmethod
    def obtener_transaccion_por_empresa(cls, user_empresa_id):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            transacciones = cls.objects.filter(user_empresa=user_empresa)
            print("-------", transacciones)
            return transacciones
        except Exception as e:
            print("Exception -> " + str(e))
            return None