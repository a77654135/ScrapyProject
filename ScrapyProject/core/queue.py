# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     queue
   Author :       talus
   date：          2018/3/15 0015
   Description :
-------------------------------------------------

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import cPickle as pickle
except ImportError:
    import pickle

import redis
from scrapy.utils.reqser import request_to_dict,request_from_dict

class BaseQueue(object):
    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        host = settings.get('REDIS_HOST', "127.0.0.1")
        port = settings.get('REDIS_PORT', 6379)
        db = settings.get('REDIS_DB', 6)
        key = settings.get('REDIS_QUEUE_KEY', "queue")
        server = redis.Redis(host=host, port=port, db=db)
        server.ping()
        return cls(server, key)

    def open(self,spider):
        self.key = "{}:{}".format(spider.name, self.key)

    def close(self):
        self.server.bgsave()
        self.server.bgrewriteaof()

    def push(self, request, spider):
        pass

    def pop(self, spider):
        pass

    def clear(self):
        pass

    @property
    def length(self):
        return 0

class RedisQueue(BaseQueue):
    def push(self,request,spider):
        self.server.lpush(self.key,pickle.dumps(request_to_dict(request,spider)))

    def pop(self,spider):
        data = self.server.rpop(self.key)
        if data:
            return request_from_dict(pickle.loads(data),spider)

    def clear(self):
        self.server.delete(self.key)

    @property
    def length(self):
        return self.server.llen(self.key)


class RedisStack(BaseQueue):
    def push(self,request,spider):
        self.server.lpush(self.key,pickle.dumps(request_to_dict(request,spider)))

    def pop(self,spider):
        data = self.server.lpop(self.key)
        if data:
            return request_from_dict(pickle.loads(data),spider)

    def clear(self):
        self.server.delete(self.key)

    @property
    def length(self):
        return self.server.llen(self.key)