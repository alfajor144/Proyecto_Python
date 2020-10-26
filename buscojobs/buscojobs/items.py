# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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
