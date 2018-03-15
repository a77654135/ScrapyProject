# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     driverMiddleware
   Author :       talus
   date：          2018/3/15 0015
   Description :
-------------------------------------------------

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.http import Response,HtmlResponse

class DriverMiddleware(object):

    def __init__(self, crawler):
        self.crawler = crawler

        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
        driver = webdriver.PhantomJS(executable_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),*["tools", "phantomjs-2.1.1-windows", "bin", "phantomjs.exe"]),desired_capabilities=dcap)
        driver.set_page_load_timeout(10)
        self.driver = driver

    @classmethod
    def from_settings(cls, settings, crawler=None):
        return cls(crawler)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings, crawler)


    def close_spider(self, spider):
        self.driver.quit()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        # self.driver.save_screenshot(os.path.abspath("../images/2.png"))
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    # def process_response(self, request, response, spider):
    #     pass
    #
    # def process_exception(self, request, exception, spider):
    #     pass