# encoding=utf-8
import re
import datetime
import time
import json
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from fairy.items import ChangeListItem,QuarterRankingItem

class Spider(CrawlSpider):
    name = "fairy"
    host = "https://xueqiu.cn"

    

    start_urls = [
    ]
    # try:
    #url_head = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rebalancing/history?cube_symbol=SP1000132"
       #     for line in file_object:
    #start_urls.append(url_head)
       #     for url in self.start_urls:
       #         yield self.make_requests_from_url(url)
       # finally:
       #     file_object.close()
            #years_object.close()
    scrawl_ID = set(start_urls)
    finish_ID = set()  # 记录已爬url
    print 'scrawl_ID LENGTH:',len(scrawl_ID)

    def  get_id(self):
         url_quarter = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=QUARTER&page=1"
         yield Request(url=url_quarter, callback=self.parse0) 



    def start_requests(self):

        #self.get_id()
        url_quarter = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=QUARTER&page=1"
        yield Request(url=url_quarter, meta={"ID": 1},callback=self.parse0) 
        
        print 'len~~:',len(self.scrawl_ID)

        while len(self.scrawl_ID)>0:
                ID = self.scrawl_ID.pop()
                print 'scrawl_ID LENGTH NEIBU:',len(self.scrawl_ID)
                print 'ID:',ID
                self.finish_ID.add(ID)  # 加入已爬队列
                ID = str(ID)
                url_Fairy = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rebalancing/history?cube_symbol=%s" % ID
                yield Request(url=url_Fairy, meta={"ID": ID}, callback=self.parse)  # 去爬json

    def parse0(self,response):
        selector = Selector(response)
        con = json.loads(response.body_as_unicode(),encoding="gbk")
        for m in con['result_data']['list']:
            quarterRankingItem = QuarterRankingItem()
            quarterRankingItem["name"] = m['name']
            quarterRankingItem["symbol"] = m['symbol']
            quarterRankingItem["rate"] = m['rate']
            quarterRankingItem["createTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            quarterRankingItem["photo_domain"] = m['user']['photo_domain']
            quarterRankingItem["profile_image_url"] = m['user']['profile_image_url']
            self.scrawl_ID.add(m['symbol'])
            print 'len~~0:',len(self.scrawl_ID)
            print 'm_symbol:',m['symbol']
            print 'len~~1:',len(self.scrawl_ID)
            yield quarterRankingItem

    def parse(self, response):
        """ 抓取json数据 """
        selector = Selector(response)
        con = json.loads(response.body_as_unicode(),encoding="gbk") 

        for m in con['list']:
           #     print 'status:',m['status']
           #     print 'stock_name:',m['rebalancing_histories'][0]['stock_name']
           #     print 'target_weight:',m['rebalancing_histories'][0]['target_weight']
           #     print 'prev_weight_adjusted:',m['rebalancing_histories'][0]['prev_weight_adjusted']
           #     print 'updated_at:',str(m['rebalancing_histories'][0]['updated_at'])[0:10]

           #     print type(m['rebalancing_histories'][0]['updated_at'])
           #     print 'stock_symbol:',m['rebalancing_histories'][0]['stock_symbol']
                changeListItem=ChangeListItem()
                changeListItem["userId"]=response.meta["ID"]
                changeListItem["status"]=m['status']
                changeListItem["stock_name"]=m['rebalancing_histories'][0]['stock_name']
                changeListItem["target_weight"]=m['rebalancing_histories'][0]['target_weight']
                changeListItem["price"]=m['rebalancing_histories'][0]['price']
                changeListItem["prev_weight_adjusted"]=m['rebalancing_histories'][0]['prev_weight_adjusted']
                changeListItem["updated_at"]=datetime.datetime.utcfromtimestamp(float(str(m['rebalancing_histories'][0]['updated_at'])[0:10]))
                changeListItem["stock_symbol"]=m['rebalancing_histories'][0]['stock_symbol']
                yield changeListItem


        #dic 类型遍历
        #for key ,name in con.items():
        #    print key,':',name
      





""" 遍历字典
    
     #for k in d.keys():
     #self.print_dict(k, d[k])
    
    #for k in d.keys():
     #self.print_dict(k, d[k])
    def print_dict(self,k, v):
        if isinstance(v, dict):
           print k, v
           for kk in v.keys():
             print_dict(kk, v[kk])
        else:
           print k, v
 
"""