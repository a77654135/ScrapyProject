# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     scheduler
   Author :       talus
   date：          2018/3/14 0014
   Description :
-------------------------------------------------

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import json
import logging

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)

class Scheduler(object):

    def __init__(self, dupefilter, queue=None, stats=None):
        self.df = dupefilter
        self.queue = queue
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_crawler(crawler)
        queue_cls = load_object(settings['SCHEDULER_QUEUE'])
        queue = queue_cls.from_crawler(crawler)

        return cls(dupefilter, queue=queue, stats=crawler.stats)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self.spider = spider
        self.queue.open(spider)
        return self.df.open(spider)

    def close(self, reason):
        self.queue.close()
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        self.queue.push(request, self.spider)
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        return True

    def next_request(self):
        request = self.queue.pop(self.spider)
        if request:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request

    def __len__(self):
        return self.queue.length

