from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField('nombre', max_length = 200, blank = False, null = False)
    apellido = models.CharField('apellido', max_length = 200, blank = False, null = False)
    contrasenia = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254, unique=True)
    cv = models.CharField(max_length = 300, blank = True, null = True)
    def __str__(self):
        return self.nombre

class Oferta(models.Model):
    titulo = models.CharField('Titulo', max_length = 200, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)
    fecha_inicio = models.DateField('fecha inicio')
    fecha_final = models.DateField('fecha final')
    link = models.CharField('link', max_length = 2050)
    Usuario_id = models.ManyToManyField(Usuario, related_name='Postulacion', through='Postulacion')

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete = models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    fecha_uno = models.DateField('fecha uno',blank = True, null = True)
    fecha_dos = models.DateField('fecha dos',blank = True, null = True)
    fecha_tres = models.DateField('fecha tres',blank = True, null = True)

