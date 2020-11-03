# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Twago3Item(scrapy.Item):
    id_oferta = scrapy.Field()
    titulo = scrapy.Field()
    descripcion = scrapy.Field()
    fecha_inicio = scrapy.Field()
    fecha_fin = scrapy.Field()
    presupuesto = scrapy.Field()
    requisitos = scrapy.Field()

class PerfilesItem(scrapy.Item):
    id_perfil = scrapy.Field()
    precio = scrapy.Field()
    habilidades = scrapy.Field()
