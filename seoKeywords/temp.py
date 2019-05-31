
# 结果关键词过滤

def valid_keywords(k):
    is_valid = True
    filters = [
        '火腿', '双汇', '电影', '影片', '电视剧', '网盘', '李小峰', '紫微星', '片尾曲', '烟', '围棋',
        '店', '小吃', '点心', '加盟', '食品', '深圳','优级','彩票','喜剧','姑娘','音乐','dj',
        '伶人王','向前冲','牛肉','公司','简介','集团','家具','粉皮','木门','门窗','烧烤','豆皮','腻子粉',
        '粉漆','摩托车','铃木','抻面','拉面','搏击','茶','金锣','茉莉','广告','代理','一节','散打',
        '鼠','电信','龙江','炮竹','炮仗','鞭炮','榨菜','离合器','银杏','香肠','饮料','话梅','净水',
        '钙','小说','诗词'
    ]
    for f in filters:
        if k.find(f) >= 0:
            is_valid = False
            break
    return is_valid


if __name__ == "__main__":
    res = ""
    filename = "/home/bbei/Documents/baiduci/baiduci/王中王.txt"
    resname = '/home/bbei/Documents/baiduci/baiduci/res.txt'

    with open(filename, 'r') as f:
        for line in f:
            if valid_keywords(line):
                res += line

    with open(resname, 'w+') as fr:
        fr.write(res)
