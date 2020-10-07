from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeInvitado, name=''), #Home
    path('usuario/', views.HomeUser, name='usuario'), 
    path('administrador/', views.HomeAdmin, name='administrador'),
    path('registrarse/', views.Registrarse, name='registrarse'),
    path('estadistica/', views.Estadistica, name='estadistica'),
    path('entrevistar/', views.Entrevistar, name='entrevistar'),
    path('entrevistas/', views.Entrevistas, name='entrevistas'),
    path('calificar/', views.Calificar, name='calificar'),
    path('iniciar-sesion/', views.IniciarSesion, name='iniciar-sesion'),
    path('verCV/', views.VerCV, name='VerCV'),

    # -------------- FUNCIONALIDADES JULIO---------------------------------
    path('registrarUsuario/', views.RegistrarUsuario, name='registrarUsuario'),
    path('inciarSesion/', views.InciarSesion, name='inciarSesion'),
    path('buscar/', views.Buscar, name='buscar'),
    path('getAllUsers/', views.GetAllUsers, name='getAllUsers'),
    path('cerrarSesion/', views.CerrarSesion, name='cerrarSesion'),
    path('loadUC/', views.cargarUruguayConcursaJson, name='cargarUruguayConcursaJson'),
    path('postularme/', views.postularme, name='postularme'),
    path('postularmeBusquedas/', views.postularmeBusquedas, name='postularmeBusquedas'),
    path('mostrarPostulantes/', views.mostrarPostulantes, name='mostrarPostulantes'),
    path('fijarFechaEntrevista/', views.fijarFechaEntrevista, name='fijarFechaEntrevista'),
    path('definirFechaEntrevista/', views.definirFechaEntrevista, name='definirFechaEntrevista'),
    path('verFechasDeEntrevista/', views.verFechasDeEntrevista, name='verFechasDeEntrevista')
]
