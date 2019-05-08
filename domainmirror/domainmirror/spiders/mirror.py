# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request,Spider
from domainmirror.items import UrlItem, PageItem
from domainmirror.helperfunctions import *


class MirrorSpider(Spider):
    """
    框架蜘蛛定义
    """
    name = 'mirror'
    main_url = ""
    #allowed_domains = ['http://zmoney.com.cn'] # 蜘蛛爬取白名单
    # 如果是使用start_urls 则一定要配对 默认回调函数 parse
    # 否则 自己实现start_requests 开始 蜘蛛爬取
    start_urls = ['http://zmoney.com.cn/']

    # 重写父类的函数,spider开始爬行执行此函数
    def start_requests(self):
        # 定义爬行的链接
        urls = ['http://zmoney.com.cn']
        for url in urls:
            self.main_url = url
            # 针对url的爬行结果交给回调函数parse 处理clear
            yield Request(url, callback=self.parse)

    def parse(self, response):
        urls = get_urls(response)  # 获取当前页面所有的链接
        urls["links_href"] = urls_filter(urls["links_href"], self.main_url)  # 过滤无效链接

        # item = UrlItem()
        # for url in urls["links_src"] + urls["links_css"]:
        # yield Request(url, callback=self.test)
        # item["file_urls"] = [url]
        # item["file_urls"] = "http://www.zmoney.com.cn/file/script/js/jquery-1.9.1.min.js"
        # yield item

        url_item = UrlItem()
        # 下载src,css资源文件
        #url_item['file_urls'] = urls["links_src"] + urls["links_css"]
        url_item['file_urls'] = ['http://www.zmoney.com.cn/lang/zh-cn/lang.js']

        yield url_item  # 将实例化的item传入管道
