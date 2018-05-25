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

    # def start_requests(self):
    #     # yield Request(url=r"http://www.maiziedu.com/course/all/",callback=self.parse)
    #     yield Request(url=r"http://www.maiziedu.com/course/web-all/0-2/",callback=self.parse_category)


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
        meta = response.meta

        for a in a_list:
            item = MaiziItem()
            item["category"] = meta["category"]
            detailUrl = "{}{}".format(self.base_url, a.xpath("@href").extract_first())
            item["title"] = a.xpath("@title").extract_first()
            item["detailUrl"] = detailUrl
            item["vip"] = "vip" if re.search("vip_user", a.xpath("p/i[1]/@class").extract_first()) else "normal"
            item["status"] = "end" if re.search("status_end", a.xpath("p/i[2]/@class").extract_first()) else "on"
            item["img"] = "{}{}".format(self.base_url, a.xpath("p/img/@src").extract_first())
            # item["desc"] = a.xpath("div/p[@class='description']/text()").extract_first()
            item["students"] = re.findall("\d+", a.xpath("div/p[@class='color99']/text()").extract_first())[0]

            yield item

        h_list = response.xpath("//div[@class='zypage_div']/a/@href").extract()
        for h in h_list:
            href = "{}{}".format(self.base_url, h)
            yield Request(url=href, callback=self.parse_category, meta=response.meta.copy())




    # def parse_courses(self, response):
    #     a_list = response.xpath("//ul[@class='course-lists']/li/a")
    #     meta = response.meta
    #
    #     for a in a_list:
    #         item = MaiziItem()
    #         item["category"] = meta["category"]
    #         detailUrl = "{}{}".format(self.base_url, a.xpath("@href").extract_first())
    #         item["title"] = a.xpath("@title").extract_first()
    #         item["detailUrl"] = detailUrl
    #         item["vip"] = "vip" if re.search("vip_user",a.xpath("p/i[1]/@class").extract_first()) else "normal"
    #         item["status"] = "end" if re.search("status_end",a.xpath("p/i[2]/@class").extract_first()) else "on"
    #         item["img"] = "{}{}".format(self.base_url, a.xpath("p/img/@src").extract_first())
    #         # item["desc"] = a.xpath("div/p[@class='description']/text()").extract_first()
    #         item["students"] = re.findall("\d+",a.xpath("div/p[@class='color99']/text()").extract_first())[0]
    #
    #         yield item
