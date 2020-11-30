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
    path('verCV/', views.verCV, name='verCV'),
    path('hacerCV/', views.hacerCV, name='hacerCV'),
    path('calculadora/', views.calculadora, name='calculadora'),
    path('administrador/spiders', views.admin_spiders , name='admin-spiders'),
    path('administrador/daemonstatus', views.daemon_status , name='daemon-status'),
    path('administrador/listspiders', views.list_spiders , name='list-spiders'),
    path('administrador/listjobs', views.list_jobs , name='list-jobs'),
    path('administrador/cancelspider', views.cancel_spider , name='cancel-spider'),
    path('administrador/schedule', views.schedule , name='schedule'),
    path('administrador/progress/<spider>/<int:porcentaje>', views.progress_report , name='progress-report'),

    # -------------- CARGA DE DATOS DESDE JSONs--------------------------------
    #path('loadUC/', views.cargarUruguayConcursaJson, name='cargarUruguayConcursaJson'),
    #path('loadBJ/', views.cargarBuscoJobJson, name='cargarBuscoJobJson'),
    #path('loadHab/', views.cargarHabilidades, name='cargarHabilidades'),
    path('cargarBD/', views.cargarBD, name='cargarBD'),
    # -------------- FUNCIONALIDADES---------------------------------
    path('registrarUsuario/', views.RegistrarUsuario, name='registrarUsuario'),
    path('inciarSesion/', views.InciarSesion, name='inciarSesion'),
    path('buscar/', views.Buscar, name='buscar'),
    path('getAllUsers/', views.GetAllUsers, name='getAllUsers'),
    path('cerrarSesion/', views.CerrarSesion, name='cerrarSesion'),
    path('postularme/', views.postularme, name='postularme'),
    path('postularmeBusquedas/', views.postularmeBusquedas, name='postularmeBusquedas'),
    path('mostrarPostulantes/', views.mostrarPostulantes, name='mostrarPostulantes'),
    path('fijarFechaEntrevista/', views.fijarFechaEntrevista, name='fijarFechaEntrevista'),
    path('definirFechaEntrevista/', views.definirFechaEntrevista, name='definirFechaEntrevista'),
    path('verFechasDeEntrevista/', views.verFechasDeEntrevista, name='verFechasDeEntrevista'),
    path('mostrarPostulantesCalificar/', views.mostrarPostulantesCalificar, name='mostrarPostulantesCalificar'),
    path('calificarEntrevista/', views.calificarEntrevista, name='calificarEntrevista'),
    path('cargarCV/', views.cargarCV, name='cargarCV'),
    path('Calcular/', views.Calcular, name='Calcular')



]
