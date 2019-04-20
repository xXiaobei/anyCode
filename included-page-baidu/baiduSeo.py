import os
import requests
import time
import datetime
from random import randint
from lxml import etree

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "X-Forwarded-For": '%s:%s:%s:%s' % (randint(1, 255),
                                        randint(1, 255), randint(1, 255), randint(1, 255)),
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"}


def check_index_number(url):
    """
    查询网址被百度收录的数量
    :param url: 要查询的网址
    :return: 返回被百度收录的数量
    """
    url_a = 'https://www.baidu.com/s?wd=site%3A'
    url_b = '&pn=1&oq=site%3A52pojie.cn&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=dd6157d100015d1f&rsv_t=9a3eHncH3YeAeoblNqMm1f3%2FAQsJeSgF03XLXg6VDz6VqSprqUL8lGGO3us'
    joinUrl = url_a + url + url_b
    # print joinUrl   #拼接URL
    html_Doc = requests.get(joinUrl, headers=HEADERS)
    response = etree.HTML(html_Doc.content)
    try:
        index_number = response.xpath('//*[@id="1"]/div/div[1]/div/p[3]/span/b/text()')[0]
    except:
        top_htmls = response.xpath('//*[@id="content_left"]/div/div/p[1]/b/text()')[0]
        try:
            index_number = int(top_htmls.replace('找到相关结果数约','').replace('个',''))
        except:
            index_number = 0
        pass
    return index_number


def getUrl(filepath):
    with open(filepath, "r") as f:
        f = f.readlines()
    return f


def getHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def isindex(link, c_index, c_counter):
    #url = link.replace("http://", "").replace("/", "%2F")
    url = "http://www.baidu.com/s?wd=" + link
    html = getHtml(url)

    if "很抱歉，没有找到与" in html or "没有找到该URL" in html:
        print(u"{}/{}------------------- 未收录 {} ".format(str(c_index), str(c_counter), link))
    else:
        print(u"{}/{}------------------- 收 录 {} ".format(str(c_index), str(c_counter), link))
        indexed_number = check_index_number(link)
        c_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return u"{}\t included counter:{}\t{}".format(c_time, indexed_number, link)
    return ""


def main():
    total_counter = 0
    included_counter = 0
    list_files = os.listdir('yuming')

    if list_files:
        for domain_file in list_files:
            included_info = ""  # 当前文档的域名收录情况

            urls = getUrl("yuming/%s" % domain_file)

            c_index = 1
            c_counter = len(urls)
            total_counter += c_counter  # 总域名数

            for url in urls:
                #secends = 1  # randint(1, 3)  # 线程随机停顿S 停顿1到3s很慢 1000个域名要30min
                url = url.strip()
                try:
                    info = isindex(url, c_index, c_counter)
                    if info != "":
                        included_counter += 1
                        included_info += info + '\n'
                except:
                    pass
                c_index += 1
                #time.sleep(0.5)

            # 写入当前txt所包含的域名被收录的情况到新文件
            file_name = "{}.shoulu.txt".format(
                os.path.splitext(domain_file)[0])
            with open("yuming/%s" % file_name, 'w') as f:
                f.write(included_info)

            # 查询下一批域名时，线程停顿5s
            time.sleep(5)

        # 所有域名查询完毕 汇总统计结果，写入文件
        included_percent = "{}%".format((included_counter/total_counter)*100)
        with open('jieguo.txt', 'a') as f:
            c_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            res_info = "{}\t total:{} \t included:{} \t percent:{}".format(
                c_time, str(total_counter), str(included_counter), included_percent)
            f.write(res_info)


if __name__ == '__main__':
    main()
    # headers = {
    #     "Accept":"text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
    #     "Accept-Encoding":"gzip, deflate",
    #     "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    #     "Connection":"keep-alive",
    #     "Host":"api.66mz8.com",
    #     "TE":"Trailers",
    #     "Upgrade-Insecure-Requests":"1",
    #     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    # }
    # html = requests.get('https://api.66mz8.com/api/baidu.php?url=yishannian.tw',headers=headers,verify=False)
    # print(html)
