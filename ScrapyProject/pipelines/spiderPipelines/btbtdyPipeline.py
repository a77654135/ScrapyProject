# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     btbtdyPipeline
   Author :       talus
   date：          2018/3/29 0029
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
import re
from pymongo.errors import PyMongoError
from scrapy.exceptions import DropItem


class BtbtdyPipeline(object):

    def open_spider(self, spider):
        host = spider.settings.get("MONGODB_HOST","127.0.0.1")
        port = spider.settings.get("MONGODB_PORT",27017)
        database = spider.settings.get("MONGODB_DATABASE","scrapyData")

        self.conn = pymongo.MongoClient(host=host,port=port)
        self.client = self.conn[database]

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):

        download_list = item["download_list"]
        if not download_list or len(download_list) == 0:
            raise DropItem()

        if not item["name"]:
            raise DropItem()

        new_list = []
        for down_item in download_list:
            url = down_item["url"]
            if url:
                new_list.append(down_item)

        if len(new_list) == 0:
            raise DropItem()

        item["download_list"] = new_list

        desc = item["desc"]
        d_list = desc.split(" ")
        dlen = len(d_list)
        if dlen:
            if dlen > 0:
                item["year"] = re.findall(r"\d+",d_list[0])[0]
            if dlen > 1:
                item["country"] = d_list[1]
            if dlen > 2:
                item["type"] = d_list[2]

        try:
            self.client[spider.name].update({"name": item["name"]}, dict(item), True)
        except Exception,e:
            print e.message
        finally:
            return item