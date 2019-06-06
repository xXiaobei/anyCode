# -*- coding: utf-8 -*-

from os.path import join
from scrapy import Request, Spider
from tldextract import extract
from scrapy.utils.project import get_project_settings
from domainmirror.mongohelper import *
from domainmirror.helperfunctions import parse_html_url, Page, save_file, get_spider_conf


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

    # 链接数据库mongoDB
    dbClient = mongoHelper()

    # 重写父类的函数,spider开始爬行执行此函数
    def start_requests(self):
        # 定义爬行的链接
        #urls = ['http://zqrb.cn', "https://www.z01.com"]
        #urls = ["https://www.z01.com"]
        urls = ["http://zqrb.cn"]
        for url in urls:
            page = Page("title_from_db", "kw_from_db", "desc_from_db")
            page.isIndexPage = True
            ext_domain = extract(url)  # 解析源网站域名
            page.domain = "{}.{}".format(ext_domain.domain, ext_domain.suffix)  # 记录当前蜘蛛爬取的主域名
            ext_domain = extract("http://www.ceshi.com")  # 解析待镜像的域名结构，待镜像的域名从配置中读取
            save_path = "{}.{}".format(ext_domain.domain, ext_domain.suffix)
            page.rootPath = join(self.file_save_root, save_path)  #镜像站点文件保存的目录

            request = Request(url, callback=self.parse)
            request.meta['page'] = page
            yield request

        # 释放数据库资源
        self.dbClient.db_close()

    def parse(self, response):
        """
        解析首页
        """
        url = response.url
        page = response.meta['page']
        url = str.format("{}/index.html", url)

        # 获取要过滤的栏目名称
        catNames = self.dbClient.icn_get_all()
        page.filter_cate = [cn["name"] for cn in catNames]
        # 获取栏目模板
        page.template_cat = self.dbClient.pt_by_type("list")
        # 获取内容页模板
        page.template_page = self.dbClient.pt_by_type("page")
        # 解析首页html
        parse_html_url(response, page)
        # 保存首页文件
        # save_file(page, url)
        # 爬取首页所有文件，并保存
        # for url in page.urls:
        #     request = Request(url, callback=self.parse_inner)
        #     request.meta['page'] = page
        #     yield request
        # 保存站点的采集规则  ???? 测试？？？？
        s_conf = get_spider_conf(page)
        # if s_conf:
        #     self.dbClient.insert_category(s_conf, page.domain)
        #  

    def parse_inner(self, response):
        """
        保存内页
        """
        page_index = response.meta['page']
        page_inner = Page('inner_title', 'inner_keywords',
                          'inner_description')  # TODO:生产环境中从配置导入
        page_inner.isIndexPage = False
        page_inner.domain = page_index.domain
        page_inner.rootPath = page_index.rootPath

        # 解析内页html
        parse_html_url(response, page_inner)

        # 保存内页html文件,并记录当前路径页面统计信息
        save_file(page_inner, response.url)
