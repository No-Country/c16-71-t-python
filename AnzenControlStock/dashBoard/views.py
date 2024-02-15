from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.

def index(request):
    return HttpResponse('<h1 style="color:orange;"> This is the Index Page </h1>')



def staff(request):
    return HttpResponse('This is the Staff Page')