import scrapy
import logging
from twago.items import PerfilesItem
from scrapy.exceptions import CloseSpider

#import pdb; pdb.set_trace()
class PerfilesSpider(scrapy.Spider):
    name = 'perfiles'
    allowed_domains = ['www.twago.es']
    start_urls = ['https://www.twago.es/search/freelancer/?q=*&sortDirection=descending&cat=freelancer&sortField=default']
    perfiles_count = 0
    page_count = 0
    perfiles_deletes = 0

    def parse(self, response):
        #import pdb; pdb.set_trace()
        logging.info(response.url)
        # obtiene todos los perfiles de la pagina actual
        perfiles = response.xpath('//div[@class="company-name small"]/a')
        # ingresa en cada perfil de la pagina actual y la funcion parse_item obtiene los datos
        for perfil in perfiles:
            perfil_link = perfil.xpath('./@href').get()
            yield response.follow(url=perfil_link, callback=self.parse_item)

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
            self.page_count += 1
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_item(self, response):
        #import pdb; pdb.set_trace()
        logging.info(response.url)
        item = PerfilesItem()
        str_url = response.url
        str_url = str_url.split("/")
        id_perfil = str_url[len(str_url) - 2]
        precio = response.xpath(
            '//span[@class="company-stats-rate"]/text()').get()
        if precio is not None:
            precio = precio.strip()
            precio = precio.split(" ")
            precio = precio[0]
            self.perfiles_count += 1
        habilidades = response.xpath(
            '//div[@class="company-skills-summary"]/span/text()').getall()
        item['id_perfil'] = id_perfil
        item['precio'] = precio
        item['habilidades'] = habilidades
        
        try:
            if self.perfiles_count <= 211:
                yield item
            else:
                raise CloseSpider('Se alcanzó el máximo número de elementos a raspar!')
        except CloseSpider as error:
            print("Error en perfiles.py, se alcanzo el límite a raspar.")

