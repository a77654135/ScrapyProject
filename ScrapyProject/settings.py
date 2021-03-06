# -*- coding: utf-8 -*-

# Scrapy settings for ScrapyProject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import datetime

BOT_NAME = 'scrapybot'

SPIDER_MODULES = ['ScrapyProject.spiders']
NEWSPIDER_MODULE = 'ScrapyProject.spiders'

DEBUG = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36 QIHU 360SE'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36 QIHU 360SE',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ScrapyProject.middlewares.ScrapyprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ScrapyProject.middlewares.rotate_useragent.RotateUserAgentMiddleware': 100,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}



# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 30
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 24 * 60 * 60
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


TEST = False

if not TEST:
    # Configure a delay for requests for the same website (default: 0)
    # See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
    # See also autothrottle settings and docs
    DOWNLOAD_DELAY = 3

    # Configure item pipelines
    # See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
    ITEM_PIPELINES = {
        'ScrapyProject.pipelines.mongoPipeline.MongoPipeline': 300,
        'ScrapyProject.pipelines.csvPipeline.CSVPipeline': 400,
        # 'ScrapyProject.pipelines.jsonPipeline.JSONPipeline': 500,
        # 'ScrapyProject.pipelines.txtPipeline.TxtPipeline': 600,
    }

    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DATABASE = 'scrapyData'

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 6

    REDIS_DUPEFILTER_KEY = "dupefilter"
    REDIS_QUEUE_KEY = "queue"

    SCHEDULER = 'ScrapyProject.core.scheduler.Scheduler'
    DUPEFILTER_CLASS = 'ScrapyProject.core.dupefilter.RedisDupeFilter'
    SCHEDULER_QUEUE = 'ScrapyProject.core.queue.RedisStack'

    # dt = datetime.datetime.now()
    # LOG_FILE = '../logs/logging-{}_{}_{}_{}_{}_{}.txt'.format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
    # LOG_LEVEL = 'DEBUG'
