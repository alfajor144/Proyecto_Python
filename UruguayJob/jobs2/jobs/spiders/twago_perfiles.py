import scrapy
import logging
from jobs.items import TwagoPerfilesItem
from scrapy.exceptions import CloseSpider, DropItem
import datetime
import requests
import math
from ipdb import launch_ipdb_on_exception

#from scrapy.project import crawler


class PerfilesSpider(scrapy.Spider):
    name = 'twago-perfiles'
    limite = None
    nro_item = 0
    pages = 0
    perfiles_deletes = 0
    pagination = None
    porcentaje_enviado = 0

    with launch_ipdb_on_exception():
        custom_settings = {
            'ROBOTSTXT_OBEY':False,
            'COOKIES_ENABLED':False,
            'ITEM_PIPELINES':{
                'jobs.pipelines.TwagoPerfilesPipeline': 300,
            },
            # Configuración para exportar a json automaticamente
            'FEED_URI': 'Proyecto_Python/UruguayJob/twago-perfiles_' + datetime.datetime.today().strftime('%y%m%d%H%M%S') + '.json',
            'FEED_FORMAT': 'json',
            'FEED_EXPORTERS': {
                'json': 'scrapy.exporters.JsonItemExporter',
            },
            'FEED_EXPORT_ENCODING': 'utf-8',
            # Para no usar el proxy y tor comentar comentar tor_ip_rotator
            # Las últimas dos lineas son para rotar el usr-agent
            'DOWNLOADER_MIDDLEWARES': {
                'tor_ip_rotator.middlewares.TorProxyMiddleware': 100,
                'scrapy.dowloadermiddlewares.useragent.UserAgentMiddleware': None,
                'jobs.middlewares.UserAgentRotatorMiddleware': 543,
            },
            'TOR_IPROTATOR_ENABLED' :True,
            'TOR_IPROTATOR_CHANGE_AFTER' : 20,
        }

        allowed_domains = ['www.twago.es']
        start_urls = ['https://www.twago.es/search/freelancer/?q=*&sortDirection=descending&cat=freelancer&sortField=default']

        def __init__(self, limite=10, *args, **kwargs):
            super(PerfilesSpider, self).__init__(*args, **kwargs) # <- important
            try:
                self.limite = int(limite)
            except ValueError:
                #Si el limite ingresado no es válido
                self.limite = 10

        def parse(self, response):
            self.logger.info('Función ofertas.parse %s', response.url)
            self.pages += 1
            # obtiene todos los links de los perfiles de la pagina actual
            perfiles = response.xpath('//div[@class="company-name small"]/a')
            # ingresa en cada perfil de la pagina actual y la 
            # funcion parse_item obtiene los datos
            for perfil in perfiles:
                perfil_link = perfil.xpath('./@href').get()
                yield response.follow(url=perfil_link, callback=self.parse_item)
            # trae todos los links del la paginación
            self.pagination = response.xpath(
               '//nav[@class="search-results-pager-links"]/a')
            # extrae la clase del btn. del paginador de la pag. actual
            for i in range(len(self.pagination)-1):
                # primero obtiene el actual, que tiene la clase selected
                clase_link = self.pagination[i].xpath('./@class').get()
                if clase_link == "search-results-page-link selected":
                    next_page_url = self.pagination[i+1].xpath('./@href').get()
                    break
    #        # Avanza a la siguiente pagina de la paginación
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))


        def parse_item(self, response):
            logging.info(response.url)
            #import pdb; pdb.set_trace()
            item = TwagoPerfilesItem()
            precio = response.xpath(
                '//span[@class="company-stats-rate"]/text()'
                ).get()
            if precio is not None:
                precio = precio.strip()
                precio = precio.split(" ")
                precio = precio[0]
                str_url = response.url
                str_url = str_url.split("/")
                id_perfil = str_url[len(str_url) - 2]
                habilidades = response.xpath('//div[@class="company-skills-summary"]/span/text()').getall()
                item['id_perfil'] = id_perfil
                item['precio'] = precio
                item['habilidades'] = habilidades
                self.nro_item += 1
                print("pagina:", self.pages, ", item:", self.nro_item)
                if self.nro_item > self.limite:
                    #self.crawler.stop()
                    raise CloseSpider("Parada")
                else:
                    #import ipdb; ipdb.set_trace()
                    self.progress_report() # calcula el porcentaje para enviar
                    yield item
            else:
                item['id_perfil'] = ""
                item['precio'] = ""
                item['habilidades'] = ""
                self.perfiles_deletes += 1
                yield item


        def porcentaje(self):
            #import ipdb; ipdb.set_trace()
            if self.nro_item > 0 and self.limite > 0:
                p =  100 * self.nro_item / self.limite 
                return p

        def progress_report(self):
            p = self.porcentaje()
            parte_decimal, parte_entera = math.modf(p)
            if parte_entera != self.porcentaje_enviado:
                self.porcentaje_enviado = parte_entera
                progress = int(self.porcentaje_enviado)
                pload = { "spider": 'twago-perfiles', "porcentaje": progress }
                response = requests.get("http://localhost:8000/administrador/progress", params=pload ) 
                #import ipdb; ipdb.set_trace()
                #response = response.json()
                return response
