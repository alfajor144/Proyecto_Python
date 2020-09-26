from django.shortcuts import render, redirect
from apps.Usuario.models import Usuario
# Create your views here.

def HomeAdmin(request):
    try:
        nombre = request.session['nombre']
        if(request.session['isAdmin']):
            context = {
                'userNombre': request.session['nombre']
            }
            return render(request, 'hAdmin.html', context)
        else:
            context = {
                'userNombre': request.session['nombre']
            }
            return render(request, 'hUsuario.html', context)
    except KeyError: 
            request.session.flush()
            return render(request, 'hInvitado.html')

def HomeUser(request):
    try:
        nombre = request.session['nombre']
        if(request.session['isAdmin'] == 0):
            context = {
                'userNombre': request.session['nombre']
            }
            return render(request, 'hUsuario.html', context)
        else:
            request.session.flush()
            return render(request, 'hInvitado.html')
    except KeyError: 
            request.session.flush()
            return render(request, 'hInvitado.html')

def HomeInvitado(request):
    request.session.flush()
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
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'registroDeUsuario.html')
        
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

        request.session['id_usuario'] = usr.id_usuario
        request.session['nombre'] = usr.nombre
        request.session['apellido'] = usr.apellido
        request.session['isAdmin'] = usr.isAdmin

        context = {
            'userNombre': request.session['nombre']
        }
        return render(request, 'hUsuario.html', context)

def InciarSesion(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    try:
        usr = Usuario.objects.get(email=request.POST['email'])
        if usr.contrasenia == request.POST['password']:
            if usr.isAdmin:
                request.session['id_usuario'] = usr.id_usuario
                request.session['nombre'] = usr.nombre
                request.session['apellido'] = usr.apellido
                request.session['isAdmin'] = usr.isAdmin
                context = {
                    'userNombre': request.session['nombre']
                }
                return render(request, 'hAdmin.html', context)
            else:
                request.session['id_usuario'] = usr.id_usuario
                request.session['nombre'] = usr.nombre
                request.session['apellido'] = usr.apellido
                request.session['isAdmin'] = usr.isAdmin

                context = {
                    'userNombre': request.session['nombre']
                }
                return render(request, 'hUsuario.html', context)
        else:
            context = {
                'msg1':"Contraseña incorrecta!"
            }
            return render(request, 'iniciarSesion.html', context)

    except Usuario.DoesNotExist:
        context = {
            'msg2':"No hay ningun usuario con ese correo :("
        }
        return render(request, 'iniciarSesion.html', context)


def GetAllUsers(request):
    Usuarios = Usuario.objects.all()
    #Usuarios = Usuario.objects.get(nombre="julio")
    context = {
        'Usuarios': Usuarios
    }
    return render(request, 'entrevistar.html', context)

def CerrarSesion(request):
    request.session.flush()
    return render(request, 'hInvitado.html')




 
