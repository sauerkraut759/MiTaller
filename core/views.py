from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def home(request):

    return render(request, 'core/index.html')

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