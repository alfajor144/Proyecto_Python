from django.db import models

# Create your models here.

class Autor(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200, blank = False, null = False)
    apellido = models.CharField(max_length = 200, blank = False, null = False)
    nacionalidad = models.CharField(max_length = 100, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    id =  models.AutoField(primary_key = True)
    titulo = models.CharField('Titulo', max_length = 200, blank = False, null = False)
    fecha_publicacion = models.DateField('fecha de publicacion', blank = False, null = False)
    fecha_de_ingreso = models.DateField('Fecha de ingreso al sistema', auto_now = True, auto_now_add = False)
    #autor_id = models.OneToOneField(Autor, on_delete = models.CASCADE) #si un autor tiene un solo libro
    #autor_id = models.ManyToManyField(Autor) # si muchos autores tienen muchos libros
    autor_id = models.ForeignKey(Autor, on_delete = models.CASCADE) # si un autor tiene muchos libros

    def __str__(self):
        return self.titulo
