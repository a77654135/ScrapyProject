# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 15:41
# @Author  : Talus

import os
import threading
from multiprocessing import Queue
import sys
reload(sys)  # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import pymongo
import requests
import json

thread_list = []
queue = Queue()

def init():
    global thread_list
    for i in range(10):
        t = threading.Thread(target=threading_download)
        t.start()
        thread_list.append(t)


def end():
    global thread_list
    for t in thread_list:
        t.join()



def threading_download():
    global queue
    while not queue.empty():
        try:
            data = queue.get(block=True, timeout=1)
            download_item(data)
        except:
            break

def name_replace(name):
    strs = [":", "：", "-", "*", "/", r"\\", "?", "<", ">", "\""]
    for s in strs:
        name = name.replace(s, "")
    name = name.strip()
    return name

def download_item(item):
    name = item["course_name"]
    video = item["course_video"]
    category = item["category"]
    title = item["title"]
    detailUrl = item["detailUrl"]

    category = name_replace(category)
    title = name_replace(title)

    dir_parent1 = os.path.join(r"E:/maizi", category)
    dir_parent2 = os.path.join(r"G:/maizi", category)
    parent = dir_parent2 if os.path.exists(dir_parent2) else dir_parent1
    dir_name = os.path.join(parent, title)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    txt = os.path.join(dir_name, u"课程地址.txt")
    if not os.path.exists(txt):
        with open(txt, "w") as f:
            f.write(detailUrl)

    file_name = os.path.join(dir_name, "{}.mp4".format(name))
    if not os.path.exists(file_name):
        print u"开始下载：   {}".format(name)
        try:
            res = requests.get(video, timeout=10)
            if res.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(res.content)
                    print u"下载成功： {}".format(name)
            else:
                print u"下载失败： {}".format(name)
        except:
            print u"下载超时：  {}".format(name)


def download_maizi_category(category):

    global queue

    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db = client["scrapyData"]
    coll = db["maizi"]

    res = coll.find({"category": {"$regex": category, "$options": "i"}})
    # res = coll.find()

    for item in res:
        category = item.get("category", "")
        title = item.get("title", "")
        course_list = item.get("course", [])
        detailUrl = item.get("detailUrl", "")

        if not category:
            continue
        if not title:
            continue
        if not course_list or not len(course_list):
            continue

        for course in course_list:
            name = course.get("course_name", "")
            video = course.get("course_video", "")
            if not name or not video:
                continue

            data = {"category": category, "title": title, "course_name": name, "course_video": video, "detailUrl": detailUrl}
            print u"输入数据：   {}".format(json.dumps(data))
            queue.put(data, block=True, timeout=1)

def download_maizi_title(_title):

    global queue

    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db = client["scrapyData"]
    coll = db["maizi"]

    res = coll.find({"title": {"$regex": _title, "$options": "i"}})

    for item in res:
        category = item.get("category", "")
        title = item.get("title", "")
        course_list = item.get("course", [])
        detailUrl = item.get("detailUrl", "")

        if not category:
            continue
        if not title:
            continue
        if not course_list or not len(course_list):
            continue

        for course in course_list:
            name = course.get("course_name", "")
            video = course.get("course_video", "")
            if not name or not video:
                continue

            data = {"category": category, "title": title, "course_name": name, "course_video": video , "detailUrl": detailUrl}
            print u"输入数据：   {}".format(json.dumps(data))
            queue.put(data, block=True, timeout=1)

if __name__ == '__main__':
    download_maizi_category(u"android")
    # download_maizi_title(u"django")
    init()
    end()
