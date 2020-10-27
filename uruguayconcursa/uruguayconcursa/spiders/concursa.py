import scrapy
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from  uruguayconcursa.items import UruguayconcursaItem
from scrapy_splash import SplashRequest


class ConcursaSpider(scrapy.Spider):
    name = 'concursa'
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

    
    # Método para setear los valores inciales de la solicitud
    def start_requests(self):        
        # Trae toda la pagina completa utilizando splash
        yield SplashRequest(url="https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.inicio", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script_pagina_completa
        })


    def parse(self, response):
        #Registra la url que obtenemos como respuesta de cada solicitud enviada
        logging.info(response.url)
        print(response.url)
        # Obtiene todas las etiquetas 'a' de las ofertas
        ofertas = response.xpath('//td[4]/span[1]/a')
    
        for oferta in ofertas:
            link_relativo = oferta.xpath('.//@href').get()
            oferta_link = f"https://www.uruguayconcursa.gub.uy/Portal/servlet/{link_relativo}"
            #absolute_url = response.urljoin(oferta_link)
            yield SplashRequest(url=oferta_link, callback=self.parse_item , endpoint="execute", args={
                'lua_source': self.script_pagina_completa
            })


        pagination = response.xpath('normalize-space(//*[@id="PAGECOUNTINFORMATION"]/text())').get().strip()
        cadenas_pagination = pagination.split(" ")
        pagina_actual = cadenas_pagination[0]
        ultima_pagina = cadenas_pagination[2]

        if pagina_actual != ultima_pagina :
            yield SplashRequest(url=response.url, callback=self.parse, endpoint="execute", args={
                'lua_source': self.script_siguiente
            })
 

    
    def parse_item(self, response):
        
        llamado = response.xpath('normalize-space(//*[@id="TABLE1"]/tbody/tr[1]/td/span[1]/text()[1])').get().strip()
        nro_llamado = llamado.split(" ")[2]  # selecciona la última palabra del string
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

        items = UruguayconcursaItem()
        items['nro_llamado'] = nro_llamado
        items['titulo'] = titulo
        items['fecha_inicio'] = fecha_inicio 
        items['fecha_fin'] = fecha_fin 
        items['tipo_tarea'] = tipo_tarea 
        items['tipo_vinculo'] = tipo_vinculo 
        items['tiempo_contrato'] = tiempo_contrato
        items['descripcion'] = descripcion 
        items['requisitos'] = requisitos
        items['recepcion_postulaciones'] = recepcion_postulaciones 
        items['recepcion_consultas'] = recepcion_consultas 
        items['telefono_consultas'] = telefono_consultas 
        items['organismo'] = organismo 
        items['comentario_interes'] = comentario_interes 

        yield {
            'nro_llamado': items['nro_llamado'],
            'titulo': items['titulo'],
            'fecha_inicio': items['fecha_inicio'], 
            'fecha_fin': items['fecha_fin'], 
            'tipo_tarea': items['tipo_tarea'], 
            'tipo_vinculo': items['tipo_vinculo'], 
            'tiempo_contrato': items['tiempo_contrato'], 
            'descripcion': items['descripcion'], 
            'requisitos': items['requisitos'], 
            'recepcion_postulaciones': items['recepcion_postulaciones'], 
            'recepcion_consultas': items['recepcion_consultas'], 
            'telefono_consultas': items['telefono_consultas'], 
            'organismo': items['organismo'], 
            'comentario_interes': items['comentario_interes'] 
        } 