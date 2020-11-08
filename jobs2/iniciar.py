
#-*- coding:utf-8 -*-
import sys
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#import pdb; pdb.set_trace()
from jobs.spiders import twago_ofertas
from colorama import init, Fore, Back, Style

#    spider1 = CrawlerProcess()
#    spider1.crawl(twago_perfiles.PerfilesSpider )
#    spider1.start()
spider2 = CrawlerProcess()
spider2.crawl(twago_ofertas.TwagoOfertasSpider, limite=10 )
spider2.start()
#    spider3 = CrawlerProcess()
#    spider3.crawl(concursa_ofertas.ConcursaSpider )
#    spider3.start()
#    spider4 = CrawlerProcess()
#    spider4.crawl(uybuscojob_ofertas.UyBuscoJobSpider )
#    spider4.start()



