import scrapy
import logging
import datetime
from ..items import BuscojobsItem
from scrapy.exceptions import CloseSpider


class UyBuscoJobSpider(scrapy.Spider):
    name = 'uybuscojob-ofertas'
    custom_settings = {
        'ROBOTSTXT_OBEY':True,
        'COOKIES_ENABLED':False,
        'ITEM_PIPELINES':{
            'jobs.pipelines.UyBuscoJobPipeline': 300,
        },
        # Configuración para exportar a json automaticamente
        'FEED_URI': 'uybuscojob-ofertas_' + datetime.datetime.today().strftime('%d_%m_%y') + '.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    allowed_domains = ['www.buscojobs.com.uy']
    start_urls = ['https://www.buscojobs.com.uy/ofertas']
    item_count = 0
    fecha_oferta = ""

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
        items = BuscojobsItem()
        items['nro_llamado'] = nro_llamado
        items['fecha_inicio'] = self.fecha_oferta
        items['fecha_fin'] = ""
        items['titulo'] = titulo
        items['descripcion']  = descripcion
        items['empresa_nombre'] = empresa_nombre
        items['empresa_imagen'] = empresa_imagen
        items['lugar'] = lugar 
        items['jornada_laboral'] = jornada_laboral 
        items['puestos_vacantes'] = puestos
        items['categoria'] = categoria 
        items['categoria_padre'] = categoria_padre
        items['requisitos'] = all_requisitos
        self.item_count += 1
        if self.item_count > 350 :
            raise CloseSpider('item_exceeded')
        yield items
