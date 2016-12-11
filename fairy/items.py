# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field

# 定义某个人的调仓历史
class ChangeListItem(Item):
    """ 个人信息 """
    userId = Field()
    status = Field()  # 交易ID
    stock_symbol = Field()  # 股票代码
    price = Field()  # 交易价格
    prev_weight_adjusted = Field()  # 之前权重
    target_weight = Field()  # 目标权重
    updated_at = Field()  # 交易时间
    stock_name = Field() #股票名字

#定义最近三个月实盘大赛排名
class QuarterRankingItem(Item):
    name = Field()
    symbol = Field()
    rate = Field()
    createTime = Field()
    photo_domain = Field()
    profile_image_url = Field()

#定义最近一个月实盘大赛排名
class MonthRankingItem(Item):
    name = Field()
    symbol = Field()
    rate = Field()
    createTime = Field()
    photo_domain = Field()
    profile_image_url = Field()

#定义最近一周实盘大赛排名
class WeekRankingItem(Item):
    name = Field()
    symbol = Field()
    rate = Field()
    createTime = Field()
    photo_domain = Field()
    profile_image_url = Field()