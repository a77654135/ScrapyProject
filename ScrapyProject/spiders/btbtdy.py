# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ScrapyProject.items.btbtdyItem import BtbtdyItem


class BtbtdySpider(scrapy.Spider):
    name = 'btbtdy'
    allowed_domains = ['btbtdy.com']
    start_urls = ['http://btbtdy.com/']

    base_url = r"http://www.btbtdy.com"
    link_url = r"http://www.btbtdy.com/screen/"

    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyProject.pipelines.mongoPipeline.MongoPipeline': 300,
            'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
            # 'ScrapyProject.pipelines.txtPipeline.TxtPipeline': 600,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'ScrapyProject.middlewares.rotate_useragent.RotateUserAgentMiddleware': 100,
            'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 200,
        }
    }

    def start_requests(self):
        yield Request(url=r"http://www.btbtdy.com/screen/1-----time-1.html",callback=self.parse, meta={"category": "movie"})
        yield Request(url=r"http://www.btbtdy.com/screen/30-----time-1.html",callback=self.parse, meta={"category": "series"})
        yield Request(url=r"http://www.btbtdy.com/screen/34-----time-1.html",callback=self.parse, meta={"category": "cartoon"})
        yield Request(url=r"http://www.btbtdy.com/screen/29-----time-1.html",callback=self.parse, meta={"category": "languang"})
        yield Request(url=r"http://www.btbtdy.com/screen/28-----time-1.html",callback=self.parse, meta={"category": "movie3D"})
        yield Request(url=r"http://www.btbtdy.com/screen/38-----time-1.html",callback=self.parse, meta={"category": "movieVR"})
        # yield Request(url=r"http://www.btbtdy.com/btdy/dy12587.html",callback=self.parse_item, meta={"category": "movieVR"})

    def parse(self, response):
        meta_total = response.meta

        movie_list= response.xpath("//div[@class='list_su']/ul/li")
        print len(movie_list)
        for movie_item in movie_list:
            meta = meta_total.copy()
            meta["cover"] = movie_item.xpath("div[@class='liimg']//img[@class='lazy']/@data-src").extract_first()
            meta["name"] = movie_item.xpath("div[@class='cts_ms']/p[@class='title']/a/text()").extract_first()
            meta["grade"] = movie_item.xpath("div[@class='cts_ms']/p[@class='title']/span/text()").extract_first()
            meta["desc"] = movie_item.xpath("div[@class='cts_ms']/p[@class='des']/text()").extract_first()
            meta["detail_url"] = BtbtdySpider.base_url + movie_item.xpath("div[@class='liimg']/a[@class='pic_link']/@href").extract_first()
            meta["state"] = movie_item.xpath("div[@class='liimg']/a[@class='pic_link']/span/text()").extract_first()

            # print meta["cover"]
            # print meta["name"]
            # print meta["grade"]
            # print meta["desc"]
            # print meta["detail_url"]
            # print meta["state"]
            # print ""

            yield Request(url=meta["detail_url"],callback=self.parse_item,meta=meta)

        link_list = response.xpath("//div[@class='pages']/a/@href").extract()
        for link in link_list:
            yield Request(url=BtbtdySpider.link_url + link, callback=self.parse, meta=meta_total.copy())


    def parse_item(self, response):
        down_list = response.xpath("//ul[@class='p_list_02']/li")
        item = BtbtdyItem()
        meta = response.meta
        download_list = []

        item["category"] = meta["category"]
        item["name"] = meta["name"]
        item["cover"] = meta["cover"]
        item["grade"] = meta["grade"]
        item["desc"] = meta["desc"]
        item["detail_url"] = meta["detail_url"]
        if meta["state"]:
            item["state"] = meta["state"]

        for down in down_list:
            down_item = {}
            down_item["title"] = down.xpath("a/@title").extract_first()
            down_item["url"] = down.xpath("span/a/@href").extract_first()
            download_list.append(down_item)

        item["download_list"] = download_list
        yield item

