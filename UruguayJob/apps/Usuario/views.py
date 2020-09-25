from django.shortcuts import render, redirect

# Create your views here.

def HomeAdmin(request):
    return render(request, 'hAdmin.html')

def HomeUser(request):
    return render(request, 'hUsuario.html')

def HomeInvitado(request):
    return render(request, 'hInvitado.html')