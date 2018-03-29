# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     btbtdyItem
   Author :       talus
   date：          2018/3/28 0028
   Description :
-------------------------------------------------

"""
import scrapy

class BtbtdyItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    desc = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    type = scrapy.Field()
    grade = scrapy.Field()
    state = scrapy.Field()
    detail_url = scrapy.Field()
    download_list = scrapy.Field()
