# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test0000'
    allowed_domains = ['www.cec-cesec.com.cn']
    start_urls = ['http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', 'http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', 'http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', 'http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1']
    headers = {
        "Referer": 'www.baidu.com',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def start_requests(self):
        yield scrapy.FormRequest('http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', method='GET', dont_filter=True)
        yield scrapy.FormRequest('http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', method='GET', dont_filter=True)
        yield scrapy.FormRequest('http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', method='GET', dont_filter=True)
        yield scrapy.FormRequest('http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/1', method='GET', dont_filter=True)

    def parse(self, response):
        print(len(response.text))

