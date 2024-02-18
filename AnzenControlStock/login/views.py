from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Empresa
import random
import string
from django.db import IntegrityError
from django.shortcuts import render



Empleado = get_user_model()
CustomUser= get_user_model()
# Create your views here.
  
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def post(self, request):     
        usuario = authenticate(
            request,
            email = request.POST['email'], 
            password = request.POST['password'] #
            )

        if usuario is not None:
            login(request, usuario)

            empresa = Empresa.objects.get(user_id = usuario.id)
            if empresa is not None:
                return HttpResponse("Iniciando Sesion empresa") #return render(request, 'index.html', {'objeto': empresa})
            empleado = Empleado.objects.get(user_id = usuario.id)

            return HttpResponse("Iniciando Sesion empresa") #return render(request, 'index_empleado.html', {'objeto': empleado})
        else:
            return HttpResponse("Error en usuario o contraseña")

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUsuarioView(View): 
    def post(self, request):

        if request.POST['password1'] == request.POST['password2']:       
            try:
                username_aleatorio=''.join(random.choice(string.     ascii_letters) for _ in range(30))
                usuario = CustomUser.objects.create_user(
                username= username_aleatorio,
                nombre= request.POST['nombre'],
                email = request.POST['email'], 
                password = request.POST['password'], 
                es_empresa = True
                )
                usuario.save()
                return HttpResponse("usuario creado")  #return render(request, 'plantilla_registro_siguiente.html', {'objeto': usuario})
            except IntegrityError as e:
                return HttpResponse("El Email ya esta en uso.") 
            except Exception as e:
                return HttpResponse(str(e))                     
        else:
            return HttpResponse("Las contreaseñas no coinciden")
        
@method_decorator(csrf_exempt, name='dispatch')
class RegisterEmpresaView(View):

    def post(self, request):
        try:
            empresa = Empresa.objects.create(
                user= request.POST['user_id'],       
                nombre_de_la_empresa = request.POST['nombre_de_la_empresa'], 
                foto_de_perfil = request.POST['foto_de_perfil'], 
                categoria_de_negocio = request.POST['categoria_de_negocio'], 
                teléfono = request.POST['teléfono'], 
                correo_electrónico_de_la_empresa = request.POST['correo_electrónico_de_la_empresa'] 
            )
            empresa.save()
            return HttpResponse("Empresa creada")    #return render(request, 'pantalla_principal.html', {'objeto': empresa})
        except IntegrityError as e:
            return HttpResponse(f"Error de integridad al guardar el objeto: {e}")
        except Exception as e:
            return HttpResponse(str(e))    
