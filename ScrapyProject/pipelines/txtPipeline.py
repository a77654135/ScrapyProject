# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     txtPipeline
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

class TxtPipeline(object):
    def process_item(self, item, spider):
        try:
            txt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),*["data","txt"])
            if not os.path.exists(txt_dir):
                os.makedirs(txt_dir)
            txt_file = os.path.join(txt_dir,"{}.txt".format(spider.name))

            with open(txt_file,"a") as f:
                f.write(json.dumps(dict(item)) + "\n")
        except:
            pass
        finally:
            return item


