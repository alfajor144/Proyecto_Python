# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TwagoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id_oferta = scrapy.Field()
    titulo = scrapy.Field()
    descripcion = scrapy.Field()
    fecha_inicio = scrapy.Field()
    fecha_fin = scrapy.Field()
    presupuesto = scrapy.Field()
    requisitos = scrapy.Field()


class PerfilesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id_perfil = scrapy.Field()
    precio = scrapy.Field()
    habilidades = scrapy.Field()
    user_agent = scrapy.Field()
