#!/bin/bash
scrapy crawl concursa-ofertas -a limite=200
sleep 10s
scrapy crawl twago-ofertas -a limite=200
sleep 10s
scrapy crawl twago-perfiles -a limite=200
sleep 10s
scrapy crawl uybuscojob-ofertas -a limite=200

