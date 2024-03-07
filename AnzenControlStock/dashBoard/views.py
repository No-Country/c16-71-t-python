from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from login.models import CustomUser, Empresa, Empleado
from products.models import Producto, Categoria, Proveedor

from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model

# Create your views here.


def inicio(request):
    if request.method == 'POST':
        usuario = authenticate(
            request,
            email=request.POST["email"],
            password=request.POST["password"]
        )

        if usuario is not None:
            login(request, usuario)

            if usuario.es_empresa == True:
                request.session["id_user"] = usuario.id
                print ("Sesion iniciada "+ str(request.session.get("id_user")))
                messages.success(request, "Sesión iniciada correctamente")
                return redirect("dashboard")
            else:
                request.session["id_user"] = usuario.id
                print ("Sesion iniciada "+ str(request.session.get("id_user")))
                messages.success(request, "Sesión iniciada correctamente")
                return redirect("dashboard")


        else:
            messages.error(request, "Error, verifique sus datos")
            return redirect("inicio")
    else:
        return render(request, 'login/inicio.html')


def registro(request):
    if request.method == 'GET':
        return render(request, 'login/registro.html')
    if request.method == 'POST':
        # verificaciones
        if request.POST['password1'] == request.POST['password2'] and request.POST['nombre'] and request.POST['email']:
            new_user = CustomUser.register(request.POST['nombre'], request.POST['email'], request.POST['password1'], True)
            if new_user == -1:
                print("El correo ya existe, mostrar un mensaje de error con toast")
                messages.error(request, "Error, el email utilizado ya existe")
                return redirect("registro")
            elif new_user == -2:
                print("Ocurrio un error durante el registro")
                messages.error(request, "Ocurrio un error durante el registro")
                return redirect("registro")
            else:
                print("El usuario ",new_user.nombre, "fue creado")
                return redirect("registro2", id_user=new_user.id) #Se le pasa el name del url
        else:
            messages.error(request, "Error, las contraseñas no son iguales")
            return redirect("registro")

def registro2(request,id_user):
    if request.method == 'GET':
        return render(
            request,
            "login/registro2.html",
            {"id_user": id_user},
        )
    if request.method == 'POST':
        print("POST*********",request.POST)

        new_empresa = Empresa.register(
            request.POST['id_user'],
            request.POST['nombre_de_empresa'],
            request.POST['categoria_de_negocio'],
            request.POST['teléfono'],
            request.POST['correo_electrónico_de_la_empresa']
        )

        if new_empresa == -2:
            print("Ocurrio un error")
            messages.error(request, "Ocurrio un error")
            return redirect("registro2", id_user=id_user)
        else:
            print("Se creo la empresa", new_empresa.nombre_de_la_empresa)
            # Iniciar sesion automaticamente
            request.session["id_user"] = id_user
            print ("Sesion iniciada "+ str(request.session.get("id_user")))
            messages.success(request, "Sesión iniciada correctamente")
            return redirect("dashboard")


def editar_perfil(request):
    id_user = request.session.get("id_user")

    if request.method == "GET":
        if id_user:
            usuario = CustomUser.obtener_usuario_por_id(id_user)
            empresa = Empresa.obtener_empresa_por_id(id_user)
            data = {"empresa": empresa, "usuario": usuario}
            return render(request, "login/perfil.html", data)
        else:
            return redirect("inicio")

    usuario = CustomUser.obtener_usuario_por_id(id_user)
    empresa = Empresa.obtener_empresa_por_id(id_user)
    data = {"empresa": empresa, "usuario": usuario}

    if request.method == "POST":
        if request.POST["password1"] != request.POST["password2"]:

            messages.error(request, "Error, las contraseñas no son iguales")
            return render(request, "login/perfil.html", data)
        else:
            user_actualizado = CustomUser.modificar_usuario(id_user,
                request.POST["nombre"],
                request.POST["email"],
                request.POST["password1"]
            )
            print("usuario editado: " + user_actualizado.nombre)
            if user_actualizado == 1 :
                messages.error(request, "El mail ya esta en uso")
            elif user_actualizado == 2 :
                messages.error(request, "Error en la modificacion de usuario")
            else:
                empresa_actualizada = Empresa.modificar_empresa(id_user,
                request.POST["nombreEmpresa"],
                request.POST["categoriaNegocio"],
                request.POST["telefono"],
                request.POST["correoElectronico"])
                if empresa_actualizada == -2:
                    messages.error(request, "Error, las contraseñas no son iguales")
                    return render(request, "login/perfil.html", data)
                else:
                    messages.success(request, "Se modifico el perfil correctamente")
                    return redirect("dashboard")


