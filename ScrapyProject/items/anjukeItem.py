# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jokeItem
   Author :       talus
   date：          2018/3/13 0013
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

class AnjukeItem(scrapy.Item):
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