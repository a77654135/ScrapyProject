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

class JokeItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    view_count = scrapy.Field()