def cerrar_sesion(request):
    request.session["id_user"] = None
    return redirect("inicio")


def main(request):
    if request.method == "GET":
        if request.session.get("id_user"):
            return render(
                request, "dashboard/dashboard.html", {"seccion_actual": "dashboard"}
            )
        else:
            return redirect("inicio")


def inventario(request):
    id_user = request.session.get("id_user")
    productos = Producto.obtener_productos_por_empresa(id_user)
    print("PRODUCTOS",productos)
    categorias =  Categoria.objects.all()
    #print("Categorias", categorias)

    if request.method == "POST":
        # Obtener los datos del formulario
        buscar_texto = request.POST.get("texto", "")
        cantidad = request.POST.get("cantidad", None)
        cantidad = int(cantidad)
        id_categoria = request.POST.get("categoria", None)
        id_categoria = None if id_categoria == "-1" else id_categoria

        print("Se busca ->", buscar_texto, cantidad, id_categoria)

        # Filtrar productos
        productos_filtrados = Producto.filtrar(
            productos, buscar_texto, cantidad, id_categoria
        )
        print("FILTRADOS ->", productos_filtrados)

        data = {"seccion_actual": "inventario",
                "productos": productos_filtrados,
                "categorias": categorias,
        }
        return render(
            request, "inventario/inventario.html", data
        )
    if request.method == "GET":
        if id_user:
            data = {"seccion_actual": "inventario",
                    "productos": productos,
                    "categorias": categorias,
            }
            return render(
                request, "inventario/inventario.html", data
            )
        else:
            return redirect("inicio")


def crear_producto(request):
    id_user = request.session.get("id_user")

    if request.method == "GET":
        if id_user:
            categorias = Categoria.objects.all()
            proveedores = Proveedor.objects.all()
            data = {
                "categorias": categorias,
                "proveedores": proveedores,
                "seccion_actual": "inventario",
            }
            return render(request, "inventario/agregarProducto.html", data)
        else:
            return redirect("inicio")

    if request.method == "POST":
        print("POST*********", request.POST)
        new_producto = Producto.create_producto(
            id_user,
            request.POST["nombreProducto"],
            request.POST["descripcion"],
            request.POST["precioUnitario"],
            request.POST["cantidad"],
            request.POST["categoria"],
            request.POST["proveedor"],
        )
        print("Product creado: ",new_producto)
        if new_producto == -2:
            messages.error(request, "Ocurrio un error al crea el producto")
        else:
            messages.success(request, "Producto creado correctamente")
        return redirect("inventario")


def editar_producto(request, id):
    id_user = request.session.get("id_user")

    if request.method == "GET":
        if id_user:
            producto = Producto.obtener_producto_por_id_y_empresa(id, id_user)
            categorias = Categoria.objects.all()
            proveedores = Proveedor.objects.all()
            data = {
                "proveedores": proveedores,
                "producto": producto,
                "categorias": categorias,
                "seccion_actual": "inventario",
            }
            return render(request, "inventario/editarProducto.html", data)
        else:
            return redirect("inicio")

    if request.method == "POST":
        actualizado = Producto.actualizar_producto(
            id,
            request.POST["nombreProducto"],
            request.POST["descripcion"],
            request.POST["precioUnitario"],
            request.POST["cantidad"],
            request.POST["fecha_ingreso"],
            request.POST["categoria"],
            request.POST["proveedor"],
        )
        print("Producto editado: " + actualizado.nombre)
        messages.success(request, "Producto editado correctamente")
        return redirect("inventario")


def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.eliminar_producto()
    messages.success(request, "Producto eliminado correctamente")
    return redirect("inventario")

def editar_empleado(request, id):
    print(id)
    id_user = request.session.get("id_user")
    empleado = Empleado.obtener_empleado_por_id_y_empresa(id,id_user)
    print("Empleados",empleado)
    print(id_user)

    if request.method == "GET":
        if id_user:
            data = {"seccion_actual": "empleados",
                    "empleado": empleado,
            }
            return render(
                request, "dashboard/registro_empleado.html", data
            )
        else:
            return redirect("inicio")
    else:
        if request.POST['password1'] == request.POST['password2'] and request.POST['nombreEmpleado'] and request.POST['mailEmpleado']:
            user_actualizado = CustomUser.modificar_usuario(empleado.user.id,
            request.POST["nombreEmpleado"],
            request.POST["mailEmpleado"],
            request.POST["password1"]
        )
        #print("usuario editado: ", user_actualizado.nombre)
        if user_actualizado == 1 :
            messages.error(request, "El mail ya esta en uso")
        elif user_actualizado == 2 :
            messages.error(request, "Error en la modificacion de usuario")
        else:
            empleado_actualizado = Empleado.modificar_empleado(user_actualizado.id,
            request.POST["rol"],
            request.POST["telefonoEmpleado"]
            )
            print(empleado_actualizado)
            messages.success(request, "Se modifico el empleado correctamente")
            return redirect("vista_empleados")


