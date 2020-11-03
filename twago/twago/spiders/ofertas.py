import scrapy
#import logging
from twago.items import TwagoItem
from scrapy.exceptions import CloseSpider

#import pdb; pdb.set_trace()


class OfertasSpider(scrapy.Spider):
#    import ipdb; ipdb.set_trace()
    name = 'ofertas'
    allowed_domains = ['www.twago.es']
    start_urls = [
        'https://www.twago.es/search/projects/?q=*&sortDirection=descending&cat=projects&sortField=default']
    _items = 0
    _pages = 0
    pagination = ""

#    def start_requests(self):
#        url="https://www.twago.es/search/projects/?q=*&sortDirection=descending&cat=projects&sortField=default"
#        yield scrapy.Request(url, self.parse)

    def parse(self, response):
#        import ipdb; ipdb.set_trace()
        self.logger.info('Función ofertas.parse %s', response.url)
        self._pages += 1
        # obtiene todas los proyectos (ofertas) de la pagina actual
        ofertas = response.xpath('//div[@class="project-name"]/a')
        # ingresa a cada oferta de la pagina actual y luego la
        #funcion parse_item obtiene los datos
        for oferta in ofertas:
            oferta_link = oferta.xpath('./@href').get()
            yield response.follow(url=oferta_link, callback=self.parse_item)
#        if self._pages >= 9:
#            import ipdb; ipdb.set_trace()
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
#        if self._pages == 1:
#            next_page_url = self._pages
        print("pagina:", self._pages, ", item:", self._items)
        if self._pages > 6:
            raise CloseSpider(
                'Se alcanzó el máximo número de elementos a raspar!'
                )
        # Avanza a la siguiente pagina de la paginación
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_item(self, response):
        #self.logger.info('Función ofertas.parse_item %s', response.url)
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
        presupuesto = response.xpath(
            'normalize-space(//div[@class="job-proposal-content"][1]/p/text())').get()
        fecha_inicio = response.xpath(
            '//div[@class="job-proposal-content"][2]/p/text()').get()
#        import ipdb; ipdb.set_trace()
#        fecha_inicio = fecha_inicio.split()
#        fecha_inicio = fecha_inicio[0]
#        fecha_inicio = fecha_inicio.split("/")
#        fecha_inicio = "20"+fecha_inicio[2] + \
#            "-"+fecha_inicio[1]+"-"+fecha_inicio[0]
        item['id_oferta'] = id_oferta
        item['titulo'] = response.xpath(
            '//div[@class="job-controls-info"]/h1/text()').get()
        item['descripcion'] = descripcion
        item['fecha_inicio'] = fecha_inicio
        item['fecha_fin'] = fecha_fin
        item['presupuesto'] = presupuesto
        item['requisitos'] = requisitos
        self._items += 1
        print("pagina:", self._pages, ", item:", self._items)
        if self._items >= 400:
            raise CloseSpider(
                    'Se alcanzó el máximo número de elementos a raspar!'
                    )
        if self._items == 67:
            import ipdb; ipdb.set_trace()
        yield item
