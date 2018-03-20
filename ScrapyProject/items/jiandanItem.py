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

class JiandanItem(scrapy.Item):
    img_url = scrapy.Field()