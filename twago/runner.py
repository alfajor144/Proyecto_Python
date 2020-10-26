import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#import pdb; pdb.set_trace()
from twago.spiders import perfiles, ofertas

process = CrawlerProcess(settings=get_project_settings())

process.crawl(perfiles.PerfilesSpider)
process.start()
