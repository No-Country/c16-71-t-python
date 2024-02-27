from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from login.models import CustomUser
from login.models import Empresa

# Create your views here.

def index(request):
    return render(request, 'dashboard/index.html')

def inicio(request):
    return render(request, 'dashboard/inicio.html')

def staff(request):
    return render(request, 'dashboard/staff.html')

def products(request):
    return render(request, 'dashboard/products.html')

def order(request):
    return render(request, 'dashboard/order.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'dashboard/registro.html')
    if request.method == 'POST':
        # verificaciones
        if request.POST['password1'] == request.POST['password2'] and request.POST['nombre'] and request.POST['email']:
            new_user = CustomUser.register(request.POST['nombre'], request.POST['email'], request.POST['password1'])
            if new_user == -1:
                print("El correo ya existe, mostrar un mensaje de error con toast")
            elif new_user == -2:
                print("Ocurrio un error durante el registro")
            else:
                print("El usuario ",new_user.nombre, "fue creado")
                return render(request, "dashboard/registro2.html", {"id_user": new_user.id})
            return HttpResponse("Hubo un problema durante el registro. Verifica tus datos.")

def registro2(request):
    if request.method == 'GET':
        return render(
            request,
            "dashboard/registro2.html",
            {"form_action": reverse("dashboard-registro2")},
        )
    if request.method == 'POST':
        print("POST*********",request.POST)
        if Empresa.es_extension_valida(request.POST['foto_perfil']):
            foto_de_perfil = Empresa.generate_unique_filename(request.POST['foto_perfil'])

            new_empresa = Empresa.register(
                request.POST['id_user'],
                foto_de_perfil,
                request.POST['categoria_de_negocio'],
                request.POST['teléfono'],
                request.POST['correo_electrónico_de_la_empresa']
            )
            if new_empresa == -2:
                print("Ocurrio un error")
            else:
                print("Se creo la empresa", new_empresa.nombre_de_la_empresa)
