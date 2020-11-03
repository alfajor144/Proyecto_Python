import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#import pdb; pdb.set_trace()
from twago3.spiders import ofertas

process = CrawlerProcess(settings=get_project_settings())

process.crawl(ofertas.OfertasSpider)
process.start()