def vista_empleados(request):
    id_user = request.session.get("id_user")
    empleados = Empleado.obtener_empleado_por_empresa(id_user)
    print("Empleados",empleados)
    print(id_user)

    if request.method == "GET":
        if id_user:
            data = {"seccion_actual": "empleados",
                    "empleados": empleados,
            }
            return render(
                request, "dashboard/vista_empleados.html", data
            )
        else:
            return redirect("inicio")

def eliminar_empleado(request, id):
    empleado = Empleado.objects.get(user_id=id)
    empleado.eliminar_empleado()
    messages.success(request, "Empleado eliminado correctamente")
    return redirect("vista_empleados")



    return render(request, 'dashboard/vista_empleados.html')

def registro_empleado(request):
    id_user = request.session.get("id_user")
    empleados = Empleado.obtener_empleado_por_empresa(id_user)
    print("Empleados",empleados)
    print(id_user)

    if request.method == "GET":
        if id_user:
            return render(
                request, "dashboard/registro_empleado.html"
            )
        else:
            return redirect("inicio")
    else:
        if request.POST['password1'] == request.POST['password2'] and request.POST['nombreEmpleado'] and request.POST['mailEmpleado']:
            new_user = CustomUser.register(request.POST['nombreEmpleado'], request.POST['mailEmpleado'], request.POST['password1'], False)
            if new_user == -1:
                print("El correo ya existe, mostrar un mensaje de error con toast")
                messages.error(request, "Error, el email utilizado ya existe")
                return redirect("vista_empleados")
            elif new_user == -2:
                print("Ocurrio un error durante el registro")
                messages.error(request, "Ocurrio un error durante el registro")
                return redirect("vista_empleados")
            else:
                print("El usuario ",new_user.nombre, "fue creado")
                new_empleado = Empleado.register(
                    new_user.id,
                    request.POST["rol"],
                    request.POST["telefonoEmpleado"],
                    id_user
                )
                print("empleado creado: ",new_empleado.user.nombre)
                print("empleado creado: ",new_empleado.user)
                print("empleado creado: ",new_empleado.telefono)
                print("empleado creado: ",new_empleado.id_empresa)
                messages.success(request, "Empleado creado correctamente")
                return redirect("vista_empleados")
        else:
            return redirect("vista_empleados")

def eliminar_empresa(request, id):
    empresa = Empresa.objects.get(user_id=id)
    empresa.eliminar_empresa()
    messages.success(request, "Cuenta eliminada correctamente")
    return redirect("inicio")

    return render(request, 'dashboard/registro_empleado.html')


def editar_empleado(request):
    empleados = Empleado.objects.all()
    return render(request, 'editar_empleado.html', {'empleados': empleados})


def eliminar_empleado(request, empleado_id):
    empleados = Empleado.objects.all()
    return render(request, 'eliminar_empleado.html', {'empleados': empleados})


def cerrar_sesion(request):
    request.session["id_user"] = None
    return redirect("dashboard-inicio")


def proveedores(request):
    id_user = request.session.get("id_user")

    if request.method == "GET":
        if id_user:
            proveedores = Proveedor.objects.all()
            data = {
                "proveedores": proveedores,
                "seccion_actual": "proveedores",
            }
            return render(request, "proveedores/proveedores.html", data)
        else:
            return redirect("inicio")


def crear_proveedor(request):
    id_user = request.session.get("id_user")

    if request.method == "GET":
        if id_user:
            data = {
                "seccion_actual": "proveedores",
            }
            return render(request, "proveedores/agregarproveedor.html", data)
        else:
            return redirect("inicio")

    if request.method == "POST":
        print("POST*********", request.POST)
        new_proveedor = Proveedor.crear_proveedor(
            id_user,
            request.POST["nombre"],
            request.POST["telefono"],
            request.POST["correo"],
        )
        print("Proveedor creado: ",new_proveedor.nombre)
        messages.success(request, "Proveedor creado correctamente")
        return redirect("proveedores")

def editar_proveedor(request, id):
    pass


def eliminar_proveedor(request, id):
    pass
