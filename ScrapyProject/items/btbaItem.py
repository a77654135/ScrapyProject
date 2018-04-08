# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     btbaItem
   Author :       talus
   date：          2018/4/8 0008
   Description :
-------------------------------------------------

"""
import sys

import scrapy

class BtbaItem(scrapy.Item):
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