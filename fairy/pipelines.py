# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import ChangeListItem,QuarterRankingItem

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class FairyPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost",27017)
        db = clinet['fairy']
        self.changeList = db["changeList"]
        self.quarterRanking = db["quarterRanking"]

    def process_item(self, item, spider):
        """  判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item,ChangeListItem):
            try:
                self.changeList.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, QuarterRankingItem):
            try:
                self.quarterRanking.insert(dict(item))
            except Exception:
                pass
        return item


def dbHandle():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        charset='utf8',
        use_unicode=False
    )
    return conn

class MysqlPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'insert into fairy.t_changeList(userIcon,userName,content,likes,comment) values (%s,%s,%s,%s,%s)'

        try:
            cursor.execute(sql,(item['userIcon'],item['userName'],item['content'],item['like'],item['comment']))
            dbObject.commit()
        except Exception,e:
            print e
            dbObject.rollback()

        return item