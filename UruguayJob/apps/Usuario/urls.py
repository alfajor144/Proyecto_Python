from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeInvitado, name='Invitado'), #Home
    path('u/', views.HomeUser, name='Usuario'), 
    path('a/', views.HomeAdmin, name='Administrador'),
    path('r/', views.Registrarse, name='Registrarse'),
    path('e/', views.Estadistica, name='Estadistica'),
    path('n/', views.Entrevistar, name='Entrevistar'),
    path('s/', views.Entrevistas, name='Entrevistas'),
    path('c/', views.Calificar, name='Calificar'),
    path('i/', views.IniciarSesion, name='IniciarSesion')
]
