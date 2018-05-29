#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'talus'

import scrapy

class MaiziItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    vip = scrapy.Field()
    status = scrapy.Field()
    img = scrapy.Field()
    desc = scrapy.Field()
    students = scrapy.Field()
    detailUrl = scrapy.Field()
    course = scrapy.Field()
