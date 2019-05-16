"""
共用辅助类
"""

import codecs  # 解决文件写入时编码问题
from time import time
from os import makedirs
from os.path import basename, dirname, join, exists
from urllib.parse import urlparse, urljoin
from tldextract import extract  # 解析域名的二级域名


class Page:
    """
    页面抽象类
    用于存储页面相关信息
    """

    # 是否为首页
    isIndexPage = False
    # 站点更目录
    rootPath = ""
    # category 为一个set访问器 记录当前网站所有栏目(以首页为基准)
    category = []
    # 每个栏目的page总数
    category_pages = 0
    # urls 为列表，记录当前页面所有有效的href
    urls = []
    # 当前网站的所有的动态链接，以及每个动态链接对应的静态链接
    # 用于将动态链接静态化
    dynamic_urls = []

    def __init__(self, title, kw, desc, content=""):
        self.title = title
        self.keywords = kw
        self.description = desc
        self.content = content


def save_file(content, url, fileroot):
    """
    文件写入本地
    :param content: 即将写入的内容
    :param url: 当前页面的url，用于分析页面保存的路径
    :param fileRoot: 当前爬虫项目文件保存路径
    """

    # TODO: 写文件时，将href中的源网站网址，替换为目标占的网址

    is_inner_page = False
    file_extends = [
        ".html", ".shtml", ".htm", ".php", ".jsp", ".php", ".asp", ".shtm",
        ".dhtml", ".xhtml"
    ]

    for extend in file_extends:
        if extend in url:
            is_inner_page = True
            break

    if not is_inner_page:
        if not str(url).endswith("/"):
            url = url + "/"  # 如果栏目的结尾不是/，加上/，避免urlparse后的path不准确

    url_schema = urlparse(url)
    file_path = fileroot + dirname(url_schema.path)

    # 文件路经不存在则创建
    if not exists(file_path):
        try:
            makedirs(file_path)
        except Exception as ex:
            print(u"路径创建失败 %s" % file_path + str(ex))

    try:
        file_name = join(file_path, basename(url_schema.path))
        with codecs.open(file_name, 'w+', 'utf-8') as file:
            file.write(content)
    except Exception as ex:
        print(u"文件写入失败 %s " % url_schema.path + str(ex))


def parse_html_url(response, page):
    """
    解析html中的url
    :param response: 蜘蛛爬行的结果
    :param page 自定义数据临时存储类
    """

    site_url = extract(response.url).domain  # 解析当前域名的主域名
    site_url_suf = extract(response.url).suffix  # 域名后缀
    links_href = response.xpath("//@href").getall()
    links_src = response.xpath("//@src").getall()
    dynamic_urls = [".php", ".jsp", ".aspx", ".asp"]
    index_links = [
        "http://www.{}.{}".format(site_url, site_url_suf),
        "http://www.{}.{}/".format(site_url, site_url_suf),
        "https://www.{}.{}".format(site_url, site_url_suf),
        "https://www.{}.{}/".format(site_url, site_url_suf)
    ]

    #TODO:TDK 处理逻辑

    # 当前站点的所有资源路径改为绝对路径
    for src in links_src:
        if site_url in src:
            url_schema = urlparse(src)
            if url_schema.path == "":
                abs_src = urljoin(response.url, str.strip(src))
                response.text = response.text.replace(src, abs_src)

    # 过滤href供spider爬取
    for href in links_href:
        url_schema = urlparse(href)

        if ".css" in href or ".ico" in href:  # css链接,ico 文件不爬取
            if url_schema.scheme == "":
                abs_css_href = urljoin(response.url, str.strip(href))
                response.text = response.text.replace(href, abs_css_href)
            continue
        if url_schema.path != "" and url_schema.scheme == "":  # 转为绝对路径
            href = urljoin(response.url, href)
            url_schema = urlparse(href)
        if str.strip(href) in index_links:  # 排除首页
            continue
        if url_schema.scheme not in ["http", "https"]:  # 排除一些无效链接
            continue
        if extract(href).subdomain != "www":  # www外的二级域名不爬取
            continue
        for ext in dynamic_urls:  # 转化动态链接为静态链接
            if ext in href:
                timespan = lambda: int(time * 1000)
                page.dynamic_urls.append({
                    "d_link":
                    href,
                    "s_link":
                    url_schema.path + str(timespan) + ".html"
                })

        # 如果当前页面是首页，则构建改网站的物理架构
        if page.isIndexPage:
            category_dict = {"cat_name": "", "cat_index": 0}
            if "/" in url_schema.path:
                cat_schema = url_schema.path.split("/")
                cat_deep_num = len(cat_schema)
                if cat_deep_num > 1:
                    category_dict["cat_name"] = cat_schema[1]
                    category_dict["cat_index"] = 1
                
                # 添加每个链接的根目录到集合
                if len(page.category) == 0:
                    page.category.append(category_dict)
                else:
                    for cat_dic in page.category:
                        if category_dict["cat_name"] not in cat_dic["cat_name"]:
                            page.category.append(category_dict)
                            break # 添加完后，退出循环，避免无效操作
                
                # 判断当前目录是否为最终目录
                if cat_deep_num > 3:
                    #目录的最小结构为3级（根目录、本身、页面）
                    #发现当前目录较已存在的目录的层次要深则替换调当前目录
                    #循环构造目录(用较长的路径替换当前路径中较短的路径，直至当前目录最终路径)
                    cur_deep_num = cat_deep_num - 1
                    cur_category = url_schema.path.substring(0, url_schema.path.rindex("/"))
                    for cd in category_dict:
                        if cd["cat_name"] in cur_category and cd["cat_index"] < cur_deep_num:
                            cd["cat_name"] = cur_category
                            cd["cat_index"] = int(cur_deep_num)

        page.urls.append(href)

        # page.category.add(dirname(url_schema.path))

    page.content = response.text
