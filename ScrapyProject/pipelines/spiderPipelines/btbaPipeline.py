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


class BtbaPipeline(object):

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
        if not download_list:
            raise DropItem()

        if not item["name"]:
            raise DropItem()

        colname = "btbtdy"

        try:
            ret = self.client[colname].find_one({"name": item["name"]})
            if not ret:
                item["download_list"] = [download_list]
                self.client[colname].update({"name": item["name"]}, dict(item), True)
            else:
                dl = ret.get("download_list",[])
                has = False
                for d in dl:
                    if d["title"] == download_list["title"]:
                        has = True
                        break

                if has:
                    raise DropItem()
                else:
                    dl.append(download_list)
                    ret["download_list"] = dl
                    self.client[colname].update({"name": item["name"]}, ret, True)
        except Exception,e:
            print e.message
        finally:
            return item