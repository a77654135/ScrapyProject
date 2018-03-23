# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re

from ScrapyProject.items.movieHeavenItem import MovieItem

class MovieHeavenSpider(scrapy.Spider):
    name = 'movie_heaven'
    allowed_domains = ['dy2018.com']
    start_urls = ['https://www.dy2018.com/']

    base_url = r"https://www.dy2018.com"

    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyProject.pipelines.movieHeavenPipeline.MovieHeavenPipeline': 20,
            # 'ScrapyProject.pipelines.mongoPipeline.MongoPipeline': 300,
            'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
            'ScrapyProject.pipelines.txtPipeline.TxtPipeline': 600,
        }
    }

    # def start_requests(self):
    #     yield scrapy.Request(url=r"https://www.dy2018.com/i/98652.html",callback=self.parse_series_detail,dont_filter=True)

    def parse(self, response):
        menu_list = response.xpath("//div[@id='menu']//a/@href").extract()

        for menu in menu_list:
            if re.match(r"/[0-9]+/",menu):
                yield scrapy.Request("{}{}".format(MovieHeavenSpider.base_url,menu),callback=self.parse_movie,dont_filter=True)
            elif re.match(r"/html/.*",menu):
                yield scrapy.Request("{}{}".format(MovieHeavenSpider.base_url, menu), callback=self.parse_series,dont_filter=True)

    def parse_movie(self, response):

        link_list = response.xpath("//select[@name='select']/option/@value").extract()
        for link in link_list:
            yield scrapy.Request("{}{}".format(MovieHeavenSpider.base_url, link), callback=self.parse_movie_sheet,dont_filter=True)

    def parse_movie_sheet(self,response):
        table_list = response.xpath("//div[@class='co_content8']//table")
        for table in table_list:
            link = table.xpath("tr//a[@class='ulink' and @title]/@href").extract_first()    #详细链接
            yield scrapy.Request("{}{}".format(MovieHeavenSpider.base_url, link), callback=self.parse_movie_detail,dont_filter=True)

    def parse_movie_detail(self,response):
        item = MovieItem()
        item["title"] = response.xpath("//div[@class='title_all']/h1/text()").extract_first()
        item["grade"] = response.xpath("//div[@class='co_content8']//strong[@class='rank']/text()").extract_first()
        item["date"] = response.xpath("//div[@class='co_content8']//span[@class='updatetime']/text()").re("[0-9-]+")[0]
        # item["desc"] = response.xpath("//div[@id='Zoom']/p/text()").extract()
        item["downloadLink"] = response.xpath("//td[starts-with(@style,'WORD-WRAP')]//a/text()").extract()
        item["type"] = response.xpath("//div[@class='co_content8']//div[@class='position']/span[2]/a/text()").extract()
        item["category"] = "movie"
        item["detailLink"] = response.url
        yield item


    def parse_series(self, response):
        link_list = response.xpath("//select[@name='select']/option/@value").extract()
        for link in link_list:
            yield scrapy.Request("{}{}".format(MovieHeavenSpider.base_url, link), callback=self.parse_series_sheet,dont_filter=True)

    def parse_series_sheet(self, response):
        table_list = response.xpath("//div[@class='co_content8']//table")
        for table in table_list:
            link = table.xpath("tr//a[@class='ulink' and @title]/@href").extract_first()  # 详细链接
            yield scrapy.Request("{}{}".format(MovieHeavenSpider.base_url, link), callback=self.parse_series_detail,dont_filter=True)

    def parse_series_detail(self, response):
        item = MovieItem()
        item["title"] = response.xpath("//div[@class='title_all']/h1/text()").extract_first()
        item["date"] = response.xpath("//div[@class='co_content8']//span[@class='updatetime']/text()").re("[0-9-]+")[0]
        # item["desc"] = response.xpath("//div[@id='Zoom']/p/text()").extract()
        item["downloadLink"] = response.xpath("//td[starts-with(@style,'WORD-WRAP')]//a/text()").extract()
        item["type"] = response.xpath("//div[@class='bd3l']/a[last()]/text()").extract_first()
        item["category"] = "series"
        item["detailLink"] = response.url
        yield item

