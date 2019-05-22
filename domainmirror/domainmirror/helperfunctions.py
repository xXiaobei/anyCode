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
    # 站点更目录
    rootPath = ""
    # 站点页面目录 以及该目录对应的页面总数
    pagePath = {}
    # category 为一个set访问器 记录当前网站所有栏目(以首页为基准)
    # 该逻辑暂停，写文件时这个逻辑已经体现
    category = []
    # urls 为列表，记录当前页面所有有效的href
    urls = []
    # 当前网站的所有的动态链接，以及每个动态链接对应的静态链接
    # 用于将动态链接静态化
    dynamic_urls = []
    # 每个栏目页面数目限制
    pageLimit = 0
    # 蜘蛛爬行深度，建议为2(从根目录开始,根目录为1)
    # 爬行深度超过2，总页面算法为 pageLimit的(n-1)次方,n为蜘蛛爬行深度
    pageDeep = 0
    # 站点域名
    domain = ""

    def __init__(self, title, kw, desc, content=""):
        self.title = title
        self.keywords = kw
        self.description = desc
        self.content = content


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


def save_file(page, url):
    """
    文件写入本地
    :param page: 当前页面对象
    :param url: 当前页面的url，用于分析页面保存的路径
    """

    is_inner_page = False
    url_schema = urlparse(url)
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

    file_path = page.rootPath + dirname(url_schema.path)

    # 文件路经不存在则创建
    if not exists(file_path):
        try:
            makedirs(file_path)
        except OSError as ex:
            print(u"路径创建失败 %s" % file_path + str(ex))

    # 但前url
    page_counter = 0
    url_path = url_root_path(url, page)
    # 路径存在则直接赋值记数
    if url_path in page.pagePath:
        page_counter = int(page.pagePath[url_path])

    try:
        file_name = basename(url_schema.path)
        if file_name.strip() == "":
            file_name = "index.html"
        file_full_name = join(file_path, file_name)
        with codecs.open(file_full_name, 'w+', 'utf-8') as file:
            file.write(page.content)
            page_counter += 1  # 文件写入成功，当前路径（url）页面记数+1
    except OSError as ex:
        print(u"文件写入失败 %s " % url_schema.path + str(ex))

    # 更新当前路径（url）的页面记数
    page.pagePath[url_path] = page_counter


def parse_html_url(response, page):
    """
    解析html中的url
    :param response: 蜘蛛爬行的结果
    :param page 自定义数据临时存储类
    """
    htmls = response.text
    links_href = response.xpath("//@href").getall()
    links_src = response.xpath("//@src").getall()
    dynamic_urls = [".php", ".jsp", ".aspx", ".asp"]

    #TODO:TDK 处理逻辑

    # 当前站点的所有资源路径改为绝对路径
    for src in links_src:
        url_schema = urlparse(src)
        if url_schema.netloc == "":
            abs_src = urljoin(page.domain, str.strip(src))
            htmls = htmls.replace(src, abs_src)

    # 过滤href供spider爬取
    for href in links_href:
        url_schema = urlparse(href)

        # 排除一些无效链接
        if url_schema.netloc == "" and url_schema.path == "":
            continue
        # 替换当前页面中的相对路径为绝对路径
        if url_schema.netloc == "":
            if not href.startswith("/"):
                abs_href = urljoin(page.domain, "/" + href)
                htmls = htmls.replace(href, abs_href)
                url_schema = urlparse(abs_href)
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

        # 如果当前页面是首页，则构建改网站的物理架构
        # if page.isIndexPage:
        #     append_sub_node(page.category, href)

        # 当前页面如果为首页，则检索出所有的栏目页（栏目的深度为配置的蜘蛛爬行深度）
        if page.isIndexPage:
            cat_path = url_root_path(href, page)
            if cat_path != "":
                page.pagePath[cat_path] = 0 # 每个栏目默认的页面记数为0

        # 判断当前url是否为有效url
        if is_valid_url(href.strip(), page):
            page.urls.append(href.strip())

    page.content = htmls


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
    4：url的所在的栏目总页面数超过设定值的
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
    # 当前url所在的栏目的页面数判断
    each_path = c_url_schema.path.split("/")
    len_each_path = len(each_path)
    if len_each_path > 2:
        r_path = url_root_path(cur_url, page)
        if r_path in page.pagePath:
            if page.pagePath[r_path] > page.pageLimit:
                return False

    return res_check

def url_root_path(url, page):
    """
    根据配置获取当前url的根目录
    :param url: 待确定根目录的url
    :param page: 当前页面的配置
    """
    dist_path = "/" # 最终目录以根目录开始
    each_path = url.split('/')
    len_each_path = len(each_path)
    if len_each_path < 2:
        return ""
    for i in range(1, page.pageDeep):
        dist_path += each_path[i] + "/"
    return dist_path
