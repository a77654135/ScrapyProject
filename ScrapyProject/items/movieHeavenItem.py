# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     movieHeavenItem
   Author :       talus
   date：          2018/3/21 0021
   Description :
-------------------------------------------------

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

class MovieItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    grade = scrapy.Field()
    desc = scrapy.Field()
    downloadLink = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    detailLink = scrapy.Field()