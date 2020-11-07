import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#import pdb; pdb.set_trace()
from jobs.spiders import twago_perfiles



process = CrawlerProcess()
process.crawl(twago_perfiles.PerfilesSpider )
process.start()
