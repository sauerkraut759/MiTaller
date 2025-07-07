import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dateutil.parser import parse

from .models import Categoria, Profesor, Lugar

# Create your views here.}

API_URL = 'http://localhost:8000/api/'

def home(request):
    try:
        # No estaba seguro si consumir la propia API del sistema era un requerimiento asi que lo hice de todas formas para asegurar
        # Normalmente obtendria la informacion a traves de los modelos
        response = requests.get(API_URL + 'talleres?futuros=true')
        response.raise_for_status()
        talleres = response.json()
    except requests.exceptions.RequestException as e:
        talleres = []
        print("Error al consultar la API:", e)

    for taller in talleres:
        taller["fecha"] = parse(taller["fecha"])
        taller["profesor"] = Profesor.objects.get(id=taller["profesor"])
        taller["categoria"] = Categoria.objects.get(id=taller["categoria"])
        taller["lugar"] = Lugar.objects.get(id=taller["lugar"])

    data = {
        "talleres": talleres
    }

    return render(request, 'core/index.html', data)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            messages.success(request, 'Sesion iniciada correctamente')
            return redirect('home')
        else:
            messages.warning(request, "Error al iniciar sesion")
            return redirect('login')

    else:
        return render(request, 'core/login.html');

def logoutUser(request):
    if request.user.is_anonymous:
        return redirect('home')
    
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente')
    return redirect('home')

def verTalleres(request):
    if request.user.is_anonymous:
        return redirect('home')
    
    cookies = {'sessionid': request.COOKIES.get('sessionid')}
    
    try:
        response = requests.get(API_URL + 'talleres', cookies=cookies)
        response.raise_for_status()
        talleres = response.json()
    except requests.exceptions.RequestException as e:
        talleres = []
        print("Error al consultar la API")

    for taller in talleres:
        taller["fecha"] = parse(taller["fecha"])
        taller["profesor"] = Profesor.objects.get(id=taller["profesor"]) if taller["profesor"] else None
        taller["categoria"] = Categoria.objects.get(id=taller["categoria"])
        taller["lugar"] = Lugar.objects.get(id=taller["lugar"])

    data = {
        "talleres": talleres
    }
    
    return render(request, 'core/talleres.html', data)