from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario =  models.AutoField(primary_key = True)
    nombre = models.CharField('nombre', max_length = 200, blank = False, null = False)
    apellido = models.CharField('apellido', max_length = 200, blank = False, null = False)
    contrasenia = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254, unique=True)
    cv = models.CharField(max_length = 300, blank = True, null = True)
    isAdmin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

class Oferta(models.Model):
    id_oferta =  models.AutoField(primary_key = True)
    titulo = models.CharField('Titulo', max_length = 200, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)
    pais = models.CharField('pais', max_length = 50, blank = False, null = False)
    fecha_inicio = models.DateField('fecha inicio')
    fecha_final = models.DateField('fecha final')
    link = models.CharField('link', max_length = 2050)
    Usuario_id = models.ManyToManyField(Usuario, related_name='Postulacion', through='Postulacion')

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    id_oferta = models.ForeignKey(Oferta, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    calificacion = models.IntegerField(blank = True, null = True)
    fecha_uno = models.DateField('fecha uno',blank = True, null = True)
    fecha_dos = models.DateField('fecha dos',blank = True, null = True)
    fecha_tres = models.DateField('fecha tres',blank = True, null = True)

    def __str__(self):
        return self.id_oferta 

class Categoria(models.Model):
    id =  models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length = 50, blank = False, null = False)
    id_Oferta = models.ForeignKey(Oferta, on_delete = models.CASCADE)

    def __str__(self):
        return self.nombre

class masBuscados(models.Model):
    id =  models.AutoField(primary_key = True)
    puesto = models.CharField('Nombre', max_length = 50, blank = False, null = False)
    id_Oferta = models.ForeignKey(Oferta, on_delete = models.CASCADE)

    def __str__(self):
        return self.puesto

