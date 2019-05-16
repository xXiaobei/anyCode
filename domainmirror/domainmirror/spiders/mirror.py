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

    # 文件保存路径
    file_save_root = pro_setting['FILE_STORE']

    # 重写父类的函数,spider开始爬行执行此函数
    def start_requests(self):
        # 定义爬行的链接
        urls = ['http://zqrb.cn']
        for url in urls:
            page = Page("title_from_db", "kw_from_db", "desc_from_db")
            page.isIndexPage = True
            page.rootPath = "zqrb.cn"  # TODO:生产环境中从配置中导入

            request = Request(url, callback=self.parse)
            request.meta['page'] = page
            yield request

    def parse(self, response):
        """
        保存首页
        """
        url = response.url
        page = response.meta['page']
        parse_html_url(response, page)

        if page.isIndexPage:
            url = str.format("{}/index.html", url)

        # file_root_path = join(self.file_save_root, page.rootPath)
        # save_file(page.content, url, file_root_path)

        # for inner_page_url in page.urls:
        #     yield Request(inner_page_url, callback=self.parse_inner)

    def parse_inner(self, response):
        """
        保存内页
        """
        page_inner = Page('inner_title', 'inner_keywords',
                          'inner_description')  # TODO:生产环境中从配置导入
        page_inner.isIndexPage = False
        page_inner.rootPath = "zqrb.cn"  # TODO:生产环境中从配置中导入
        parse_html_url(response, page_inner)

        file_root_path = join(self.file_save_root, page_inner.rootPath)
        save_file(page_inner.content, response.url, file_root_path)

        for url in page_inner.urls:
            yield Request(url, callback=self.parse_inner)
