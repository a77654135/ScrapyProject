# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     dupefilter
   Author :       talus
   date：          2018/3/15 0015
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import logging

from scrapy.utils.job import job_dir
from scrapy.utils.request import request_fingerprint
import redis

class RedisDupeFilter(object):
    def __init__(self, client=None, key=None, debug=False):
        self.logdupes = True
        self.debug = debug
        self.client = client
        self.key = key
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get("REDIS_HOST","127.0.0.1")
        port = crawler.settings.get("REDIS_PORT",6379)
        db = crawler.settings.get("REDIS_DB",6)
        debug = crawler.settings.get("DEBUG",False)
        key = crawler.settings.get("REDIS_DUPEFILTER_KEY","dupefilter")

        client = redis.Redis(host=host, port=port, db=db)
        client.ping()
        return cls(client=client, key=key, debug=debug)

    def open(self,spider):
        self.key = "{}:{}".format(spider.name, self.key)

    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if self.client.sismember(self.key, fp):
            return True
        self.client.sadd(self.key, fp)
        return False

    def close(self, reason):  # can return a deferred
        # self.client.bgsave()
        # self.client.bgrewriteaof()
        pass


    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)

