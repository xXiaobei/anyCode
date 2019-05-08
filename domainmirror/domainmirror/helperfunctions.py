"""
共用辅助类
"""


def get_urls(response):
    """
    检索当前html中所有的url
    :param response：蜘蛛爬行的结果
    :return： dict 
    """
    urls = {"links_src": [], "links_css": [], "links_href": []}
    if response:
        allHrefs = response.xpath("//@href").getall()
        urls["links_src"] = response.xpath("//@src").getall()
        for href in allHrefs:
            if ".css" in href:
                urls["links_css"].append(href)
            else:
                urls["links_href"].append(href)

    return urls


def urls_filter(_urls, _baseUrl):
    """
    过滤无效的链接,非本站链接
    :param _urls: list urls
    :return: list urls
    """
    invalid_urls, result_urls = [], []

    invalid_urls.append("javascript:;")
    invalid_urls.append("javascript:void(0);")
    invalid_urls.append("javascript:void(0)")
    invalid_urls.append("#")

    if 'http' in _baseUrl:
        _baseUrl = str.replace(_baseUrl, "http://", "")
    if "www." in _baseUrl:
        _baseUrl = str.replace(_baseUrl, "www.", "")

    for url in _urls:
        if str.strip(url) == "":
            continue

        # 排除非本站链接
        if _baseUrl not in url:
            continue

        # 排除无效链接
        if url not in invalid_urls:
            result_urls.append(url)

    return result_urls
