# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BuscojobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nro_llamado = scrapy.Field()
    fecha_inicio = scrapy.Field()
    fecha_fin = scrapy.Field()
    titulo = scrapy.Field()
    descripcion  = scrapy.Field()
    empresa_nombre  = scrapy.Field()
    empresa_imagen = scrapy.Field()
    lugar  = scrapy.Field()
    jornada_laboral  = scrapy.Field()
    puestos_vacantes = scrapy.Field()
    categoria_padre  = scrapy.Field()
    categoria  = scrapy.Field()
    requisitos = scrapy.Field()

class TwagoOfertasItem(scrapy.Item):
    id_oferta = scrapy.Field()
    titulo = scrapy.Field()
    descripcion = scrapy.Field()
    fecha_inicio = scrapy.Field()
    fecha_fin = scrapy.Field()
    presupuesto = scrapy.Field()
    requisitos = scrapy.Field()
 
class TwagoPerfilesItem(scrapy.Item):
    id_perfil = scrapy.Field()
    precio = scrapy.Field()
    habilidades = scrapy.Field()

class UruguayConcursaItem(scrapy.Item):
    nro_llamado = scrapy.Field()
    titulo = scrapy.Field()
    fecha_inicio = scrapy.Field()
    fecha_fin = scrapy.Field()
    tipo_tarea = scrapy.Field()
    tipo_vinculo = scrapy.Field()
    tiempo_contrato = scrapy.Field()
    descripcion = scrapy.Field()
    requisitos = scrapy.Field()
    recepcion_postulaciones = scrapy.Field()
    recepcion_consultas = scrapy.Field()
    telefono_consultas = scrapy.Field()
    organismo = scrapy.Field()
    comentario_interes = scrapy.Field()
