# -*- coding: utf-8 -*-
import datetime

import logging
import scrapy
from bs4 import BeautifulSoup

from crawlAutohomeUsers.items import autouserItem

logger=logging.getLogger("spiderusers")
class SpiderusersSpider(scrapy.Spider):
    name = 'spiderusers'
    allowed_domains = ['i.autohome.com.cn','iservice.autohome.com.cn']

    start_urls = ['https://i.autohome.com.cn/{userid}']

    #主页
    starturl='https://i.autohome.com.cn/{userid}'
    #https://i.autohome.com.cn/60383084
    #他的主贴
    baseurl='http://iservice.autohome.com.cn/clubapp/OtherTopic-{userid}-all-1.html'
    #个人资料
    uinfourl='https://i.autohome.com.cn/{userid}/info'

    def __init__(self, **kwargs):
        self.count = 0
        self.startuid=10000
        self.enduid=60469999
        #300001

    def start_requests(self):
        # for url in self.start_urls:
            # self._wait()

        for uid in range(int(self.startuid),int(self.enduid)):
            uid=str(uid)
            logger.log(logging.INFO,'当前用户ID=%s'%uid)
            url=self.starturl.replace('{userid}',uid)
            request = scrapy.Request(url=url, callback=self.parse)
            # request= scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # https://i.autohome.com.cn/25587150
        curl=response.url
        # response.css('')
        usercenter = soup.find('div', class_='user-center')
        #用户信息
        userid = curl[curl.find('cn') + 3:len(curl)]
        usernametag = usercenter.find('h1', class_='user-name')
        username= usernametag.find('b').get_text(strip=True)
        usersex= usernametag.findAll('span')[1].attrs['class'][0]
        # 用户关注，粉丝
        userlv= usercenter.find('div',class_='user-lv')
        usersgz=userlv.findAll('a', 'state-mes')
        # print(usersgz)
        guanzhu = usersgz[0].find('span').get_text(strip=True)
        fensi = usersgz[1].find('span').get_text(strip=True)
        #用户地址
        useraddr= userlv.find('a',class_='state-pos').get_text(strip=True)

        userstate= usercenter.find('div',class_='user-state').find('div', class_='user-con')
        #里程值
        otherHelpVal = userstate.find(id='otherHelpVal').get_text(strip=True)
        jhtopicCount = userstate.find(id='jhtopicCount').get_text(strip=True)
        topicCount = userstate.find(id='topicCount').get_text(strip=True)

        #车库
        carport = soup.find('div', class_='carport')
        # print(carport)
        cartype= carport.findAll('a',class_='car-name')

        cartypes=''
        for car in cartype :
            cartypes = car.attrs['title']+';'
        carCount = carport.find('div', class_="carport-title").find('h3').find('span').get_text(strip=True)
        #车辆个数
        carCount=carCount[carCount.find('(')+1:carCount.find(')')]

        #menuBox
        menuBox=soup.find('div',class_='menuBox')
        luntanurl=menuBox.find('a',class_='ico_lt01').attrs['href']

        print('userid',userid)
        print('username',username)
        # print('usersex',usersex)
        print('guanzhu',guanzhu)
        print('fensi',fensi)
        print('useraddr',useraddr)
        print('otherHelpVal',otherHelpVal)
        print('jhtopicCount',jhtopicCount)
        print('topicCount',topicCount)
        print('cartypes', cartypes)
        print('carCount',carCount)

        # url=response.urljoin(luntanurl)

        item=autouserItem()
        item['userid'] = userid
        item['username'] = username
        # item['usersex'] = usersex
        item['guanzhu'] = guanzhu
        item['fensi'] = fensi
        item['useraddr'] = useraddr
        item['otherHelpVal'] = otherHelpVal
        item['jhtopicCount'] = jhtopicCount
        item['topicCount'] = topicCount
        item['cartypes'] = cartypes
        item['carCount'] = carCount
        item['userurl'] = curl


        # http://iservice.autohome.com.cn/clubapp/OtherTopic-60383084-all-1.html
        tpurl = self.baseurl.replace('{userid}', userid)
        print('他的主贴：',tpurl)
        request=scrapy.Request(url=tpurl,callback=self.parseTopicTie)
        request.meta['item']=item
        yield request

    def parseuinfo(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'lxml')
        udata = soup.find('div', class_='uData')
        infos = udata.findAll('p')

        # http://iservice.autohome.com.cn/clubapp/OtherTopic-60383084-all-1.html
        tpurl = self.baseurl.replace('{userid}', item['userid'])
        print('他的主贴：',tpurl)
        request=scrapy.Request(url=tpurl,callback=self.parseTopicTie)
        request.meta['item']=item
        yield request

    def parseTopicTie(self,response):
        # print(response.text)
        item=response.meta['item']
        turl=response.url

        soup = BeautifulSoup(response.text, 'lxml')

        clmm = soup.find('div', class_='cl_m')
        # print('clmm=',clmm)
        #注册时间
        zcdate = clmm.find('li', class_='item-w1').find('span').get_text(strip=True)
        #最后登录时间
        zhdate= response.css('body  div.cl_m.m_t27  div  ul:nth-child(5)  li:nth-child(2)  span::text').extract_first()

        zhdate= response.css('body  div.cl_m.m_t27  div  ul:nth-child(5)  li:nth-child(2)  span::text').extract_first()
#body > div.cl_m.m_t27 > div > ul:nth-child(3) > li:nth-child(3) > a
#body > div.cl_m.m_t27 > div > ul:nth-child(3) > li:nth-child(2) > a

        ultext=response.css('body  div.cl_m.m_t27  div  ul:nth-child(3) li *::text').extract()
        texts=''
        for l in ultext:
            texts=texts+l.strip()

        guanzhucar = texts[texts.find('车：') + 2:len(texts)]
        print('texts=',texts)
        # print('zcdate=', zcdate)
        # print('zhdate=', zhdate)
        item['guanzhucar'] = guanzhucar
        item['zcdate'] = zcdate
        item['zhdate'] = zhdate
        item['usertopicurl'] = turl


        crawldate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['crawldate'] = crawldate
        yield item


