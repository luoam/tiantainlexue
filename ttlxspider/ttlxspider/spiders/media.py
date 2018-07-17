# -*- coding: utf-8 -*-
import scrapy

from ttlxspider.items import TtlxspiderItem


class MediaSpider(scrapy.Spider):
    name = 'media'
    allowed_domains = ['oss.6tiantian.com', '127.0.0.1']
    start_urls = ['http://127.0.0.1:9501/index/Urls/1']

    def parse(self, response):
        url = TtlxspiderItem()
        for item in response.xpath('/html/body/div/ul/li/a/@href').extract():
            url['mediaurl'] = item
            yield url

        weburl = "http://127.0.0.1:9501%s"
        next_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_url is not None:
            next_url = weburl % next_url
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
