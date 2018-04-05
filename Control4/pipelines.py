# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import settings

from scrapy.exporters import CsvItemExporter


class Control4Pipeline(object):

    def open_spider(self, spider):
        f = open(settings.FILE_PATH, 'wb')
        self.exporter = CsvItemExporter(f)
    
    def process_item(self, item, spider):
        self.exporter.start_exporting()
        self.exporter.export_item(item)

        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
