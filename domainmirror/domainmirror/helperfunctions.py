"""
共用辅助类
"""

import codecs  # 解决文件写入时编码问题
from time import time
from os import makedirs
from os.path import basename, dirname, join, exists
from urllib.parse import urlparse, urljoin
from collections import defaultdict  # 用于构造树形结构数据
from tldextract import extract  # 解析域名的二级域名


class cTree:
    """
    自定义树节点，用于构造网站的目录结果
    """

    def __init__(self, _name, _children, _pages):
        self.name = _name
        self.children = _children
        self.pages = _pages


class Page:
    """
    页面抽象类
    用于存储页面相关信息
    """

    # 是否为首页
    isIndexPage = False
    # 站点域名
    domain = ""
    # 站点更目录
    rootPath = ""
    # 站点栏目信息
    categorys = {}
    # urls 为列表，记录当前页面所有有效的href
    urls = []
    # domainUrls 为当前站点所有的有效页面（url）
    domainUrls = []
    # domainUrlSeen 记录当前站点已处理的页面（url）
    domainUrlSeen = set()
    # 当前网站的所有的动态链接，以及每个动态链接对应的静态链接
    # 用于将动态链接静态化
    dynamic_urls = []
    # 要过滤的栏目名称（从数据库中获取）
    filter_cate = []
    # 栏目的模板页
    template_cat = ""
    # 内容页的模板
    template_page = ""

    def __init__(self, title, kw, desc, content=""):
        self.title = title  # seo title
        self.keywords = kw  # seo keywords
        self.description = desc  # seo description
        self.content = content


class Category:
    """
    栏目相关信息
    """

    def __init__(self, c_path, c_keywords, c_template, c_template_arc, c_name):
        self.name = c_name
        self.path = c_path
        self.keywords = c_keywords
        self.template = c_template
        self.template_arc = c_template_arc


def node_to_root(rootNode, curNode, deepNode, urlNode):
    """
    解析url递归添加到根节点
    :param rootNode:相对于下个节点的根节点
    :param deepNode:当前树的深度
    :param urlNode:当前url的深度
    """
    url_deep = len(urlNode)
    cur_node_deep = len(curNode.children)

    if deepNode < url_deep:
        is_exsit = False
        c_parent = cTree("", [], 0)  # 记录下次查找的根节点
        c_url_node = "/{}/".format(urlNode[deepNode].strip())
        for i in range(cur_node_deep):
            if curNode.children[i].name == c_url_node:
                is_exsit = True
                break
        if not is_exsit:
            c_parent.name = c_url_node
            # 页面不包含在目录中，但是逻辑继续（deepNode +=1）
            if "." not in c_url_node:
                curNode.children.append(c_parent)
            deepNode += 1
        node_to_root(rootNode, c_parent, deepNode, urlNode)


def append_sub_node(listCategory, url):
    """
    追加子节点到对应的父节点
    :param listCategory:为当前页面的所有栏目
    :param url:为但前页面所有的url
    """
    url_schema = urlparse(url)
    url_path = url_schema.path
    url_category = []

    if "/" in url_path:
        url_category = url_path.split("/")
    len_category = len(url_category)
    if len_category == 0 or len_category < 1:
        return False

    # 添加根节点到集合
    root_exsit = False
    url_start = join('/', url_category[1] + '/')
    root_node = cTree(url_start, [], 0)
    for n in listCategory:
        if n.name == root_node.name:
            root_node = n
            root_exsit = True
            break
    if not root_exsit:
        if "." not in root_node.name:
            listCategory.append(root_node)
        else:
            return False

    # 添加子节点到根节点
    # 添加子节点从网站根目录开始的第二个节点开始
    node_to_root(root_node, root_node, 2, url_category)


def url_root_path(url, page):
    """
    根据配置获取当前url的根目录
    :param url: 待确定根目录的url
    :param page: 当前页面的配置
    """
    dist_path = "/"  # 最终目录以根目录开始
    url_path = urlparse(url).path
    each_path = url_path.split('/')
    len_each_path = len(each_path)
    if len_each_path < 2:
        return ""
    # 每个链接的根目录默认为网站根目录的下一个目录
    for i in range(1, 2):
        dist_path += each_path[i] + "/"
    return dist_path


def save_file(page, url):
    """
    文件写入本地
    :param page: 当前页面对象
    :param url: 当前页面的url，用于分析页面保存的路径
    """
    url_schema = urlparse(url)
    # file_extends = [
    #     ".html", ".shtml", ".htm", ".php", ".jsp", ".php", ".asp", ".shtm",
    #     ".dhtml", ".xhtml"
    # ]

    file_path = page.rootPath + dirname(url_schema.path)

    # 文件路经不存在则创建
    if not exists(file_path):
        try:
            makedirs(file_path)
        except OSError as ex:
            print(u"路径创建失败 %s" % file_path + str(ex))

    try:
        file_name = basename(url_schema.path)
        if file_name.strip() == "":
            file_name = "index.html"
        file_full_name = join(file_path, file_name)

        with codecs.open(file_full_name, 'w+', 'utf-8') as file:
            file.write(page.content)

    except OSError as ex:
        print(u"文件写入失败 %s " % url_schema.path + str(ex))


