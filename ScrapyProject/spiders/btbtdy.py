# -*- coding: utf-8 -*-
import scrapy
import re
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
            'ScrapyProject.pipelines.spiderPipelines.btbtdyPipeline.BtbtdyPipeline': 300,
            'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
            # 'ScrapyProject.pipelines.txtPipeline.TxtPipeline': 600,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'ScrapyProject.middlewares.rotate_useragent.RotateUserAgentMiddleware': 100,
            'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 200,
        }
    }

    def start_requests(self):
        yield Request(url=r"http://www.btbtdy.com/screen/1-----time-1.html",callback=self.parse_list, meta={"category": u"电影"})
        yield Request(url=r"http://www.btbtdy.com/screen/30-----time-1.html",callback=self.parse_list, meta={"category": u"电视剧"})
        yield Request(url=r"http://www.btbtdy.com/screen/34-----time-1.html",callback=self.parse_list, meta={"category": u"动漫"})
        yield Request(url=r"http://www.btbtdy.com/screen/29-----time-1.html",callback=self.parse_list, meta={"category": u"蓝光"})
        yield Request(url=r"http://www.btbtdy.com/screen/28-----time-1.html",callback=self.parse_list, meta={"category": u"3D电影"})
        yield Request(url=r"http://www.btbtdy.com/screen/38-----time-1.html",callback=self.parse_list, meta={"category": u"VR电影"})
        # yield Request(url=r"http://www.btbtdy.com/btdy/dy12587.html",callback=self.parse_item, meta={"category": "movieVR"})

    def parse_list(self, response):
        meta_total = response.meta
        last_href = response.xpath("//div[@class='pages']/a[last()]/@href").extract_first()
        if last_href:
            idx = re.findall(r".*time-(\d+).html",last_href)
            if idx and len(idx):
                idx = int(idx[0])
                for i in range(1,idx+1,1):
                    href = last_href.replace("time-{}.html".format(idx),"time-{}.html".format(i))
                    df = False
                    if i == 1:
                        df = True
                    yield Request(url="{}{}".format(BtbtdySpider.link_url,href),callback=self.parse,meta=meta_total.copy(),dont_filter=df)



    def parse(self, response):
        meta_total = response.meta

        movie_list= response.xpath("//div[@class='list_su']/ul/li")
        for movie_item in movie_list:
            meta = meta_total.copy()
            meta["cover"] = movie_item.xpath("div[@class='liimg']//img[@class='lazy']/@data-src").extract_first()
            meta["name"] = movie_item.xpath("div[@class='cts_ms']/p[@class='title']/a/text()").extract_first()
            meta["grade"] = movie_item.xpath("div[@class='cts_ms']/p[@class='title']/span/text()").extract_first()
            meta["desc"] = movie_item.xpath("div[@class='cts_ms']/p[@class='des']/text()").extract_first()
            meta["detail_url"] = BtbtdySpider.base_url + movie_item.xpath("div[@class='liimg']/a[@class='pic_link']/@href").extract_first()
            meta["state"] = movie_item.xpath("div[@class='liimg']/a[@class='pic_link']/span/text()").extract_first()

            yield Request(url=meta["detail_url"],callback=self.parse_item,meta=meta)

        # link_list = response.xpath("//div[@class='pages']/a/@href").extract()
        # for link in link_list:
        #     yield Request(url=BtbtdySpider.link_url + link, callback=self.parse, meta=meta_total.copy())


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

