from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterUsuarioView.as_view(),name='register'),
    path('register/empresa/', views.RegisterEmpresaView.as_view(),name='register_empresa')
    path('register/empeado/', views.RegisterEmpresaView.as_view(),name='register_empleado')
    
]