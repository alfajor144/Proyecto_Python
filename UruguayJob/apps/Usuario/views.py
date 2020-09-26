from django.shortcuts import render, redirect

# Create your views here.

def HomeAdmin(request):
    return render(request, 'hAdmin.html')

def HomeUser(request):
    return render(request, 'hUsuario.html')

def HomeInvitado(request):
    return render(request, 'hInvitado.html')

def Registrarse(request):
    return render(request, 'registroDeUsuario.html')

def IniciarSesion(request):
    return render(request, 'iniciarSesion.html')

def Estadistica(request):
    return render(request, 'estadistica.html')
    
def Entrevistar(request):
    return render(request, 'entrevistar.html')

def Entrevistas(request):
    return render(request, 'entrevistas.html')

def Calificar(request):

    ListaOfertas = ["Panadero", "Verdulero", "Carnicero"]

    context = {
        'titulo': ListaOfertas,
    }

    return render(request, 'calificarEntrevista.html', context )

def Buscar(request):
    print(request.POST['keyWord'])
    print(request.POST['categoria'])
    print(request.POST['pais'])
    print(request.POST['ciudad'])
    return render(request, 'busquedas.html')




 
