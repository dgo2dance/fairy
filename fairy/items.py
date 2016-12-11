# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


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
