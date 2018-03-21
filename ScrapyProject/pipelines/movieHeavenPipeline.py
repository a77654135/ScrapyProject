# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     movieHeaverPipeline
   Author :       talus
   date：          2018/3/21 0021
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import re
from scrapy.exceptions import DropItem
import pymongo


class MovieHeavenPipeline():

    def open_spider(self, spider):
        host = spider.settings.get("MONGODB_HOST","127.0.0.1")
        port = spider.settings.get("MONGODB_PORT",27017)
        database = spider.settings.get("MONGODB_DATABASE","scrapyData")

        self.conn = pymongo.MongoClient(host=host,port=port)
        self.client = self.conn[database]

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):

        title = item["title"]
        if not title:
            raise DropItem("not title found!")

        names = re.findall(ur".*《(.*)》.*", title)
        if len(names):
            item["name"] = names[0]
        try:
            # newDesc = []
            # for desc in item["desc"]:
            #     if not re.search("\xa0", desc):
            #         newDesc.append(desc)
            # item["desc"] = newDesc

            self.client[spider.name].insert(dict(item))
        except:
            pass
        finally:
            return item


