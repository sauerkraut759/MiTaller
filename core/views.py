import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dateutil.parser import parse
from django.utils import timezone
from django.core.serializers import serialize

from .models import Categoria, Profesor, Lugar, Taller
from .forms import ProponerTallerForm

# Create your views here.}

API_URL = 'http://localhost:8000/api/'

def home(request):

    talleres = Taller.objects.filter(estado='aceptado', fecha__gte=timezone.now().date())

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

def proponerTaller(request):
    if request.user.is_anonymous:
        return redirect('home')
    

    if request.method == 'POST':
        sessionid = request.COOKIES.get('sessionid')
        csrftoken = request.COOKIES.get('csrftoken')
        cookies = {'sessionid': sessionid, 'csrftoken': csrftoken}
        headers = {'X-CSRFToken': csrftoken} if csrftoken else {}
        headers['Content-Type'] = 'application/json'

        form = ProponerTallerForm(request.POST)

        if form.is_valid():
            taller = form.save(commit=False)
            taller_json = serialize('json', [taller])
            data = json.loads(taller_json)
            fields = data[0]['fields'] # serialize funciona con listas

            try:
                response = requests.post(API_URL + 'talleres/', json=fields,headers=headers, cookies=cookies)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print("Error al enviar datos a la API", e)
        
        return redirect('proponerTaller')
            
    else:
        form = ProponerTallerForm

    return render(request, 'core/proponer.html', {'form': form})
