# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UruguayconcursaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # Atributos de la oferta
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