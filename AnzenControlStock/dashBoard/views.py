from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from login.models import CustomUser, Empresa
from products.models import Producto

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

            empresa = Empresa.objects.get(user_id=usuario.id)
            if empresa is not None:
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
            new_user = CustomUser.register(request.POST['nombre'], request.POST['email'], request.POST['password1'])
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

def registro2(request,id_user):
    if request.method == 'GET':
        return render(
            request,
            "login/registro2.html",
            {"id_user": id_user},
        )
    if request.method == 'POST':
        print("POST*********",request.POST)
        foto_de_perfil = request.FILES.get("foto_perfil")
        if foto_de_perfil:
            foto_de_perfil = Empresa.generate_unique_filename(foto_de_perfil)

        new_empresa = Empresa.register(
            request.POST['id_user'],
            request.POST['nombre_de_empresa'],
            foto_de_perfil,
            request.POST['categoria_de_negocio'],
            request.POST['teléfono'],
            request.POST['correo_electrónico_de_la_empresa']
        )
        if not isinstance(new_empresa, int):
            if not new_empresa.es_extension_valida(foto_de_perfil):
                print('Error: La extension de la foto de perfil no es valida, pruebe con una de las siguientes: ".jpg", ".jpeg", ".png", ".gif"')
                new_empresa.foto_de_perfil = None

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
    if request.method == "POST":
        return HttpResponse("Hola")
    if request.method == "GET":
        id_user = request.session.get("id_user")
        if id_user:
            productos = Producto.obtener_productos_por_empresa(id_user)
            print("PRODUCTOS",productos)
            data = {"seccion_actual": "inventario",
                    "productos": productos
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
            return render(request, "inventario/agregarProducto.html")
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
        )

        return redirect("inventario")


def editar_producto(request):
    id_user = request.session.get("id_user")

    if request.method == "GET":
        if id_user:
            return render(request, "inventario/editarProducto.html")
        else:
            return redirect("inicio")
