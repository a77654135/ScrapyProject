# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ttt
   Author :       talus
   date：          2018/3/14 0014
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


import pymongo


# with open("ttt.csv","w") as f:
#     f.write("id,name,age\n")
#     f.write("11,aa,12\n")

obj = {
    "id":1,
    "name":"wc",
    "age":12
}


# for k,v in obj.iteritems():
#     print k,v
#
# # print sorted(obj)
# for i,j in enumerate(sorted(obj)):
#     print i,j

import redis

client = redis.Redis(host="localhost",port=6379,db=2)
client.set("name","www")