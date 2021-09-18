# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihulivesCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
'''
#remove duplicates lives
from scrapy.exceptions import DropItem

class DuplicatesLive(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
#remove duplicate speakers

class DuplicatesSpeaker(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
'''

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from zhihulives_crawler.items import LiveItem,SpeakerItem

#save live and speaker in two different files
'''
class MultiCSVItemPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporter1 = CsvItemExporter(fields_to_export=LiveItem.fields.keys(),file=open("lives.csv",'wb'))
        self.exporter2 = CsvItemExporter(fields_to_export=SpeakerItem.fields.keys(),file=open("speakers.csv",'wb'))

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.exporter1.start_exporting()
        self.exporter2.start_exporting()

    def spider_closed(self, spider):
        self.exporter1.finish_exporting()
        self.exporter2.finish_exporting()
        #file = self.files.pop(spider)
        #file.close()

    def process_item(self, item, spider):
        self.exporter1.export_item(item)
        self.exporter2.export_item(item)
        return item
'''