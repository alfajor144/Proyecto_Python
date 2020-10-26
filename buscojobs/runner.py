import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from buscojobs.spiders.uysbusco import UysbuscoSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(UysbuscoSpider)
process.start()