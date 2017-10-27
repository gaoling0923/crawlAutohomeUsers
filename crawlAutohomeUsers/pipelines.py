# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from _md5 import md5

import happybase
import pymongo
from datetime import datetime
# from twisted.enterprise import adbapi

# import importlib,sys
from scrapy.conf import settings

import datetime
import random

from crawlAutohomeUsers.items import autouserItem


class randomRowKey(object):
    # 生产唯一key
    def getRowKey(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

class HBaseUsersPipeline(object):
    def __init__(self):
        host = settings['HBASE_HOST']
        self.port = settings['HBASE_PORT']
        self.table_name = settings['HBASE_TABLE']
        # port = settings['HBASE_PORT']
        self.connection = happybase.Connection(host=host,port=self.port,timeout=None, autoconnect=False)



    def process_item(self, item, spider):
        # cl = dict(item)
        randomrkey = randomRowKey()
        rowkey = randomrkey.getRowKey()
        self.connection.open()
        table = self.connection.table(self.table_name)
        # b= self.table.batch()
        if isinstance(item, autouserItem):
            # self.table.put('text', cl)
            print('进入pipline')
            userid = item.get('userid', '')
            username = item.get('username', '')
            usersex = item.get('usersex', '')
            guanzhu = item.get('guanzhu', '')
            fensi = item.get('fensi', '')
            useraddr = item.get('useraddr', '')
            lichengzhi = item.get('lichengzhi', '')
            jhtopicCount = item.get('jhtopicCount', '')
            topicCount = item.get('topicCount', '')
            cartypes = item.get('cartypes', '')
            carCount = item.get('carCount', '')
            guanzhucar = item.get('guanzhucar', '')
            zcdate = item.get('zcdate', '')
            zhdate = item.get('zhdate', '')
            userurl = item.get('userurl', '')
            usertopicurl = item.get('usertopicurl', '')
            crawldate = item.get('crawldate', '')
            table.put(md5(str(rowkey).encode('utf-8')).hexdigest(), {
                 'cf1:userid':userid,
                 'cf1:username':username,
                 'cf1:usersex':usersex,
                 'cf1:guanzhu':guanzhu,
                 'cf1:fensi':fensi,
                 'cf1:useraddr':useraddr,
                 'cf1:lichengzhi':lichengzhi,
                 'cf1:jhtopicCount':jhtopicCount,
                 'cf1:topicCount':topicCount,
                 'cf1:cartypes':cartypes,
                 'cf1:carCount':carCount,
                 'cf1:guanzhucar':guanzhucar,
                 'cf1:zcdate':zcdate,
                 'cf1:zhdate':zhdate,
                 'cf1:userurl':userurl,
                 'cf1:usertopicurl':usertopicurl,
                 'cf1:crawldate':crawldate
                                     })
            # b.send()
        self.connection.close()
        return item
class CrawlautohomeusersPipeline(object):
    def process_item(self, item, spider):
        return item
