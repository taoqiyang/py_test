# -*- coding: utf-8 -*-
import scrapy
import os
import copy
from sinaNews.items import SinanewsItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # parentUrls = response.xpath('//div[@id="tab01"])
        tab0 = response.xpath("//div[@id='tab01']")
        clearfixs = tab0.xpath("./div[@class='clearfix']")
        for clearfix in clearfixs:
            title = clearfix.xpath("./h3/a")
            parentTitle = title.xpath("text()").extract_first()
            if parentTitle is None:
                continue
            parentUrl = title.xpath("@href").extract_first()
            parentFileName = "./Data/" + parentTitle
            if not os.path.exists(parentFileName):
                os.makedirs(parentFileName)

            for subitem in clearfix.xpath('.//li/a'):
                subTitle = subitem.xpath('text()').extract_first()
                subUrls = subitem.xpath('@href').extract_first()
                if subTitle is None or subUrls is None:
                    continue
                item = SinanewsItem()
                item['parentTitle'] = parentTitle
                item['parentUrl'] = parentUrl
                item['subTitle'] = subTitle
                item['subUrls'] = subUrls
                subFilename = parentFileName + os.sep + subTitle
                if not os.path.exists(subFilename):
                    os.makedirs(subFilename)
                item['subFilename'] = subFilename
                yield scrapy.Request(url=subUrls, meta={'item': item}, callback=self.parse_sub)

    def parse_sub(self, response):
        p_item = response.meta['item']
        parentUrl = p_item['parentUrl']
        sonUrls = response.xpath('//a/@href').extract()
        for url in sonUrls:
            if not url.endswith('.shtml') or not url.startswith(parentUrl):
                continue

            item = copy.deepcopy(p_item)
            item['sonUrls'] = url
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        p_item = response.meta['item']
        p_item['head'] = response.xpath('//h1[@class="main-title"]/text()').extract_first()
        p_item['content'] = ''.join(response.xpath('//div[@id="article"]/p/text()').extract())
        yield p_item
