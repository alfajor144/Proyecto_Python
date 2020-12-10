import scrapy
import logging
import datetime
import requests
import math
from jobs.items import BuscojobsItem
from scrapy.exceptions import CloseSpider


class UyBuscoJobSpider(scrapy.Spider):
    name = 'uybuscojob-ofertas'
    nro_item = 0
    limite = None
    nro_item = 0
    pages = 0
    fecha_oferta = ""
    porcentaje_enviado = 0
    custom_settings = {
        'ROBOTSTXT_OBEY':True,
        'COOKIES_ENABLED':False,
        'ITEM_PIPELINES':{
            'jobs.pipelines.UyBuscoJobPipeline': 300,
        },
        # Configuración para exportar a json automaticamente
        'FEED_URI': 'Proyecto_Python/UruguayJob/uybuscojob-ofertas_' + datetime.datetime.today().strftime('%y%m%d%H%M%S') + '.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOADER_MIDDLEWARES' : {
        #    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        #    'tor_ip_rotator.middlewares.TorProxyMiddleware': 100,
            'scrapy.dowloadermiddlewares.useragent.UserAgentMiddleware': None,
            'jobs.middlewares.UserAgentRotatorMiddleware': 543,
        #    'scrapy_splash.SplashCookiesMiddleware': 723,
        #    'scrapy_splash.SplashMiddleware': 725,
        #    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
    }
    allowed_domains = ['www.buscojobs.com.uy']
    start_urls = ['https://www.buscojobs.com.uy/ofertas']

    def __init__(self, limite=5, *args, **kwargs):
        super(UyBuscoJobSpider, self).__init__(*args, **kwargs) # <- important
        try:
            self.limite = int(limite)
        except ValueError:
            #Si el limite ingresado no es válido
            self.limite = 5

    def parse(self, response):
        logging.info(response.url)
        # Obtiene todas las etiquetas a de las ofertas
        ofertas = response.xpath('//div[@class="row link-header"]/h3/a')
        # obtiene todas las fechas de las publicaciones de la pagina actual
        fechas = response.xpath('//div[@class="row link-footer"]/div/span')
        # Ingresa en cada oferta para obtener los datos con la funcion parse_item
        for i in range (len (ofertas)):
            oferta_link = ofertas[i].xpath('.//@href').get()
            self.fecha_oferta = fechas[i].xpath('normalize-space(.//text())').get()
            yield response.follow(url=oferta_link, callback=self.parse_item )
        next_page_url = response.xpath('//*[@id="paginaSiguiente"]/a/@href').get()
        if next_page_url is not None:
            self.pages += 1
            yield scrapy.Request(response.urljoin(next_page_url))
    
    def parse_item(self, response):
        logging.info(response.url)
        #obtiene el nro de llamado de la url y le agrega el uy- al inicio
        nro_llamado = response.url
        nro_llamado = nro_llamado.split("-")
        nro_llamado = "uy-" + nro_llamado.pop()
        titulo = response.xpath('normalize-space(//div/h1[@class="oferta-title"]/text())').get()
        all_dellates1  = response.xpath('//div[@class="col-md-12 descripcion-texto"]')
        empresa_nombre  = response.xpath('normalize-space(//div[@class="row"]/div[@class="col-sm-12 no-padding-right"]/a/h2/text())').get()
        empresa_imagen  = response.xpath('normalize-space(//div[@class="row text-center"]/img[@class="img-responsive"]/@src)').get()
        all_detalles2  = response.xpath('//div[@class="row"]/div[@class="col-sm-12"]')
        all_requisitos = response.xpath('//div[@class="row oferta-contenido"]/div/div')
        descripcion = all_dellates1.xpath('./p/text()').getall()
        categoria_padre = response.xpath('normalize-space(//div[@class="row oferta-contenido"]//ul/li[1]/a[1]/text())').get()
        puestos = ""
        requisitos = ""
        for i in range( len( all_detalles2 )):
            # obtiene el primer enlace, correspondiente al lugar
            if i == 0:
                lugar = all_detalles2[i].xpath('./a/h2/text()').getall()
                continue
            # obtiene el último enlace, correspondiente a la categoría
            if i == len(all_detalles2)-1:
                categoria = all_detalles2[i].xpath('./a/h2/text()').getall()
                continue
            # obtiene todos los elementos que están entre lugar y categoria
            if 0 < i < len(all_detalles2) -1 :
                nombre = all_detalles2[i].xpath('./strong/text()').get()
                if nombre == "Puestos Vacantes:":
                    puestos = all_detalles2[i].xpath('.//span/text()').get() 
                    continue
                if nombre == "Jornada Laboral:":
                    jornada_laboral = all_detalles2[i].xpath('.//span/text()').get() 
                    continue
        item = BuscojobsItem()
        item['nro_llamado'] = nro_llamado
        item['fecha_inicio'] = self.fecha_oferta
        item['fecha_fin'] = ""
        item['titulo'] = titulo
        item['descripcion']  = descripcion
        item['empresa_nombre'] = empresa_nombre
        item['empresa_imagen'] = empresa_imagen
        item['lugar'] = lugar 
        item['jornada_laboral'] = jornada_laboral 
        item['puestos_vacantes'] = puestos
        item['categoria'] = categoria 
        item['categoria_padre'] = categoria_padre
        item['requisitos'] = all_requisitos
        self.nro_item += 1
        if self.nro_item > self.limite :
            raise CloseSpider('item_exceeded')
        #import ipdb; ipdb.set_trace()
        self.report_buscojob() # calcula el porcentaje para enviar
        yield item


    def porcentaje(self):
        #import ipdb; ipdb.set_trace()
        if self.nro_item > 0 and self.limite > 0:
            p =  100 * self.nro_item / self.limite 
            return p

    def report_buscojob(self):
        p = self.porcentaje()
        parte_decimal, parte_entera = math.modf(p)
        if parte_entera != self.porcentaje_enviado:
            self.porcentaje_enviado = parte_entera
            progress = int(self.porcentaje_enviado)
            pload = {  "porcentaje": progress }
            response = requests.get("http://localhost:8000/administrador/progress/buscojob", params=pload ) 
            #import ipdb; ipdb.set_trace()
            #response = response.json()
            return response
