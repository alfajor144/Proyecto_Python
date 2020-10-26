import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from uruguayconcursa.spiders.concursa import ConcursaSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(ConcursaSpider)
process.start()
