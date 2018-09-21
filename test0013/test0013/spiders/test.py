# -*- coding: utf-8 -*-
import scrapy
import os
import hashlib

h = hashlib.md5()

def get_name(url):
    h.update(url.encode(encoding='utf-8'))
    return h.hexdigest() + ".jpeg"


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/p/2166231880']

    def parse(self, response):
        urls = response.xpath('//img[@class="BDE_Image"]/@src').extract()
        if not os.path.exists('images'):
            os.makedirs('images')

        for url in urls:
            yield scrapy.Request(url, callback=self.download, dont_filter=True)

    def download(self, response):
        name = get_name(response.url)
        with open('images' + os.sep + name, mode='xb') as fp:
            fp.write(response.body)


def rename():
    d = os.pardir + os.sep + os.pardir + os.sep + 'images'
    for f in os.listdir(d):
        f_name = os.path.join(d, f)
        os.rename(f_name, f_name + ".jpeg")


if __name__ == '__main__':
    rename()