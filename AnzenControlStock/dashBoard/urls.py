from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'), 
    path('inicio/', views.inicio, name='dashboard-inicio'), 
    path('staff/', views.staff, name='dashboard-staff'),
    path('products/', views.products, name='dashboard-products'),
    path('order/', views.order, name='dashboard-order'),
    path('registro/', views.registro, name='dashboard-registro'), 
    path('registro2/', views.registro2, name='dashboard-registro2'), 
]