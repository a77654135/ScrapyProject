# -*- coding: utf-8 -*-
import scrapy
import os
import re
import requests
import random


class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = [
        'https://www.qiushibaike.com/',
        "https://www.qiushibaike.com/hot/",
        "https://www.qiushibaike.com/imgrank/",
        "https://www.qiushibaike.com/text/",
        "https://www.qiushibaike.com/history/",
        "https://www.qiushibaike.com/pic/",
        "https://www.qiushibaike.com/textnew/",
    ]

    base_url = 'https://www.qiushibaike.com'

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'ScrapyProject.pipelines.spiderPipelines.btbaPipeline.BtbaPipeline': 300,
            # 'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'ScrapyProject.middlewares.rotate_useragent.RotateUserAgentMiddleware': 100,
        #     'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 200,
        # }
    }

    def start_requests(self):

        self.name_cache = set()
        self.csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),*["data","csv","qiushibaike.csv"])
        self.img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),*["data","img"])
        self.id = 1

        with open(self.csv_file,"w") as f:
            f.write("id,name,head,sex\n")

        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        item_list = response.xpath("//div[@class='author clearfix']")
        for item in item_list:
            pic_url = "{}{}".format("https:",item.xpath("a/img/@src").extract_first())
            name = item.xpath("a/h2/text()").extract_first()
            sex_icon = item.xpath("div/@class").extract_first()
            if not name or not pic_url:
                continue
            if not name in self.name_cache:
                self.name_cache.add(name)
                if sex_icon:
                    if re.search("women",sex_icon):
                        sex = "girl"
                    else:
                        sex = "boy"
                else:
                    sex = "boy" if random.random() < 0.5 else "girl"

                pic_name = "{}_{}.jpg".format(sex,self.id)
                with open(self.csv_file,"a") as f:
                    f.write('"{}","{}","{}","{}"\n'.format(self.id,name,pic_name,sex))

                self.id += 1
                res = requests.get(pic_url)
                with open(os.path.join(self.img_dir,pic_name), "wb") as f:
                    f.write(res.content)
                    print "save image: " + pic_name

        page_list = response.xpath("//ul[@class='pagination']/li/a/@href").extract()
        for page in page_list:
            yield scrapy.Request(url="{}{}".format(self.base_url,page), callback=self.parse)

