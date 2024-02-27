from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.

def main(request):
    return render(request, 'dashboard/main.html')

def staff(request):
    return render(request, 'dashboard/staff.html')

def products(request):
    return render(request, 'dashboard/products.html')

def order(request):
    return render(request, 'dashboard/order.html')

def inicio(request):
    return render(request, 'dashboard/inicio.html')

def registro(request):
    return render(request, 'dashboard/registro.html')

def registro2(request):
    return render(request, 'dashboard/registro2.html')