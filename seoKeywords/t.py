import re
from urllib.parse import urlparse, urljoin
from os.path import basename, dirname,join
from tldextract import extract

class Page:
    """
    页面抽象类
    用于存储页面相关信息
    """
    # category 为一个set访问器 记录当前网站所有栏目
    category = set()
    # 每个栏目的page总数
    category_pages = 0
    # urls 为列表，记录当前页面所有有效的href
    urls = []
    # 当前网站的所有的动态链接，以及每个动态链接对应的静态链接
    # 用于将动态链接静态化
    dynamic_urls = []

    def __init__(self, site_url, title, kw, desc, content=""):
        self.title = title
        self.keywords = kw
        self.description = desc
        self.content = content
        self.site_url = site_url

    @property
    def site_url(self):
        return self.site_url

    @site_url.setter
    def site_url(self, value):
        if "http" in value:
            value = value.replace("http://", "")
        if "www." in value:
            value = value.replace("www.", "")
        self.site_url = value


def test():
    t = r'<div id="rs"><div class="tt">相关搜索</div><table cellpadding="0"><tbody><tr><th><a href="/s?wd=%E7%94%9F%E8%82%96%E8%BF%90%E5%8A%BF&amp;rsf=1&amp;rsp=0&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">生肖运势</a></th><td></td><th><a href="/s?wd=%E6%9C%80%E5%87%86%E7%9A%8412%E7%94%9F%E8%82%96%E9%85%8D%E5%AF%B9%E8%A1%A8&amp;rsf=1&amp;rsp=1&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">最准的12生肖配对表</a></th><td></td><th><a href="/s?wd=%E7%94%9F%E8%82%96%E9%85%8D%E5%AF%B9&amp;rsf=1&amp;rsp=2&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">生肖配对</a></th></tr><tr><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E4%BF%9D%E6%8A%A4%E7%A5%9E&amp;rsf=8&amp;rsp=3&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖保护神</a></th><td></td><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E8%B4%A2%E8%BF%90%E6%96%B9%E4%BD%8D&amp;rsf=8&amp;rsp=4&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖财运方位</a></th><td></td><th><a href="/s?wd=%E7%94%9F%E8%82%96%E5%B9%B4%E4%BB%BD%E5%AF%B9%E7%85%A7%E8%A1%A8&amp;rsf=1&amp;rsp=5&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">生肖年份对照表</a></th></tr><tr><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E7%9B%B8%E5%86%B2%E7%9B%B8%E5%85%8B%E8%A1%A8&amp;rsf=1&amp;rsp=6&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖相冲相克表</a></th><td></td><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E5%A9%9A%E5%A7%BB%E9%85%8D%E5%AF%B9%E5%A4%A7%E5%85%A8&amp;rsf=1&amp;rsp=7&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖婚姻配对大全</a></th><td></td><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E5%AE%88%E6%8A%A4%E7%A5%9E&amp;rsf=8&amp;rsp=8&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖守护神</a></th></tr></tbody></table></div>'
    # a = re.compile('<a([\s\S]*?)>(.*?)<\/a>').search(t)
    a = re.findall('<a([\s\S].*?)>(.*?)<\/a>', t)
    for b in a:
        print(b[1])
    # print(a)


def testlist():
    return []


def testurl():
    url = "http://www.zmoney.com.cn/redian/guoneixinwen/index.html"
    url1 = "http://www.baidu.com.cn/xinwen/huanqiuxinwen/"
    schema_url = urlparse(url1)
    # print(extract("http://forums.news.cnn.com/").subdomain)
    # print(urljoin("http://www.zmoney.com", url1))
    # print(schema_url)
    # print(dirname(schema_url.path))
    # print(schema_url.netloc)
    # print(urlparse('/xinwem/index.html'))
    # print(basename('/xinwen/guonei/index.html'))
    # print(dirname('/xinwen/guonei/index.html'))
    print("http://www.baidu.com/list.php?id")
    print(basename("/xinwen/guonei/index.html"))
    print(urlparse("/xinwen/guonei/index.html"))
    print(join("/xinwen/guonei/","index.html"))


if __name__ == "__main__":
    testurl()
    # list_t = testlist()
    # for x in list_t:
    #     print(x)
    # file_content = ''
    # res_keywords = ['白姐正版四不像生肖', '2019年香港四不像正版', '白小姐四不像必中肖', '白姐i正版四不像生肖图', '白小姐四不像的图', '白小姐特马图四不像', '白姐正版四不像.中特图', '香港四不像必中一图', '管家婆正版四不像图', '白姐公开一码']
    # file_path = "/home/bbei/Documents/zhaoshengxiao.txt"
    # for kw in res_keywords:
    #     file_content += kw + "\n"
    # with open(file_path, 'w') as f:
    #     f.write(file_content)
    # print('关键词结果已经报错到文件 zhaoshengxiao.txt ')
