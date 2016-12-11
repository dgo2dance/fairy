# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import ChangeListItem

class FairyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost",27017)
        db = clinet['fairy']
        self.changeList = db["changeList"]

    def process_item(self, item, spider):
        """  判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item,ChangeListItem):
            try:
                self.changeList.insert(dict(item))
            except Exception:
                pass

        return item