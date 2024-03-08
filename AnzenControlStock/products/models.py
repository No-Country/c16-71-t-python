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
    telefono = models.CharField(max_length=32)
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

    @classmethod
    def obtener_proveedores_por_empresa(cls, user_empresa_id):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            proveedores = cls.objects.filter(user_empresa=user_empresa)
            print("-------", proveedores)
            return proveedores
        except Exception as e:
            print("Exception -> " + str(e))
            return None


class Categoria(models.Model):
    nombre = models.CharField(max_length=32)


class Producto(models.Model):
    user_empresa = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    nombre= models.CharField(max_length=32)
    descripcion= models.CharField(max_length=100)
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
    def obtener_producto_por_id(cls, id_producto):
        try:
            producto = cls.objects.get(id=id_producto)
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

    @classmethod
    def agregar_cantidad(cls, producto_id, cantidad_a_agregar):
        try:
            producto = cls.objects.get(id=producto_id)
            producto.stock += cantidad_a_agregar
            producto.save()
            return producto
        except cls.DoesNotExist:
            raise Exception("El producto no existe.")

    @classmethod
    def quitar_cantidad(cls, producto_id, cantidad_a_quitar):
        try:
            producto = cls.objects.get(id=producto_id)

            # Verificar si la cantidad a quitar es mayor que la existencia actual
            if cantidad_a_quitar > producto.stock:
                return (
                    -1
                )  # Retorna -1 indicando que la cantidad a quitar es mayor que la existencia

            producto.stock -= cantidad_a_quitar
            producto.save()
            return producto
        except cls.DoesNotExist:
            raise Exception("El producto no existe.")


class Transaccion(models.Model):
    user_empresa = (
        models.ForeignKey(  # Usuaro de la empresa a la que pertenece el proveedor
            CustomUser,
            on_delete=models.CASCADE,
        )
    )
    user_empleado = models.IntegerField()
    nombre_producto = models.CharField(max_length=32)
    descripcion_producto = models.CharField(max_length=100)
    tipo_de_transaccion = models.CharField(max_length=32) #Compra o salida
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=100) #en compra: reposicion, en salida: venta o rotura
    fecha_y_hora = models.DateTimeField()

    def __str__(self):
        return "Transaccion de empresa dueño:"+self.user_empresa.nombre

    @classmethod
    def create_transaccion(
        cls,
        user_empresa_id,
        user_empleado,
        nombre_producto,
        descripcion_producto,
        tipo_de_transaccion,
        cantidad,
        descripcion,
    ):
        try:
            user_empresa = CustomUser.objects.get(id=user_empresa_id)
            print("Empleado a utilizar,", user_empleado)
            transaccion = cls.objects.create(
                user_empresa=user_empresa,
                user_empleado=user_empleado,
                nombre_producto=nombre_producto,
                descripcion_producto=descripcion_producto,
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
            print("------- empresa:", user_empresa.nombre)
            transacciones = cls.objects.filter(user_empresa=user_empresa)
            print("------- transacciones:", transacciones)
            todas = cls.objects.all()
            print("------- todas:",todas)
            return transacciones
        except Exception as e:
            print("Exception -> " + str(e))
            return None

    def obtener_empleado_nombre(self):
        try:
            empleado = Empleado.objects.get(user_id=self.user_empleado)
            print("Empleado -> ", empleado.user.nombre)
            return empleado.user.nombre
        except Empleado.DoesNotExist:
            return "Empleado no encontrado"
