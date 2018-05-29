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


class MaiziPipeline(object):

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
            raise DropItem()

        course = item["course"]

        # course_video = item["course_video"]
        # course_url = item["course_url"]
        # course_name = item["course_name"]

        obj = self.client[spider.name].find_one({"title": title})
        if not obj:
            if not course:
                item["course"] = []
            else:
                item["course"] = []
                item["course"].append(course)
            self.client[spider.name].insert(dict(item))
        else:
            if course and course not in obj["course"]:
                obj["course"].append(course)
                self.client[spider.name].update({"title": title}, dict(obj), True)

        return item