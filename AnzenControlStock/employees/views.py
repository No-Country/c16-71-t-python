from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView ,UpdateView ,DeleteView
from .models import *
from django.urls import reverse_lazy

class EmpleadoList(ListView):
    model = Empleado
    context_object_name = 'empleados'

class EmpleadoDetail(DetailView):
    model = Empleado
    context_object_name = 'empleado'

class EmpleadoCreate(CreateView):
    model = Empleado
    fields = '__all__'
    success_url = reverse_lazy('empleados')

class EmpleadoUpdate(UpdateView):
	model = Empleado
	fields = '__all__'
	success_url = reverse_lazy('empleados')

class EmpleadoDelete(DeleteView):
	model = Empleado
	context_object_name = 'empleado'
	success_url = reverse_lazy('empleados')


    
