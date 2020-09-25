from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeInvitado, name='Invitado'), #Home
    path('usuario/', views.HomeUser, name='Usuario'), 
    path('administrador/', views.HomeAdmin, name='Administrador'),
    path('registrarse/', views.Registrarse, name='Registrarse'),
    path('estadistic/', views.Estadistica, name='Estadistica'),
    path('entrevistar/', views.Entrevistar, name='Entrevistar'),
    path('enrevistas/', views.Entrevistas, name='Entrevistas'),
    path('calificar/', views.Calificar, name='Calificar'),
    path('iniciar-sesion/', views.IniciarSesion, name='IniciarSesion')
]
