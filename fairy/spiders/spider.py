# encoding=utf-8
import re
import datetime
import time
import json
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from fairy.items import ChangeListItem,QuarterRankingItem
import pdb



class Spider(CrawlSpider):
    name = "fairy"
    host = "https://xueqiu.cn"

    start_urls = ['1','2','3','4','5',
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
    finish_ID = set()  # 记录已爬人员
    print 'scrawl_ID LENGTH:',len(scrawl_ID)

    def  get_id(self):
         url_quarter = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=QUARTER&page=1"
         Request(url=url_quarter, callback=self.parse0) 



    def start_requests(self):

        #self.get_id()
        while len(self.scrawl_ID)>0:
            ID = self.scrawl_ID.pop()
            url_quarter = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=QUARTER&page=%s" % ID
            url_month = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=MONTH&page=%s" % ID
            url_week = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=WEEK&page=%s" % ID
            url_year = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rank?tid=PAMID&period=YEAR&page=%s" % ID
            yield Request(url=url_quarter, meta={"ID": 1,"SIGN":"QUARTER"},callback=self.parse2) 
            yield Request(url=url_month, meta={"ID": 1,"SIGN":"MONTH"},callback=self.parse2) 
            yield Request(url=url_week, meta={"ID": 1,"SIGN":"WEEK"},callback=self.parse2) 
            yield Request(url=url_year, meta={"ID": 1,"SIGN":"YEAR"},callback=self.parse2) 

        
            print 'len~~:',len(self.scrawl_ID)
 
        """
        while len(self.scrawl_ID)>0:
                ID = self.scrawl_ID.pop()
                print 'scrawl_ID LENGTH NEIBU:',len(self.scrawl_ID)
                print 'ID:',ID
                self.finish_ID.add(ID)  # 加入已爬队列
                ID = str(ID)
                url_Fairy = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rebalancing/history?cube_symbol=%s" % ID
                yield Request(url=url_Fairy, meta={"ID": ID}, callback=self.parse1)  # 去爬调整历史
        """

    def parse2(self,response):
        selector = Selector(response)
        print 'parse0'
        con = json.loads(response.body_as_unicode(),encoding="gbk")
        for m in con['result_data']['list']:
            quarterRankingItem = QuarterRankingItem()
            quarterRankingItem["name"] = m['name']
            quarterRankingItem["symbol"] = m['symbol']
            quarterRankingItem["rate"] = m['rate']
            quarterRankingItem["sign"] = response.meta["SIGN"]
            quarterRankingItem["createTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            quarterRankingItem["photo_domain"] = m['user']['photo_domain']
            quarterRankingItem["profile_image_url"] = m['user']['profile_image_url']
            yield quarterRankingItem
            if m['symbol'] not in self.finish_ID:
                url_Fairy = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rebalancing/history?cube_symbol=%s" % m['symbol']
                yield Request(url=url_Fairy, meta={"ID": m['symbol'],"NAME":m['name'],"SIGN":response.meta["SIGN"]}, callback=self.parse1)  # 去爬调整历史


    def parse1(self, response):
        """ 抓取json数据 """
        selector = Selector(response)
        con = json.loads(response.body_as_unicode(),encoding="gbk") 
        #假如已爬队列
        if response.meta["ID"] not in self.finish_ID:
            self.finish_ID.add(response.meta["ID"])

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
                changeListItem["sign"]=response.meta["SIGN"]
                changeListItem["userName"]=response.meta["NAME"]
                changeListItem["status"]=m['status']
                changeListItem["stock_name"]=m['rebalancing_histories'][0]['stock_name']
                changeListItem["target_weight"]=m['rebalancing_histories'][0]['target_weight']
                changeListItem["price"]=m['rebalancing_histories'][0]['price']
                changeListItem["prev_weight_adjusted"]=m['rebalancing_histories'][0]['prev_weight_adjusted']
            #   changeListItem["updated_at"]=datetime.datetime.utcfromtimestamp(float(str(m['rebalancing_histories'][0]['updated_at'])[0:10]))
                changeListItem["updated_at"]=time.localtime(float(str(m['rebalancing_histories'][0]['updated_at'])[0:10]))
                changeListItem["stock_symbol"]=m['rebalancing_histories'][0]['stock_symbol']
                yield changeListItem
        #pdb.set_trace()
        if  con['page']< con['maxPage']:
            nextPage = con['page']+1
            print '------nextPage',nextPage
            url_next = "https://xueqiu.com/service/tc/snowx/PAMID/cubes/rebalancing/history?cube_symbol=%s&page=%s" % (response.meta["ID"],nextPage)
            print url_next;
            yield Request(url=url_next, meta={"ID": response.meta["ID"],"SIGN":response.meta["SIGN"],"NAME":response.meta["NAME"]}, callback=self.parse1)
     
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