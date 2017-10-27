# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class autouserItem(scrapy.Item):


    userid = scrapy.Field()
    username = scrapy.Field()
    usersex = scrapy.Field()
    guanzhu = scrapy.Field()
    fensi = scrapy.Field()
    useraddr = scrapy.Field()
    otherHelpVal = scrapy.Field()
    jhtopicCount = scrapy.Field()
    topicCount = scrapy.Field()
    cartypes = scrapy.Field()
    carCount = scrapy.Field()
    guanzhucar = scrapy.Field()
    zcdate = scrapy.Field()
    zhdate = scrapy.Field()
    userurl = scrapy.Field()
    usertopicurl = scrapy.Field()
    crawldate = scrapy.Field()

class CrawlautohomeusersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
