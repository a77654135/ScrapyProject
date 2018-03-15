# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ScrapyProject.items.jokeItem import JokeItem


class JokeSpider(scrapy.Spider):
    name = 'joke'
    allowed_domains = ['jokeji.cn']
    start_urls = ['http://www.jokeji.cn/list.htm']

    def parse(self, response):
        li_list = response.xpath("//div[@class='list_title']//li")
        for li in li_list:
            item = JokeItem()
            title = li.xpath("b/a/text()").extract_first()
            view_count = li.xpath("span/text()").re("[0-9]+")[0]
            time = li.xpath("i/text()").extract_first()
            item["title"] = title
            item["view_count"] = view_count
            item["time"] = time
            yield item