def parse_html_url(response, page):
    """
    解析html中的url
    :param response: 蜘蛛爬行的结果
    :param page: 自定义数据临时存储类
    """
    htmls = response.text
    link_href_seen = set()
    link_src_seen = set()
    links_href = response.xpath("//@href").getall()
    links_src = response.xpath("//@src").getall()
    dynamic_urls = [".php", ".jsp", ".aspx", ".asp"]

    # 当前站点的所有资源路径改为绝对路径
    for src in links_src:
        url_schema = urlparse(src)
        if (url_schema.netloc == "" and src not in link_src_seen
                and url_schema.path != "/"):
            abs_src = urljoin(page.domain, str.strip(src))
            htmls = htmls.replace(src, abs_src)
            link_src_seen.add(src)

    # 过滤href供spider爬取
    for href in links_href:
        org_url = href  #记录原始的href
        url_schema = urlparse(href)

        # 排除一些无效链接
        if url_schema.netloc == "" and url_schema.path == "":
            continue
        # 替换当前页面中的相对路径为绝对路径
        if (url_schema.netloc == "" and href not in link_href_seen
                and url_schema.path != "/"):
            abs_href = urljoin(page.domain, href)
            htmls = htmls.replace(href, abs_href)
            url_schema = urlparse(abs_href)
            link_href_seen.add(href)
        # css链接,ico 文件不爬取
        if ".css" in href or ".ico" in href:
            continue
        # 排除首页
        if url_schema.path == "" or url_schema.path == "/":
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

        # 判断当前url是否为有效url
        if is_valid_url(page, href.strip()):
            page.urls.append(href.strip())

            # 替换测试域名(镜像域名)
            if page.domain in href:
                rep_href = href.replace(page.domain, "mirrort.com")
                htmls = htmls.replace(href, rep_href)

            # 检索首页中所有栏目和栏目名称（只检索顶级栏目）
            if page.isIndexPage:
                get_category_name(org_url, response, page)

    # 赋值处理后的html
    page.content = htmls
    # 修改首页标识（只有一个首页）
    page.isIndexPage = False


def is_valid_url(page, cur_url):
    """
    判断当前的url是否为有效的url
    :param page:首页page对象，记录当前网站蜘蛛爬行相关参数
    :param cur_url:待验证的url
    :return res_check:True为有效链接，反之False
    认为无效url的情况为：
    1：在当前目录下，页面总数已超过设定值
    2：非本站的url
    3：url的path为根目录的/
    4：已爬取过的不再爬取
    """

    res_check = True
    c_url_schema = urlparse(cur_url)
    c_url_domain = extract(cur_url).domain
    invalid_file_ext = [
        ".css", ".js", ".jpg", ".gif", ".png", ".bmp", ".psd", ".jpeg"
    ]

    # url的path为根目录/，判定无效链接
    if c_url_schema.path == "/":
        return False
    # 判断当前url的域名是否为本站域名
    if c_url_domain not in page.domain:
        return False
    # 文件扩展名过滤，资源文件不下载
    file_name = basename(c_url_schema.path).lower()
    if file_name in invalid_file_ext:
        return False
    # 爬取过的url不再爬取
    if cur_url in page.domainUrlSeen:
        return False
    return res_check


def get_category_name(url, res, page):
    """
    获取顶级栏目的名称
    :param url:待检索的url
    :param res:网页源码
    """
    url = url.strip()
    u_path = urlparse(url).path
    ary_path = u_path.split('/')
    if not ary_path:
        return None

    # 只检索顶级栏目（从根目录开始）
    l_path = len(ary_path)
    if l_path > 3:
        return None

    lnk_xpath = '//a[contains(@href,"{}")]'.format(url)
    ele_xpath = res.selector.xpath(lnk_xpath)
    if not ele_xpath:
        return None

    ele_text = ele_xpath[0].root.text

    if not ele_text:
        return None
    if ele_text.strip() == "":
        return None

    # 栏目名词存在过滤词的不处理
    for cn in page.filter_cate:
        if cn in ele_text:
            return None

    # 重复的栏目名不处理
    for cn in page.categorys:
        if ele_text.strip() == page.categorys[cn]:
            return None

    page.categorys[u_path] = ele_text.strip()
    return True


def get_spider_conf(page):
    """
    生存当前站点的采集规则
    :param page:当前站点的抽象
    """
    confs = []
    for c in page.categorys:
        confs.append(
            Category(c, "kw", page.template_cat, page.template_page,
                     page.categorys[c]))
    return confs

