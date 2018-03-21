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

# import redis
#
# client = redis.Redis(host="localhost",port=6379,db=2)
# client.set("name","www")

# from selenium import webdriver
# import os
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
# dcap =dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
# dcap["phantomjs.page.settings.userAgent"] =("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
# driver = webdriver.PhantomJS(executable_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),*["tools","phantomjs-2.1.1-windows","bin","phantomjs.exe"]),desired_capabilities=dcap)
# driver.set_page_load_timeout(5)
#
# try:
#     driver.get(r"https://wh.fang.anjuke.com/loupan/all")
#     print driver.title
#     driver.save_screenshot("1.png")
#     print driver.page_source
#     driver.quit()
# except Exception,e:
#     print e.message


import requests

res = requests.get("http://wx3.sinaimg.cn/large/46401622gy1fphx28v8k2j20hs0hsjsk.jpg")

with open("aaa.jpg","wb") as f:
    f.write(res.content)