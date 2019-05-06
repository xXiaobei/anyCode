import re


def test():
    t = r'<div id="rs"><div class="tt">相关搜索</div><table cellpadding="0"><tbody><tr><th><a href="/s?wd=%E7%94%9F%E8%82%96%E8%BF%90%E5%8A%BF&amp;rsf=1&amp;rsp=0&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">生肖运势</a></th><td></td><th><a href="/s?wd=%E6%9C%80%E5%87%86%E7%9A%8412%E7%94%9F%E8%82%96%E9%85%8D%E5%AF%B9%E8%A1%A8&amp;rsf=1&amp;rsp=1&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">最准的12生肖配对表</a></th><td></td><th><a href="/s?wd=%E7%94%9F%E8%82%96%E9%85%8D%E5%AF%B9&amp;rsf=1&amp;rsp=2&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">生肖配对</a></th></tr><tr><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E4%BF%9D%E6%8A%A4%E7%A5%9E&amp;rsf=8&amp;rsp=3&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖保护神</a></th><td></td><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E8%B4%A2%E8%BF%90%E6%96%B9%E4%BD%8D&amp;rsf=8&amp;rsp=4&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖财运方位</a></th><td></td><th><a href="/s?wd=%E7%94%9F%E8%82%96%E5%B9%B4%E4%BB%BD%E5%AF%B9%E7%85%A7%E8%A1%A8&amp;rsf=1&amp;rsp=5&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">生肖年份对照表</a></th></tr><tr><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E7%9B%B8%E5%86%B2%E7%9B%B8%E5%85%8B%E8%A1%A8&amp;rsf=1&amp;rsp=6&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖相冲相克表</a></th><td></td><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E5%A9%9A%E5%A7%BB%E9%85%8D%E5%AF%B9%E5%A4%A7%E5%85%A8&amp;rsf=1&amp;rsp=7&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=0&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖婚姻配对大全</a></th><td></td><th><a href="/s?wd=%E5%8D%81%E4%BA%8C%E7%94%9F%E8%82%96%E5%AE%88%E6%8A%A4%E7%A5%9E&amp;rsf=8&amp;rsp=8&amp;f=1&amp;oq=%E7%94%9F%E8%82%96&amp;ie=utf-8&amp;usm=2&amp;rsv_idx=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg&amp;rqlang=cn&amp;rs_src=1&amp;rsv_pq=80eab4bc00136906&amp;rsv_t=8b42TE4XYur880ExvB9BPpQywjtMMNSKf%2FgIPPTLLwrCIhHxYKlZaYAiNVg">十二生肖守护神</a></th></tr></tbody></table></div>'
    # a = re.compile('<a([\s\S]*?)>(.*?)<\/a>').search(t)
    a = re.findall('<a([\s\S].*?)>(.*?)<\/a>', t)
    for b in a:
        print(b[1])
    # print(a)


def testlist():
    return []


if __name__ == "__main__":
    # list_t = testlist()
    # for x in list_t:
    #     print(x)
    file_content = ''
    res_keywords = ['白姐正版四不像生肖', '2019年香港四不像正版', '白小姐四不像必中肖', '白姐i正版四不像生肖图', '白小姐四不像的图', '白小姐特马图四不像', '白姐正版四不像.中特图', '香港四不像必中一图', '管家婆正版四不像图', '白姐公开一码']
    file_path = "/home/bbei/Documents/zhaoshengxiao.txt"
    for kw in res_keywords:
        file_content += kw + "\n"
    with open(file_path, 'w') as f:
        f.write(file_content)
    print('关键词结果已经报错到文件 zhaoshengxiao.txt ')

