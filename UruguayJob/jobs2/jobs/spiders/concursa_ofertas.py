import scrapy
import logging
import datetime
import requests
import math
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jobs.items import UruguayConcursaItem
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider


class ConcursaSpider(scrapy.Spider):
    name = 'concursa-ofertas'
    limite = None
    nro_item = 0
    pages = 0
    porcentaje_enviado = 0
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'COOKIES_ENABLED': False,
        # ==== Inicio de configuración para splash ==============
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        # Configura el filtro para peticiones duplicadas de splash
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # Configura la conexión con splash
        'SPLASH_URL': 'http://localhost:8051',
        # ==== fin de configuración para splash ==============
        'ITEM_PIPELINES': {
            'jobs.pipelines.UruguayConcursaPipeline': 300,
        },
        # Configuración para exportar a json automaticamente
        'FEED_URI': 'Proyecto_Python/UruguayJob/concursa-ofertas_' + datetime.datetime.today().strftime('%y%m%d%H%M%S') + '.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    # Contiene todos los dominios permitidos para ese sitio web
    allowed_domains = ['www.uruguayconcursa.gub.uy']
    #start_urls = ['https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.inicio']
    script_pagina_completa = '''
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''
    # Preciona el boton de siguient pagina de la paginación
    script_siguiente = '''
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            btn_next = assert(splash:select("#NEXT"))
            btn_next:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def __init__(self, limite=10, *args, **kwargs):
        super(ConcursaSpider, self).__init__(*args, **kwargs) # <- important
        try:
            self.limite = int(limite)
        except ValueError:
            #Si el limite ingresado no es válido
            self.limite = 10

    # Método para setear los valores inciales de la solicitud
    def start_requests(self):
        # Trae toda la pagina completa utilizando splash
        yield SplashRequest(url="https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.inicio",
            callback=self.parse, endpoint="execute",
            args={'lua_source': self.script_pagina_completa}
        )

    def parse(self, response):
        # Registra la url que obtenemos como respuesta de cada solicitud enviada
        logging.info(response.url)
        self.pages += 1
        # Obtiene todas las etiquetas 'a' de las ofertas
        ofertas = response.xpath('//td[4]/span[1]/a')
        for oferta in ofertas:
            link_relativo = oferta.xpath('.//@href').get()
            oferta_link = f"https://www.uruguayconcursa.gub.uy/Portal/servlet/{link_relativo}"
            #absolute_url = response.urljoin(oferta_link)
            yield SplashRequest(url=oferta_link, callback=self.parse_item, endpoint="execute", args={'lua_source': self.script_pagina_completa})
        pagination = response.xpath('normalize-space(//*[@id="PAGECOUNTINFORMATION"]/text())').get().strip()
        if pagination != '':
            cadenas_pagination = pagination.split(" ")
            pagina_actual = cadenas_pagination[0]
            ultima_pagina = cadenas_pagination[2]
            if pagina_actual != ultima_pagina:
                yield SplashRequest(url=response.url, callback=self.parse, endpoint="execute", args={'lua_source': self.script_siguiente})

    def parse_item(self, response):
        llamado = response.xpath(
            'normalize-space(//*[@id="TABLE1"]/tbody/tr[1]/td/span[1]/text()[1])').get().strip()
        # selecciona la última palabra del string
        nro_llamado = llamado.split(" ")[2]
        titulo = response.xpath('normalize-space(//*[@id="TABLE1"]/tbody/tr[1]/td/span[1]/text()[2])').get().strip()
        periodo_postulacion = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[3]/td[2]/span/text()[2])').get().strip()
        fecha_inicio = periodo_postulacion.split(" ")[2]
        fecha_fin = periodo_postulacion.split(" ")[0]
        tipo_tarea = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[4]/td[2]/span/text()[2])').get().strip()
        tipo_vinculo = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[11]/td[2]/span/text()[2])').get().strip()
        tiempo_contrato = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[12]/td[2]/span/text()[2])').get().strip()
        descripcion = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[13]/td[2]/span/text()[2])').get().strip()
        requisitos = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[14]/td[2]/span)').get().strip()
        recepcion_postulaciones = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[15]/td[2]/span/text()[2])').get().strip()
        recepcion_consultas = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[16]/td[2]/span/text()[2])').get().strip()
        telefono_consultas = response.xpath('normalize-space(//*[@id="TABLE2"]/tbody/tr[17]/td[2]/span/text()[2])').get().strip()
        organismo = response.xpath('normalize-space(//*[@id="TABLE1"]/tbody/tr[4]/td/table/tbody/tr/td[1]/span/text()[1])').get().strip()
        comentario_interes = response.xpath('normalize-space(//*[@id="TABLE5"]/tbody/tr/td[2]/span)').get().strip()
        item = UruguayConcursaItem()
        item['nro_llamado'] = nro_llamado
        item['titulo'] = titulo
        item['fecha_inicio'] = fecha_inicio
        item['fecha_fin'] = fecha_fin
        item['tipo_tarea'] = tipo_tarea
        item['tipo_vinculo'] = tipo_vinculo
        item['tiempo_contrato'] = tiempo_contrato
        item['descripcion'] = descripcion
        item['requisitos'] = requisitos
        item['recepcion_postulaciones'] = recepcion_postulaciones
        item['recepcion_consultas'] = recepcion_consultas
        item['telefono_consultas'] = telefono_consultas
        item['organismo'] = organismo
        item['comentario_interes'] = comentario_interes
        self.nro_item += 1
        print("pagina:", self.pages, ", item:", self.nro_item)
        if self.nro_item > self.limite:
            raise CloseSpider('Se alcanzó el máximo número de elementos a raspar!')
        #import ipdb; ipdb.set_trace()
        self.report_concursa() # calcula el porcentaje para enviar
        yield item


    def porcentaje(self):
        #import ipdb; ipdb.set_trace()
        if self.nro_item > 0 and self.limite > 0:
            p =  100 * self.nro_item / self.limite 
            return p

    def report_concursa(self):
        p = self.porcentaje()
        parte_decimal, parte_entera = math.modf(p)
        if parte_entera != self.porcentaje_enviado:
            self.porcentaje_enviado = parte_entera
            progress = int(self.porcentaje_enviado)
            pload = {  "porcentaje": progress }
            response = requests.get("http://localhost:8000/administrador/progress/concursa", params=pload ) 
            #import ipdb; ipdb.set_trace()
            #response = response.json()
            return response
