# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jsonPipeline
   Author :       talus
   date：          2018/3/14 0014
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import os


class JSONPipeline(object):
    def process_item(self, item, spider):
        try:
            json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),*["data","json"])
            if not os.path.exists(json_dir):
                os.makedirs(json_dir)
            json_file = os.path.join(json_dir,"{}.json".format(spider.name))

            if not os.path.exists(json_file):
                content = []
            else:
                with open(json_file,"r") as f:
                    content = json.load(f)
            content.append(dict(item))

            with open(json_file,"w") as f:
                json.dump(content,f,indent=4,encoding="utf-8")
        except:
            pass
        finally:
            return item