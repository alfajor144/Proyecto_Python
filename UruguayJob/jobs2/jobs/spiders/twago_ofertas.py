import scrapy
import logging
from jobs.items import TwagoOfertasItem
from scrapy.exceptions import CloseSpider
import datetime
import requests
import math

class TwagoOfertasSpider(scrapy.Spider):
    name = 'twago-ofertas'
    limite = None
    nro_item = 0
    pages = 0
    pagination = None   
    porcentaje_enviado = 0

    custom_settings = {
        'ROBOTSTXT_OBEY':False,
        'COOKIES_ENABLED':False,
        'ITEM_PIPELINES':{
            'jobs.pipelines.TwagoOfertasPipeline': 300,
        },
        # Configuración para exportar a json automaticamente
        'FEED_URI': 'Proyecto_Python/UruguayJob/twago-ofertas_' + datetime.datetime.today().strftime('%y%m%d%H%M%S') + '.json',
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
    start_urls = ['https://www.twago.es/search/projects/?q=*&sortDirection=descending&cat=projects&sortField=default']

    def __init__(self, limite=5, *args, **kwargs):
        super(TwagoOfertasSpider, self).__init__(*args, **kwargs) # <- important
        try:
            self.limite = int(limite)
        except ValueError:
            #Si el limite ingresado no es válido
            self.limite = 5

    def parse(self, response):
        #import ipdb; ipdb.set_trace()
        self.logger.info('Función ofertas.parse %s', response.url)
        self.pages += 1
        # obtiene todas los proyectos (ofertas) de la pagina actual
        ofertas = response.xpath('//div[@class="project-name"]/a')
        # ingresa a cada oferta de la pagina actual y luego la
        #funcion parsenro_item obtiene los datos
        for oferta in ofertas:
            oferta_link = oferta.xpath('./@href').get()
            print("oferta_link:", oferta_link)
            yield response.follow(url=oferta_link, callback=self.parse_item)
        # trae todos los links del la paginación
        self.pagination = response.xpath('//nav[@class="search-results-pager-links"]/a')
        # extrae la clase del btn. del paginador de la pag. actual
        for i in range(len(self.pagination)-1):
            # primero obtiene el actual, que tiene la clase selected
            clase_link = self.pagination[i].xpath('./@class').get()
            if clase_link == "search-results-page-link selected":
                next_page_url = self.pagination[i+1].xpath('./@href').get()
                break
        # Avanza a la siguiente pagina de la paginación
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_item(self, response):
        #import ipdb; ipdb.set_trace()
        self.logger.info('Función ofertas.parse_item %s', response.url)
        descripcion = ''
        titulo = ''
        presupuesto = ''
        fecha_inicio = ''
        fecha_fin = ''
        id_oferta = ''
        descripcion = ''
        str_url = response.url
        str_url = str_url.split("/")
        id_oferta = str_url[len(str_url) - 2]
        titulo = response.xpath('//div[@class="job-controls-info"]/h1/text()').get()
        lst_descripcion = response.xpath('//div[@class="job-public-description-text"][2]').getall()
        for parrafo in lst_descripcion:
            descripcion += parrafo
        requisitos = response.xpath('//span[@class="job-public-tag"]/text()').getall()
        fecha_fin = response.xpath('normalize-space(//div[@class="job-bid-info"]/span/text())').get()
        lbl_presupuesto = response.xpath('normalize-space(//div[@class="job-proposal-content"][1]/span/text())')
        if lbl_presupuesto == 'Presupuesto':
            presupuesto = response.xpath('normalize-space(//div[@class="job-proposal-content"][1]/p/text())').get()
        lbl_publicado = response.xpath('normalize-space(//div[@class="job-proposal-content"][2]/span/text())')
        if lbl_publicado == 'Publicado el':
            fecha_inicio = response.xpath('//div[@class="job-proposal-content"][2]/p/text()').get()
        item = TwagoOfertasItem()
        item['id_oferta'] = id_oferta
        item['titulo'] = titulo
        item['descripcion'] = descripcion
        item['fecha_inicio'] = fecha_inicio
        item['fecha_fin'] = fecha_fin
        item['presupuesto'] = presupuesto
        item['requisitos'] = requisitos
        self.nro_item += 1
        print("pagina:", self.pages, ", item:", self.nro_item)
        #import ipdb; ipdb.set_trace()
        if self.nro_item > self.limite:
            raise CloseSpider('Se alcanzó el máximo número de elementos a raspar!')
        else:
            #import ipdb; ipdb.set_trace()
            self.report_twago() # calcula el porcentaje para enviar
            yield item



    def porcentaje(self):
        #import ipdb; ipdb.set_trace()
        if self.nro_item > 0 and self.limite > 0:
            p =  100 * self.nro_item / self.limite 
            return p

    def report_twago(self):
        p = self.porcentaje()
        parte_decimal, parte_entera = math.modf(p)
        if parte_entera != self.porcentaje_enviado:
            self.porcentaje_enviado = parte_entera
            progress = int(self.porcentaje_enviado)
            pload = {  "porcentaje": progress }
            response = requests.get("http://localhost:8000/administrador/progress/twago", params=pload ) 
            #import ipdb; ipdb.set_trace()
            #response = response.json()
            return response
