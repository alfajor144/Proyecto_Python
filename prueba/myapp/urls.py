from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='myapp-home'),
    path('login/', views.login, name='myapp-login')
]
