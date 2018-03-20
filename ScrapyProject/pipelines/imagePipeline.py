# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     imagePipeline
   Author :       talus
   date：          2018/3/19 0019
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import requests


base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class ImagePipeline(object):
    def process_item(self, item, spider):
        try:
            img_url = item["img_url"]
            if img_url and img_url.startswith("http"):
                dir = os.path.join(base_dir,*["images",spider.name])
                if not os.path.exists(dir):
                    os.makedirs(dir)
                _,name = os.path.split(img_url)
                imgName = os.path.join(dir,name)

                res = requests.get(img_url)

                with open(imgName,"wb") as f:
                    f.write(res.content)
                    print "save image: " + img_url
        except:
            pass
        finally:
            return item