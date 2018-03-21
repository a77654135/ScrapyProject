# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     MongoPipeline
   Author :       talus
   date：          2018/3/14 0014
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
from pymongo.errors import PyMongoError


class MongoPipeline(object):

    def open_spider(self, spider):
        host = spider.settings.get("MONGODB_HOST","127.0.0.1")
        port = spider.settings.get("MONGODB_PORT",27017)
        database = spider.settings.get("MONGODB_DATABASE","scrapyData")

        self.conn = pymongo.MongoClient(host=host,port=port)
        self.client = self.conn[database]

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.client[spider.name].insert(dict(item))
            self.client[spider.name].update()
        except Exception,e:
            print e.message
        finally:
            return item