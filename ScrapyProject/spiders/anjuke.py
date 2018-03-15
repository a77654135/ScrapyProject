# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from ScrapyProject.items.anjukeItem import AnjukeItem
from scrapy.loader import ItemLoader

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://wh.fang.anjuke.com/loupan/all/']

    def parse(self, response):
        """
        name = scrapy.Field()                       #名字
        detail_link = scrapy.Field()                #详情链接
        position = scrapy.Field()                   #地点
        home_type = scrapy.Field()                  #户型
        home_area = scrapy.Field()                  #建筑面积
        onsale = scrapy.Field()                     #售卖状态
        wuyetp = scrapy.Field()                     #地产类型
        tags = scrapy.Field()                       #标签
        activities = scrapy.Field()                 #活动
        price = scrapy.Field()                      #售价
        phone = scrapy.Field()                      #联系电话
        img_url = scrapy.Field()                    #图片地址
        :param response:
        :return:
        """

        item_list = response.xpath("//div[@class='key-list']/div[@class='item-mod']")
        print "1111111111111111"
        print item_list
        for item in item_list:
            print "222222222222"
            l = ItemLoader(item = AnjukeItem(), selector=item, response=response)
            l.add_xpath("name","div[@class='infos']//span[@class='items-name']/text()")

            i = l.load_item()
            print i.name


