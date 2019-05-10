# -*- coding: utf-8 -*-

from os.path import join
from scrapy import Request, Spider
from domainmirror.helperfunctions import parse_html_url, Page, save_file
from scrapy.utils.project import get_project_settings


class MirrorSpider(Spider):
    """
    框架蜘蛛定义
    """
    name = 'mirror'
    #allowed_domains = ['http://zmoney.com.cn'] # 蜘蛛爬取白名单
    # 如果是使用start_urls 则一定要配对 默认回调函数 parse
    # 否则 自己实现start_requests 开始 蜘蛛爬取
    start_urls = ['http://zmoney.com.cn/']

    # 读取配置文件
    pro_setting = get_project_settings()

    # 重写父类的函数,spider开始爬行执行此函数
    def start_requests(self):
        # 定义爬行的链接
        urls = ['http://zqrb.cn']
        for url in urls:
            page = Page("title_from_db", "kw_from_db", "desc_from_db")
            page.isIndexPage = True
            page.rootPath = "zqrb.cn"  # 生产环境中从配置中导入

            request = Request(url, callback=self.parse)
            request.meta['page'] = page
            yield request

    def parse(self, response):
        url = response.url
        page = response.meta['page']
        parse_html_url(response, page)

        if page.isIndexPage:
            url = str.format("{}/index.html", url)

        file_root_path = join(self.pro_setting['FILE_STORE'], page.rootPath)
        save_file(page.content, url, file_root_path)
