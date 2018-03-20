# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib
import os
from ScrapyProject.items.anjukeItem import AnjukeItem
from scrapy.http import Request


base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://wh.fang.anjuke.com/loupan/all/']

    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'ScrapyProject.middlewares.driverMiddleware.DriverMiddleware': 100,
    #     }
    # }

    def parse(self, response):
        """
        name = scrapy.Field()                       #名字
        detail_link = scrapy.Field()                #详情链接
        position = scrapy.Field()                   #地点
        home_type = scrapy.Field()                  #户型
        home_area = scrapy.Field()                  #建筑面积
        onsale = scrapy.Field()                     #售卖状态
        wuyetp = scrapy.Field()                     #地产类型
        tags = scrapy.Field()                       #标签
        price = scrapy.Field()                      #售价
        phone = scrapy.Field()                      #联系电话
        img_url = scrapy.Field()                    #图片地址
        img_local_url = scrapy.Field()              #图片本地地址
        :param response:
        :return:
        """

        mod_list = response.xpath(r"//div[@class='key-list']/div[@class='item-mod ']")

        for mod in mod_list:
            item = AnjukeItem()

            name = mod.xpath("div[@class='infos']/a[@class='lp-name']/h3/span/text()").extract_first()  # 名字
            detail_link = mod.xpath("a[@class='pic']/@href").extract_first()  # 详情链接
            position = mod.xpath("div[@class='infos']/a[@class='address']/span/text()").extract_first()   #.replace(r"&nbsp"," ")  # 地点
            home_area = mod.xpath("div[@class='infos']/a[@class='huxing']/span[last()]/text()").extract_first()  # 建筑面积
            onsale = mod.xpath("div[@class='infos']/a[@class='tags-wrap']/div[@class='tag-panel']/i[1]/text()").extract_first()  # 售卖状态
            wuyetp = mod.xpath("div[@class='infos']/a[@class='tags-wrap']/div[@class='tag-panel']/i[2]/text()").extract_first()  # 地产类型
            price = mod.xpath("a[@class='favor-pos']/p[@class='price']/span/text()").extract_first()  # 售价
            phone = mod.xpath("a[@class='favor-pos']/p[@class='tel']/text()").extract_first()  # 联系电话
            img_url = mod.xpath("a[@class='pic']/img/@src").extract_first()  # 图片地址

            item["name"] = name
            item["detail_link"] = detail_link
            item["position"] = position
            item["home_area"] = home_area
            item["onsale"] = onsale
            item["wuyetp"] = wuyetp
            item["price"] = price
            item["phone"] = phone
            item["img_url"] = img_url

            yield item

        next_link_href = response.xpath("//a[@class='next-page next-link']/@href").extract_first()
        if next_link_href is not None and next_link_href != "":
            yield Request(url=next_link_href,callback=self.parse)



