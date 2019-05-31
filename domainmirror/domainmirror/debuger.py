# encoding:utf-8
# scrapy 调试脚本


from scrapy.cmdline import execute
import sys, os

# 当前脚本路径
dirpath = os.path.dirname(os.path.abspath(__file__))
#切换到scrapy项目路径下
os.chdir(dirpath[:dirpath.rindex("/")])
# 启动爬虫,第三个参数为爬虫name
execute(['scrapy', 'crawl', 'mirror'])
