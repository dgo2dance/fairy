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
import pymysql


class FairyPipeline(object):
    def process_item(self, item, spider):
        return item

#MongoDB存取
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


#Mysql存取
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
        sqlChangeList = 'insert into fairy.t_changeList(USERNAME,STATUS,STOCK_NAME,TARGET_WEIGHT,PRICE,PREV_WEIGHT_AJJUSTED,USERID,STOCK_SYMBOL,updated_at,sign) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sqlQuarterRankingItem = 'insert into fairy.t_QuarterRankingItem(name,symbol,rate,photo_domain,profile_image_url,create_time) values(%s,%s,%s,%s,%s)'
        if isinstance(item,ChangeListItem):
            try:
                    cursor.execute(sqlChangeList,(item['userName'],item['status'],item['stock_name'],item['target_weight'],item['price'],item['prev_weight_adjusted'],item['userId'],item['stock_symbol'],item['updated_at'],item['sign']))
                    dbObject.commit()
            except Exception,e:
                    print e
                    dbObject.rollback()
        elif isinstance(item,QuarterRankingItem):
            try:    
                    cursor.execute(sqlQuarterRankingItem,(item['name'],item['symbol'],item['rate'],item['photo_domain'],item['profile_image_url'],item['createTime']))

        return item
