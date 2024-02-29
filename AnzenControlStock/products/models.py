from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=32)
    telefono = models.IntegerField()
    correo = models.CharField(max_length=32)

    @classmethod
    def crear_proveedor(cls, nombre, telefono, correo):
        proveedor = cls(nombre=nombre, telefono=telefono, correo=correo)
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
    nombre= models.CharField(max_length=32)
    descripcion= models.CharField(max_length=32)
    precio_unitario = models.IntegerField()
    stock= models.IntegerField()
    fecha_ingreso= models.DateTimeField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    @classmethod
    def create_producto(
        cls, nombre, descripcion, precio_unitario, stock, fecha_ingreso, proveedor_id
    ):
        try:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            producto = cls.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                stock=stock,
                fecha_ingreso=fecha_ingreso,
                proveedor=proveedor,
            )
            return producto
        except Proveedor.DoesNotExist:
            raise Exception("El proveedor no existe.")

    @classmethod
    def actualizar_producto(
        cls,
        producto_id,
        nombre,
        descripcion,
        precio_unitario,
        stock,
        fecha_ingreso,
        proveedor_id,
    ):
        try:
            producto = cls.objects.get(id=producto_id)
            proveedor = Proveedor.objects.get(id=proveedor_id)

            # Verificar si el proveedor existe
            if proveedor is None:
                raise Exception("El proveedor no existe.")

            # Actualizar el producto con el nuevo proveedor
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_unitario = precio_unitario
            producto.stock = stock
            producto.fecha_ingreso = fecha_ingreso
            producto.proveedor = proveedor
            producto.save()

            return producto
        except cls.DoesNotExist:
            raise Exception("El producto no existe.")

    def eliminar_producto(self):
        self.delete()

    @classmethod
    def filter_by_proveedor(cls, proveedor_id):
        try:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            productos = cls.objects.filter(proveedor=proveedor)
            return productos
        except Proveedor.DoesNotExist:
            raise Exception("El proveedor no existe.")
