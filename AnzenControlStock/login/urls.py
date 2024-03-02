from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterUsuarioView.as_view(),name='register'),
    path('register/empresa/', views.RegisterEmpresaView.as_view(),name='register_empresa')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
