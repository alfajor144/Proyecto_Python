import scrapy
import logging
from twago.items import TwagoItem
from scrapy.exceptions import CloseSpider

#import pdb; pdb.set_trace()


class OfertasSpider(scrapy.Spider):
    name = 'ofertas'
    allowed_domains = ['www.twago.es']
    start_urls = [
        'https://www.twago.es/search/projects/?q=*&sortDirection=descending&cat=projects&sortField=default']
    item_count = 0

    def parse(self, response):
        logging.info(response.url)
        # obtiene todas los proyectos (ofertas) de la pagina actual
        ofertas = response.xpath('//div[@class="project-name"]/a')
        # ingresa a cada oferta de la pagina actual y luego la funcion parse_item obtiene los datos
        for oferta in ofertas:
            oferta_link = oferta.xpath('./@href').get()
            yield response.follow(url=oferta_link, callback=self.parse_item)
        # obtiene todas las etiquetas a del la paginación menos la ultima
        pagination = response.xpath(
            '//nav[@class="search-results-pager-links"]/a')
        for i in range(len(pagination)-2):
            clase_link = pagination[i].xpath('./@class').get()
            if clase_link == "search-results-page-link selected":
                pagina_actual = int(pagination[i].xpath('./text()').get())
                if pagina_actual < (len(pagination) - 2):
                    next_page_url = pagination[i+1].xpath('./@href').get()
                    break
        # Avanza a la siguiente pagina de la paginación
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_item(self, response):
        logging.info(response.url)
        item = TwagoItem()
        # obtiene el id desde la url actual
        str_url = response.url
        str_url = str_url.split("/")
        id_oferta = str_url[len(str_url) - 2]
        lst_descripcion = response.xpath(
            '//div[@class="job-public-description-text"]/p/text()').getall()
        descripcion = ""
        for parrafo in lst_descripcion:
            descripcion += parrafo
        requisitos = response.xpath(
            '//span[@class="job-public-tag"]/text()').getall()
        fecha_fin = response.xpath(
            'normalize-space(//div[@class="job-bid-info"]/span/text())').get()
        #fecha_fin = fecha_fin.strip()
        presupuesto = response.xpath(
            'normalize-space(//div[@class="job-proposal-content"][1]/p/text())').get()
        fecha_inicio = response.xpath(
            '//div[@class="job-proposal-content"][2]/p/text()').get()
        fecha_inicio = fecha_inicio.split()
        fecha_inicio = fecha_inicio[0]
        fecha_inicio = fecha_inicio.split("/")
        fecha_inicio = "20"+fecha_inicio[2] + \
            "-"+fecha_inicio[1]+"-"+fecha_inicio[0]
        item['id_oferta'] = id_oferta
        item['titulo'] = response.xpath(
            '//div[@class="job-controls-info"]/h1/text()').get()
        item['descripcion'] = descripcion
        item['fecha_inicio'] = fecha_inicio
        item['fecha_fin'] = fecha_fin
        item['presupuesto'] = presupuesto
        item['requisitos'] = requisitos
        self.item_count += 1
        print(self.item_count)
        if self.item_count > 400:
            raise CloseSpider('item_exceeded')
        yield item
