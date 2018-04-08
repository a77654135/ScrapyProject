# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ScrapyProject.items.btbaItem import BtbaItem


class BtbaSpider(scrapy.Spider):
    name = 'btba'
    allowed_domains = ['btba.com.cn']
    start_urls = ['http://btba.com.cn/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyProject.pipelines.spiderPipelines.btbaPipeline.BtbaPipeline': 300,
            # 'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'ScrapyProject.middlewares.rotate_useragent.RotateUserAgentMiddleware': 100,
        #     'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 200,
        # }
    }

    def start_requests(self):
        yield Request(url=ur"http://www.btba.com.cn/type/电影.html?page=1",callback=self.parse, meta={"category": u"电影"})
        yield Request(url=ur"http://www.btba.com.cn/type/电视剧.html?page=1",callback=self.parse, meta={"category": u"电视剧"})
        yield Request(url=ur"http://www.btba.com.cn/type/动画.html?page=1",callback=self.parse, meta={"category": u"动漫"})
        yield Request(url=ur"http://www.btba.com.cn/type/综艺.html?page=1",callback=self.parse, meta={"category": u"综艺"})
        yield Request(url=ur"http://www.btba.com.cn/type/纪录片.html?page=1",callback=self.parse, meta={"category": u"电影"})
        # yield Request(url=ur"http://www.btba.com.cn/bt/910215057213.html",callback=self.parse_item, meta={"category": u"电影"})

    """
    category = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    desc = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    type = scrapy.Field()
    grade = scrapy.Field()
    state = scrapy.Field()
    detail_url = scrapy.Field()
    download_list = scrapy.Field()
    """


    def parse(self, response):
        li_list = response.xpath("//div[@class='left']/ul/li")

        for li in li_list:
            meta_item = response.meta.copy()
            meta_item["cover"] = li.xpath("a/img/@lazy_src").extract_first()
            meta_item["detail_url"] = li.xpath("a/@href").extract_first()
            meta_item["name"] = li.xpath("div/h3/a/text()").extract_first().split("/")[0]
            meta_item["country"] = li.xpath("div/p[3]/text()").extract_first().split(u"：")[1]
            meta_item["year"] = li.xpath("div/h3/b/text()").extract_first()
            meta_item["grade"] = li.xpath("div/p[4]/b/text()").extract_first()
            yield Request(url=meta_item["detail_url"], callback=self.parse_item, meta=meta_item)


        link_list = response.xpath("//div[@id='page']/a/@href").extract()
        for link in link_list:
            yield Request(url="{}{}".format(response.url.split("?")[0],link), callback=self.parse, meta=response.meta.copy())


    def parse_item(self, response):
        a_list = response.xpath("//div[@class='btinfo']/h3/a")
        for a in a_list:
            meta_item = response.meta.copy()
            href = a.xpath("@href").extract_first()
            text = a.xpath("text()").extract()
            meta_item["title"] = "{}{}{}{}".format(a.xpath("i/text()").extract_first(),text[0],a.xpath("b/text()").extract_first(),text[1])
            yield Request(url=href, callback=self.parse_detail, meta=meta_item)


    def parse_detail(self, response):
        item = BtbaItem()
        meta = response.meta

        item["name"] = meta["name"]
        item["category"] = meta["category"]
        item["cover"] = meta["cover"]
        item["year"] = meta["year"]
        item["country"] = meta["country"]
        item["grade"] = meta["grade"]
        item["detail_url"] = meta["detail_url"]
        item["download_list"] = {"title": meta["title"], "url": response.xpath("//textarea[@id='status']/text()").extract_first()}
        item["desc"] = None
        item["type"] = None
        item["state"] = None

        yield item