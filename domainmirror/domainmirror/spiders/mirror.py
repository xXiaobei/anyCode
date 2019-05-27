# -*- coding: utf-8 -*-

from os.path import join, dirname
from urllib.parse import urlparse
from scrapy import Request, Spider
from scrapy.utils.project import get_project_settings
from domainmirror.helperfunctions import parse_html_url, Page, save_file, is_valid_url


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
        #urls = ['http://zqrb.cn', "https://www.z01.com"]
        urls = ["https://www.z01.com"]
        for url in urls:
            page = Page("title_from_db", "kw_from_db", "desc_from_db")
            page.domain = url
            page.isIndexPage = True

            s_path = url.replace("http://", "") # TODO:"zqrb.cn"生产环境中从配置中导入
            s_path = url.replace("https://www.", "") # TODO:"zqrb.cn"生产环境中从配置中导入

            page.rootPath = join(self.file_save_root, s_path)  # TODO:"zqrb.cn"生产环境中从配置中导入
            page.pageLimit = 5  # TODO:每个栏目的页面数从配置中导入
            page.pageDeep = 2  # TODO：蜘蛛爬行深度从配置中导入

            request = Request(url, callback=self.parse)
            request.meta['page'] = page
            yield request

    def parse(self, response):
        """
        解析首页
        """
        url = response.url
        page = response.meta['page']

        if page.isIndexPage:
            url = str.format("{}/index.html", url)

        # 解析首页html
        parse_html_url(response, page)

        # 保存首页文件
        save_file(page, url)

        # 获取首页所有链接
        # page.domainUrls.extend(page.urls)

        # # 以首页为起始，爬行整个网站
        # while page.domainUrls:
        #     inner_page_url = page.domainUrls.pop(0)
        #     request = Request(inner_page_url, callback=self.parse_inner)
        #     # request = Request(inner_page_url, callback=self.parse)
        #     request.meta['page'] = page
        #     # c_url_schema = urlparse(inner_page_url)
        #     # dir_name = dirname(page.rootPath + dirname(c_url_schema.path))
        #     # if dir_name in page.categoryPages:
        #     #     if page.categoryPages[dir_name] > page.pageLimit:
        #     #         continue
        #     #     # print(u"============================= {}: 页面数： {}".format(
        #     #     # dir_name, page.categoryPages[dir_name]))            
        #     yield request
        #     page.domainUrlSeen.add(inner_page_url)
        for url in page.urls:
            request = Request(url, callback=self.parse_inner)
            request.meta['page'] = page
            yield request

    def parse_inner(self, response):
        """
        保存内页，并获取内页的url到集合
        """
        page_index = response.meta['page']
        page_inner = Page('inner_title', 'inner_keywords',
                          'inner_description')  # TODO:生产环境中从配置导入
        page_inner.isIndexPage = False
        page_inner.domain = page_index.domain
        page_inner.pageDeep = page_index.pageDeep
        page_inner.pagePath = page_index.pagePath
        page_inner.rootPath = page_index.rootPath

        # 解析内页html
        parse_html_url(response, page_inner)

        # 保存内页html文件,并记录当前路径页面统计信息
        save_file(page_inner, response.url)

        # for inner_url in page_inner.urls:
        #     request = Request(inner_url, callback=self.parse_inner)
        #     request.meta['page'] = page_index
        #     yield request
        # 添加当前页面的url到队列中
        #page_index.domainUrls.extend(page_inner.urls)
