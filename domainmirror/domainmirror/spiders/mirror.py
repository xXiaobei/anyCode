# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from domainmirror.domainmirror.items import UlrItem, PageItem
from domainmirror.domainmirror.helperfunctions import *


class MirrorSpider(scrapy.Spider):
    name = 'mirror'
    allowed_domains = ['http://zmoney.com.cn']
    # 如果是使用start_urls 则一定要配对 默认回调函数 parse
    # 否则 自己实现start_requests 开始 蜘蛛爬取
    start_urls = ['http://zmoney.com.cn/']

    # 重写父类的函数,spider开始爬行执行此函数
    def start_requests(self):
        # 定义爬行的链接
        urls = ['http://zmoney.com.cn']
        for url in urls:
            # 针对url的爬行结果交给回调函数parse 处理
            yield Request(url, callback=self.parse)

    def parse(self, response):
        links_src = urls_filter(response.xpath("//@src"))
        links_href = urls_filter(response.xpath("//@href"))
        print(links_href)
        print(links_src)
