import scrapy
import logging
from jobs.items import TwagoPerfilesItem
from scrapy.exceptions import CloseSpider
import datetime


class PerfilesSpider(scrapy.Spider):
    name = 'twago-perfiles'
    custom_settings = {
        'ROBOTSTXT_OBEY':False,
        'COOKIES_ENABLED':False,
        'ITEM_PIPELINES':{
            'jobs.pipelines.TwagoPerfilesPipeline': 300,
        },
        # Configuración para exportar a json automaticamente
        'FEED_URI': 'twago-perfiles_' + datetime.datetime.today().strftime('%d_%m_%y') + '.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    allowed_domains = ['www.twago.es']
    start_urls = [
        'https://www.twago.es/search/freelancer/?q=*&sortDirection=descending&cat=freelancer&sortField=default']
    _items = 0
    _pages = 1
    perfiles_deletes = 0
    pagination = ""

    def parse(self, response):
        logging.info(response.url)
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
            self._pages += 1
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
            habilidades = response.xpath(
                    '//div[@class="company-skills-summary"]/span/text()'
                    ).getall()
            item['id_perfil'] = id_perfil
            item['precio'] = precio
            item['habilidades'] = habilidades
            self._items += 1
            print("pagina:", self._pages, ", item:", self._items)
            if self._items >= 300:
                raise CloseSpider(
                    'Se alcanzó el máximo número de elementos a raspar!'
                    )
            else:
                yield item
        else:
            item['id_perfil'] = ""
            item['precio'] = ""
            item['habilidades'] = ""
            self.perfiles_deletes += 1
            yield item
