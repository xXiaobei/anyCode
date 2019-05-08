# 公用辅助类

def urls_filter(_urls, _issrc, _baseUrl):
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

        # src链接不用排除无效链接
        if url not in invalid_urls and (not _issrc):
            result_urls.append(url)

    return result_urls
