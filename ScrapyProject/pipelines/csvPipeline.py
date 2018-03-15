# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     csvPipeline
   Author :       talus
   date：          2018/3/14 0014
   Description :
-------------------------------------------------

"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os


class CSVPipeline(object):
    def process_item(self, item, spider):
        try:
            obj = dict(item)
            key_list = sorted(obj)
            csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),*["data","csv"])
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)
            csv_file = os.path.join(csv_dir,"{}.csv".format(spider.name))

            if not os.path.exists(csv_file):
                with open(csv_file,"a") as f:
                    line = ""
                    for idx,key in enumerate(key_list):
                        if idx < len(key_list) - 1:
                            line += r'"{}",'.format(key)
                        else:
                            line += r'"{}"'.format(key)
                    line += "\n"
                    f.write(line)

            with open(csv_file, "a") as f:
                line = ""
                for idx, key in enumerate(key_list):
                    if idx < len(key_list) - 1:
                        line += r'"{}",'.format(obj[key])
                    else:
                        line += r'"{}"'.format(obj[key])
                line += "\n"
                f.write(line)
        except:
            pass
        finally:
            return item