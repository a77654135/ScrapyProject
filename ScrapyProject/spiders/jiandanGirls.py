# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import requests
from ScrapyProject.items.jiandanItem import JiandanItem
from scrapy.http import Request


base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class JiandanGirlsSpider(scrapy.Spider):
    name = 'jiandanGirls'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/ooxx/page-45']

    custom_settings = {
        "IMAGES_STORE": os.path.join(base_dir,'images/jiandan_girls'),
        "IMAGES_EXPIRES": 30,
        "IMAGES_THUMBS": {
            'small':(50,50),
            'big':(270,270),
        },
        "IMAGES_MIN_HEIGHT": 0,
        "IMAGES_MIN_WIDTH": 0,
        # 'ITEM_PIPELINES': {
        #     'ScrapyProject.pipelines.imagePipeline.ImagePipeline': 150,
        # },
        'DOWNLOADER_MIDDLEWARES': {
            'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 100,
        }
    }

    def parse(self, response):
        line_list = response.xpath("//div[@class='cp-pagenavi']/a/@href").extract()

        for link in line_list:
            yield Request(url="http:{}".format(link),callback=self.parse)

        img_list = response.xpath("//ol[@class='commentlist']/li//div[@class='text']//img/@src").extract()

        for img in img_list:
            item = JiandanItem()
            item["img_url"] =img
            yield item
            self.parse_img(img)



    def parse_img(self,img):
        res = requests.get(img)

        _,name = os.path.split(img)
        img_dir = os.path.join(base_dir,*["images","jiandan_girls"])
        with open(os.path.join(img_dir,name),"wb") as f:
            f.write(res.content)
            print "save image: " + img







