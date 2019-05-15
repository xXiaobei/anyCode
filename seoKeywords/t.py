import re
from urllib.parse import urlparse, urljoin
from os.path import basename, dirname, join
from tldextract import extract
from aip import AipNlp


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
    print(join("/xinwen/guonei/", "index.html"))


def baiduapi():
    APP_ID = '16170203'
    APP_KEY = 'TQRGlbD2wk9RiG7B48GmHXhV'
    SECRET_KEY = 'LM5F0BGMCnyRyoiQvMPr6ygoyPmq3OqB'

    keywords = '明晚开什么生肖'
    result_words = [
        "明晚开什么生肖", "明晚开什么码白小姐", "李居明2016年生肖运程", "今晚特马买什么", "2019看图开特马",
        "查看今晚特马多少号", "今晚买四不像", "今晚什么特马生肖资料", "2019年六开彩今晚开奖", "2019年今晚开什么特马",
        "必中肖四不像获取完毕", "今晚开什么生肖", "今天晚上开什么生肖", "明晚必开生肖", "明晚开什么特生肖",
        "2019特马资料大全免费", "白姐今晚开码获取完毕", "今晚开什么码白小姐", "今晚已开特马开奖结果",
        "2019年买马最准的资料", "王中王开奖一马中特", "今晚六会彩开奖结查询", "381818白小姐一肖一码",
        "宋韶光2019年生肖运程", "2019年苏民峰生肖运势", "李居明2019年生肖运势", "董易奇2019年生肖运程",
        "2016年运程李居明", "2019十二生肖运程大全", "苏民峰2019年生肖运程", "李居明2019", "李居明32招改运法",
        "2019运程十二生肖运程", "李居明十二生肖运程", "2019年生肖运势", "2019运程李居明", "李居明2016年运程",
        "生肖运势可靠吗", "2019年运势李居明", "2019年香港四不像正版", "今天出什么特肖", "今天必中四不像图",
        "今日什么特马", "今晚特马多少号", "明天买什么特马", "今天出什么特马生肖", "2019期看图找生肖资料",
        "特马资料最准2019", "天下彩免费资料综大全", "2019年马会正版", "今晚特马号", "二肖二码长期免费公开",
        "2019今晚特马开多少号", "2019今日特马结果", "看2019今晚上开什么马", "今晚的特马开多少", "今晚肖必中",
        "2019年马会全年资料", "2019年四不像图", "今期四不像图", "白小姐特马图四不像", "2019年马会免费资料",
        "今晚必开什么特马", "今晚开什么生肖2019", "最准网站特马资料", "2019年六给彩开奖结果", "2019年今晚开奖结果",
        "2019年六开彩开奖结果", "2019六开彩公开资料", "今晚六开彩开奖开奖结果", "2019今晚六开彩开奖结果查询",
        "2019年开奖记录手机版", "2019今晚开什么特马l", "今晚特马开多少号", "2019今晚上开什么特马", "四不像图一肖中特",
        "发财一肖一码", "正版四不像一肖中特图", "香港四不像必中一图", "香港四不像期期期准", "香港马会四不像佖中一肖图",
        "四不像必中一生肖网址", "今天晚上开什么码", "2019今天晚上开什么码", "今天晚上买什么生肖!", "三期必开生肖",
        "明晚开什么特马一定中", "三期內必开", "今晚有什么生肖必开", "明天开什么生肖资料", "明晚开什么生肖单双", "今晚特马图",
        "明晚开什么生肖必开", "明晚开什么生肖几号", "明晚特马生肖", "今晚特碼开什么生肖", "明晚开什么生肖提示",
        "今晚出什么特尾", "今晚开什么特马生肖号", "明晚开什么生肖中特", "特是什么生肖", "二肖二码期期准100",
        "右手是什么生肖", "今天晚开什么生肖", "开马不开什么生肖", "明晚开什么生肖资料", "今晚会开什么生肖号码",
        "正版马会传真资料", "2019正版马会资料大全", "2019年正版免费全年资料", "2019全年免费资料大全",
        "2019全年免费料大全", "香港马会资枓大全2019", "2019年马会全年免费资料", "一码一肖100准", "白小姐今晚出",
        "三码必中", "一,肖一码´期期准", "白小姐图库统一免费", "今晚开什么码", "今晚开什么马", "今日特马结果开奖结",
        "2019今晚买什么码", "今天晚上开码资料", "2019年香港历史开奖记录版", "特马今晚开奖结果2019", "今天开什么特马",
        "2019年香港马开奖结果", "开奖直播现场手机开奖", "2019年王中王一肖中", "2019六会彩开奖结查询",
        "今晚六台彩开奖结果查询", "铁算盆王中王现场开奖结果", "今晚六会彩开奖特号码手机看开奖", "开码结果查询",
        "今期六台彩开奖结果查询2018", "381818乚白小姐中特开", "一期一码期码期期准", "二肖三码公开",
        "宋韶光2019年每月运程", "李居明2019年生肖运程", "宋韶光2019年猪年运程", "董易林2019年生肖运程",
        "宋韶光2019生肖运势", "徐墨斋2019年生肖运程", "宋韶光2019年生肖颜色", "宋韶光2019年流年运程",
        "宋韶光2019年日历", "宋韶光官网2019", "宋韶光2017年生肖每月运程", "2016运程十二生肖运程宋韶光",
        "宋韶光官网", "宋韶光每日通胜", "苏民峰2019运势生肖运势详解", "2019年属相运势苏民峰", "2019年生肖运程排名",
        "2019年风水布局苏民峰", "2019年各生肖财运排名", "苏民峰2019年属鼠运程", "苏民峰2019年生肖运程鼠",
        "苏民峰猪年运程", "2019运势排名", "熊神进2019年运势", "苏民峰2019年家居", "苏民峰2019属羊",
        "2019年风水苏民峰", "麦玲玲2019年生肖运程", "李居明2019年猪年运程", "李居明2020年运势大全",
        "麦玲玲2019", "2019年生肖运势相排名", "李居明2019运程", "李居明2019年龙人", "李居明2019属龙",
        "李居明2019财箱", "七星堂2019年生肖运程", "香港七星堂2019年运势", "董易奇2019生肖运势",
        "2019生肖蛇吉星", "董易奇一周生肖运程", "董易奇运程车", "董易奇每日生肖运势", "董易奇今日生肖运势",
        "董易奇八字排盘免费", "2019年68董易奇", "84属鼠2019运气", "1967年属羊的寿命预测", "2019李居明生肖运程",
        "12生肖2019运势完整版", "紫微2019运程", "2019年运程李居明", "李居明猴年运程", "2016年猴年运程",
        "2019十二生肖每月运程", "2019十二生肖每月运势", "2019年十二生肖运势", "2019年十二生肖运势详解",
        "2019生肖每月运势大全", "2019年各生肖运势排名", "十二生肖流年运程", "十二生肖属相运程", "2017年二生肖运程",
        "十二生肖19年运势", "2019年生肖运程", "苏民峰2019年催财布局", "香港苏民峰2019运程", "请苏民峰要多少钱",
        "苏民峰准不准", "苏民峰2019布局", "李居明2019九宫飞星图", "李居明2019年生肖运程视频", "李居明2019年运程书",
        "2019风水李居明视频", "李居明2019年运势视频", "李居明视频全集2019", "李居明教你摆财运", "李居明2019运势",
        "2019年李居明微博", "李居明改运", "李居明生肖改运", "很灵的转运小方法", "李居明属猪改运法", "李居明催桃花秘籍",
        "李居明属鼠食物改运法", "民间风水口诀准的吓人", "李居明发财密码", "李居明行好运吉利咒语", "李居明2017年运势",
        "李居明大师教你看面相", "李居明十大发达食物", "超厉害改运的几个方法", "李居明十大好运食物", "免费算命2019年运程",
        "2019生肖运势", "老农历2019生肖运程", "2019生肖运势运程", "十二生肖今日运势大全", "十二生肖运势2019",
        "十二生肖每月的运程", "十二生肖每个月运势", "香港李居明2019年运程", "李居明生肖运势", "李居明猪年运势",
        "2017李居明十二生肖运程", "李居明2017年运势12生肖运势", "生肖运势李居明", "李居明饿命学十二生肖",
        "李居明十二生肖流年运", "2019年生肖运势免费", "2019年运气最好的生肖", "2019年运程十二生肖运程",
        "2019年最顺的生肖", "2019最好的生肖", "2019年最好运生肖", "未来10年最旺的生肖", "宋韶光2019",
        "李居明2019年生肖每月运势", "2019年32岁属兔人运势", "李居明2015年运程", "猪年运程电影", "李居明2019通胜",
        "2019属牛运程李居明", "李居明马年运程", "2019属猴人全年运势女", "麦玲玲2016年运程", "李居明2019猴运程",
        "李居明2019年属虎", "生肖运势真的假的", "1985年牛女2019", "网上说的属相运势准吗", "生肖运势真的准确吗",
        "2019属猪几月出生最好", "65年蛇2019年的运势", "生肖运程能信吗", "今年什么生肖运势最好", "生肖运势真的准吗",
        "生肖运程准吗", "猪年最好的运势生肖", "属相运势真的可信吗", "生肖每年运程准吗", "生肖运程靠谱吗", "生肖运势可以相信吗",
        "2019年李居明生肖运程", "李居明2019年运程视频", "李丞责2019年运势", "李居明饿木命2019",
        "2019李居明生肖", "2019香港挂牌图正版", "2019年香港四不像资料", "今天码开什么特马", "今晚开什么特马",
        "今天晚上特马", "开奖特马料", "香港正牌四不像肖必中", "今日特马什么好", "2019今晚特马买什么",
        "今日什么特马开奖结果", "今晚开奖结果", "今天特马", "今天买什么特马", "明天晚上买什么特马包什么", "权威资料正版料大全",
        "正版四不像特肖图2019", "买马最准的资料2019", "最准的特马网站2019年", "246特彩天下彩免费资料",
        "天下彩票免费资料大全", "天下彩天空彩票免费资料大会", "天空彩天下彩票免费料i", "天下彩天空彩彩票资料大全",
        "香港曾道免费资料大全", "精准二肖二码网站", "神算子心水资料马资料", "2019三肖三马", "二肖大公开", "再公开3码",
        "一肖2码中", "2019今天特马开什么号", "今晚特马开多少号结果", "今晚特马多少号2019"
    ]

    client = AipNlp(APP_ID, APP_KEY, SECRET_KEY)

    for k in result_words:
        res = client.simnet(keywords, k)
        print(res)


if __name__ == "__main__":
    #baiduapi()
    #testurl()
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
    # t = u"\ue780第 10 页"
    # print(t.split(" "))
    # print(True)
    # print(10000 % 10000)
    print(u"{}.txt".format("测试中文字符"))
    t = ["a",'b','c']
    a = "\n".join(str(s) for s in t)
    print(a)
