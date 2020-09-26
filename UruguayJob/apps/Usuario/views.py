from django.shortcuts import render, redirect
from apps.Usuario.models import Usuario
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

def VerCV(request):
    return render(request, 'verCurriculum.html')

def Calificar(request):
    ListaOfertas = ["Panadero", "Verdulero", "Carnicero"]
    context = {
        'Ofertas': ListaOfertas,
    }
    return render(request, 'calificarEntrevista.html', context )

# ------------------- FUNCIONALIDADES ----------------------------

def Buscar(request):
    print(request.POST['keyWord'])
    print(request.POST['categoria'])
    print(request.POST['pais'])
    print(request.POST['ciudad'])
    return render(request, 'busquedas.html')

def RegistrarUsuario(request):
    usr = Usuario()
    usr.nombre = request.POST['nombre']
    usr.apellido = request.POST['apellido']
    usr.email = request.POST['email']
    usr.contrasenia = request.POST['password']

    try:
        Usuario.objects.get(email=request.POST['email'])
        context = {
            'msg':"Ya existe un usuario con ese correo :("
        }
        return render(request, 'registroDeUsuario.html', context)
    except Usuario.DoesNotExist:
        usr.save()
        return render(request, 'hUsuario.html')

def InciarSesion(request):
    return render(request, 'hUsuario.html')
    #return render(request, 'hAdmin.html')

def GetAllUsers(request):
    Usuarios = Usuario.objects.all()
    #Usuarios = Usuario.objects.get(nombre="julio")
    context = {
        'Usuarios': Usuarios
    }
    return render(request, 'entrevistar.html', context)




 
