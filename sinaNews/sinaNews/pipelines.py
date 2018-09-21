# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class SinanewsPipeline(object):
    def process_item(self, item, spider):
        head = item['head']
        with open(item['subFilename'] + os.path.sep + head, 'w') as fp:
            fp.write(item['content'])
        return item
