from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario =  models.AutoField(primary_key = True)
    nombre = models.CharField('nombre', max_length = 255, blank = False, null = False)
    apellido = models.CharField('apellido', max_length = 255, blank = False, null = False)
    contrasenia = models.CharField(max_length= 255)
    email = models.EmailField(max_length = 255, unique=True)
    cv = models.CharField(max_length = 255, blank = True, null = True)
    isAdmin = models.BooleanField(default=False)

class Curriculum(models.Model):
    id_c =  models.AutoField(primary_key = True)
    direccion = models.CharField('direccion', max_length = 255, blank = True, null = True)
    telefono = models.CharField('telefono', max_length = 255, blank = True, null = True)
    ci = models.CharField('telefono', max_length = 255, blank = True, null = True)
    experiencia = models.TextField(blank = True, null = True)
    formacion = models.TextField(blank = True, null = True)
    foto = models.ImageField(upload_to='updateFoto/', blank=True, null=True)
    idUsu = models.OneToOneField(Usuario, on_delete=models.CASCADE)

class CategoriaUC(models.Model):
    id =  models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length = 255, blank = False, null = False)
    isFreelancer = models.BooleanField(default=False)

class CategoriaBJ(models.Model):
    id =  models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length = 255, blank = False, null = False)

class SubCategoriaBJ(models.Model):
    id_Sub =  models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length = 255, blank = False, null = False)
    CategoriaBJ = models.ForeignKey(CategoriaBJ, on_delete = models.CASCADE, null = True)

class Oferta(models.Model):
    id_oferta =  models.CharField(primary_key = True, max_length = 255)
    titulo = models.CharField('Titulo', max_length = 255, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)
    pais = models.CharField('pais', max_length = 255, blank = False, null = False)
    fecha_inicio = models.DateField('fecha inicio')
    fecha_final = models.DateField('fecha final')
    Usuario_id = models.ManyToManyField(Usuario, related_name='Postulacion', through='Postulacion')
    CategoriaUC = models.ForeignKey(CategoriaUC, on_delete = models.CASCADE, null = True)
    SubCategoriaBJ = models.ForeignKey(SubCategoriaBJ, on_delete = models.CASCADE, null = True)
    #puesto = models.IntegerField('puesto', blank = True, null = True)

class Postulacion(models.Model):
    id_oferta = models.ForeignKey(Oferta, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    calificacion = models.IntegerField(blank = True, null = True)
    fecha_uno = models.DateField('fecha uno',blank = True, null = True)
    fecha_dos = models.DateField('fecha dos',blank = True, null = True)
    fecha_tres = models.DateField('fecha tres',blank = True, null = True)
    fecha_Definitiva = models.DateField('Definitiva',blank = True, null = True)
    comentario = models.TextField(blank = True, null = True)

class UruguayConcursa(models.Model):
    nro_llamado = models.CharField(primary_key = True, max_length = 255)
    titulo = models.CharField('titulo', max_length = 255, blank = False, null = False)
    fecha_inicio = models.DateField('fecha_inicio', max_length = 255, blank = False, null = False)
    fecha_fin = models.DateField('fecha_fin', max_length = 255, blank = False, null = False)
    tipo_tarea = models.CharField('tipo_tarea', max_length = 255, blank = False, null = False)
    tipo_vinculo = models.CharField('tipo_vinculo', max_length = 255, blank = False, null = False)
    tiempo_contrato = models.CharField('tiempo_contrato', max_length = 255, blank = False, null = False)
    descripcion =  models.TextField(blank = True, null = True)
    requisitos =  models.TextField(blank = True, null = True)
    recepcion_postulaciones = models.TextField(blank = True, null = True)
    recepcion_consultas =  models.TextField(blank = True, null = True)
    telefono_consultas = models.CharField('telefono_consultas', max_length = 255, blank = False, null = False)
    organismo = models.CharField('organismo', max_length = 255, blank = False, null = False)
    comentario_interes =  models.TextField(blank = True, null = True)

class BuscoJob(models.Model):
    nro_llamado = models.CharField(primary_key = True, max_length = 255)
    fecha_inicio = models.DateField('fecha_inicio', max_length = 255, blank = False, null = False)
    fecha_fin = models.DateField('fecha_fin', max_length = 255, blank = False, null = False)
    titulo = models.CharField('titulo', max_length = 255, blank = False, null = False)
    descripcion =  models.TextField(blank = True, null = True)
    empresa_nombre = models.CharField('empresa_nombre', max_length = 255, blank = False, null = False)
    lugar = models.CharField('lugar', max_length = 255, blank = False, null = False)
    jornada_laboral = models.CharField('jornada_laboral', max_length = 255, blank = False, null = False)
    puestos_vacantes = models.CharField('puestos_vacantes', max_length = 255, blank = False, null = False)
    categoria = models.CharField('categoria', max_length = 255, blank = False, null = False)
    subCategoria = models.CharField('subCategoria', max_length = 255, blank = False, null = False)
    requisitos =  models.TextField(blank = True, null = True)

class PerfHabs(models.Model):
    id_perfil = models.CharField(primary_key = True, max_length = 255)
    precio = models.IntegerField(blank = True, null = True)
    habilidades = models.TextField(blank = True, null = True)



