# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class PaperPipeline(object):

    def process_item(self, item, spider):
        if item['volume'] != None:
            item['volume'] = item['volume'].strip()[6:-1]
        if item['page'] != None:
            page = item['page'].strip()[2:]
            print(page)
            start_page = page.split('–')[0]
            print(start_page)
            item['page'] = start_page
        if item['issue'] !=None:
            item['issue'] = item['issue'][6:]
        return item



class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['papers'].insert(dict(item))
        return item

