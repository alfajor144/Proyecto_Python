# Pasos para desplegar el proyecto

## Programas a instalar:

### python-3.8.6rc1-amd64.exe

### XAMPP 7.1.32

## instalar entorno virtual:

### python.exe -m venv env

### pip install django

### pip install mysqlclient

### pip install Twisted-20.3.0-cp38-cp38-win_amd64.whl

### pip install Scapry

## Crear en phpMyAdmin base de datos "uruguayjob"

### python manage.py makemigrations

### python manage.py migrate

### importar datosDePrueba.sql

### python manage.py runserver
