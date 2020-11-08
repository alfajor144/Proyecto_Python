#!/bin/bash
scrapy crawl concursa-ofertas -a limite=10
scrapy crawl twago-ofertas -a limite=10
scrapy crawl twago-perfiles -a limite=10
scrapy crawl uybuscojob-ofertas -a limite=10

