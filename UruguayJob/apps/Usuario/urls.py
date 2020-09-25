from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeInvitado, name='Invitado'), #Home
    path('u/', views.HomeUser, name='Usuario'), 
    path('a/', views.HomeAdmin, name='Administrador'),
    path('r/', views.Registrarse, name='Registrarse'),
    path('i/', views.IniciarSesion, name='IniciarSesion')
]
