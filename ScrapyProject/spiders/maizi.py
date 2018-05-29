# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import Request
from ScrapyProject.items.maiziItem import MaiziItem


class MaiziSpider(scrapy.Spider):
    name = 'maizi'
    allowed_domains = ['maiziedu.com']
    start_urls = ['http://www.maiziedu.com/course/all/']

    base_url = "http://www.maiziedu.com"

    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyProject.pipelines.spiderPipelines.maiziPipeline.MaiziPipeline': 300,
            # 'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
            # 'ScrapyProject.pipelines.txtPipeline.TxtPipeline': 600,
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'ScrapyProject.middlewares.rotate_useragent.RotateUserAgentMiddleware': 100,
        #     'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 200,
        # }
    }

    # def start_requests(self):
    #     # yield Request(url=r"http://www.maiziedu.com/course/all/",callback=self.parse)
    #     # yield Request(url=r"http://www.maiziedu.com/course/web-all/0-2/",callback=self.parse_category)
    #     yield Request(url=r"http://www.maiziedu.com/course/232/",callback=self.parse_detail)


    def parse(self, response):
        a_list = response.xpath("//div[@class='course-nav']/ul/li/a")

        for a in a_list:
            href = a.xpath("@href").extract_first()
            title = a.xpath("text()").extract_first()
            if re.search("all-all", href):
                continue

            link = "{}{}".format(self.base_url, href)
            meta = {"category": title}
            yield scrapy.Request(url=link, callback=self.parse_category, meta=meta)
            # return scrapy.Request(url=link, callback=self.parse_category, meta=meta)

    def parse_category(self, response):

        a_list = response.xpath("//ul[@class='course-lists']/li/a")
        meta = response.meta.copy()

        for a in a_list:
            detailUrl = "{}{}".format(self.base_url, a.xpath("@href").extract_first())
            meta["title"] = a.xpath("@title").extract_first()
            meta["detailUrl"] = detailUrl
            meta["vip"] = "vip" if re.search("vip_user", a.xpath("p/i[1]/@class").extract_first()) else "normal"
            meta["status"] = "end" if re.search("status_end", a.xpath("p/i[2]/@class").extract_first()) else "on"
            meta["img"] = "{}{}".format(self.base_url, a.xpath("p/img/@src").extract_first())
            meta["desc"] = a.xpath("div/p[@class='description']/text()").extract_first()
            meta["students"] = re.findall("\d+", a.xpath("div/p[@class='color99']/text()").extract_first())[0]

            yield Request(url=detailUrl, callback=self.parse_detail, meta=meta)

        h_list = response.xpath("//div[@class='zypage_div']/a/@href").extract()
        for h in h_list:
            href = "{}{}".format(self.base_url, h)
            yield Request(url=href, callback=self.parse_category, meta=response.meta.copy())


    def parse_detail(self, response):
        meta = response.meta.copy()
        # item = MaiziItem()
        a_list = response.xpath("//ul[@class='lesson-lists']/li/a")
        for a in a_list:
            href = a.xpath("@href").extract_first()
            course_name = a.xpath("span[@class='fl']/text()").extract_first()

            meta["course_url"] = "{}{}".format(self.base_url, href)
            meta["course_name"] = course_name

            yield Request(url=meta["course_url"], callback=self.parse_course, meta=meta)

    def parse_course(self, response):
        try:
            mp4 = re.findall("http.*\.mp4",response.text)[0]
            meta = response.meta.copy()
            # meta["course_video"] = mp4
            item = MaiziItem()
            item["category"] = meta["category"]
            item["title"] = meta["title"]
            item["detailUrl"] = meta["detailUrl"]
            item["vip"] = meta["vip"]
            item["status"] = meta["status"]
            item["img"] = meta["img"]
            item["desc"] = meta["desc"]
            item["students"] = meta["students"]

            course = {}
            course["course_url"] = meta["course_url"]
            course["course_name"] = meta["course_name"]
            course["course_video"] = mp4
            item["course"] = course
            yield item
        except:
            pass





