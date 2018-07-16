# -*- coding: utf-8 -*-
import scrapy

from ttlxspider.items import TtlxspiderItem

class MediaSpider(scrapy.Spider):
    name = 'media'
    allowed_domains = ['oss.6tiantian.com', '127.0.0.1']
    start_urls = ['http://127.0.0.1:9501/index/Urls/1']

    def parse(self, response):
        for item in response.xpath('/html/body/div/ul/li/a/@href').extract():
            print(item)
