#encoding:utf-8

"""
#百度m端挖词工具
#无效关键词判断标准：
# 1：没有搜索结果
# 2：搜索结果没有10页，且第一页搜索结果没有包含5条关键词收录
"""

import os, sys
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlitehelper import dbHelper


class MobileKeywords:
    """
    百度手机端关键词挖掘
    """

    def __init__(self, tag_url, tag_kw, wait_seconds, f_kw, i_kw):
        """
        初始化
        :param tag_url:需要加载的网页地址
        :param wait_seconds:显示等待时间，默认为10S
        """
        self.url = tag_url
        self.seconds = wait_seconds
        self.keywords = tag_kw
        self.dbHelper = None  # 数据库辅助类
        self.retry_counter = 1  # 失败重试次数
        self.title_counter = 5  # 关键词在搜索结果中出现的次数
        self.page_keywords = 0  # 关键词搜索结果总页
        self.total_keywords = 0  # 总关键词记数
        self.file_save_path = ""  # 关键词文件保存路径
        self.filter_keywords = f_kw  # 过滤的关键词（关键词不得出现该列表中的任何词）
        self.include_keywords = i_kw  # 包含关键词（关键词中必须包含该列表中的任何一个词）
        self.res_keywords = {"valid": False, "sub_keywords": []}
        self.browser = webdriver.Chrome(chrome_options=self.init_driver())
        self.wait = WebDriverWait(self.browser, wait_seconds)

    def init_save_info(self):
        """
        初始化关键词保存相关
        """
        try:
            file_path = '/home/documents/seobaidu/baiduci/'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_name = os.path.join(file_path,
                                     u"{}.txt".format(self.keywords))
            self.file_save_path = file_name
            print(u"-----------------------------------------------------")
            print(u"==关键词保存路径为：{}".format(self.file_save_path))
            print(u"-----------------------------------------------------")
        except:
            print(u"===关键词结果保存文件创建出错，请重试...")
            os._exit(0)

    def init_driver(self):
        """
        webdriver 配置项
        """
        opt = ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }  # 禁止加载图片
        opt.add_experimental_option("prefs", prefs)
        opt.add_argument("blink-settings=imagesEnabled=false")  # 禁止加载图片
        opt.add_argument('--headless')  # 无界面模式
        opt.add_argument('--disable-gpu')  # 禁止使用硬件加速
        opt.add_argument('--no-sandbox')  # 针对selenium在centos7 server中的配置
        opt.add_argument(
            '--disable-dev-shm-usage')  # 针对selenium在centos7 server中的配置
        opt.add_argument(
            "user-agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'"
        )  # 自定义请求头
        return opt

    def status_rest(self):
        """
        状态初始化，为下一个关键词准备
        """
        self.title_counter = 5
        self.page_keywords = 0
        self.retry_counter = 1
        self.res_keywords = {"valid": False, "sub_keywords": []}

    def restart_driver(self):
        """
        当超时发生后，清理当前游览器，重新赋值
        """
        try:
            self.wait = None
            self.browser.quit()
            self.browser = webdriver.Chrome(self.init_driver())
            self.wait = WebDriverWait(self.browser, self.seconds)
        except:
            print(u"===webdriver重启出错，即将重试...")
            self.restart_driver()

    def request_url(self, req_url, tipMsg):
        """
        请求给定的网站，超时进行默认次数的重试，成功则返回页面，反之返回None
        """
        try:
            self.browser.get(req_url)
            return True
        except TimeoutException as ex:
            if self.retry_counter <= 1:
                self.browser.quit() # 清空driver所占有的所有资源
                self.restart_driver() # 重启driver 在一个异常中不能引发另外一个异常
                print(u"=== {}，正在尝试重试第 {} 次...".format(tipMsg, self.retry_counter))
                self.retry_counter += 1
                self.request_url(req_url, tipMsg)
            else:
                self.retry_counter = 1
                return None

    def write_file(self, kw_data):
        """
        将关键词写入文件
        """
        with open(self.file_save_path, 'a+') as f:
            s = "\n".join(s for s in kw_data)
            f.write(s)
        kw_data.clear()  # 清空，为下次准备

    def ele_waiting(self, selector, selector_type, wait_type, retry):
        """
        等待页面元素加载完成
        :param selector: 页面元素的选择器
        :param selector_type: 页面元素选择器的种类
        :wait_type: 等待类型，是否出现？可以点击？...
        :retry: 等待超时，是否需要重试
        找到则返回当前元素，反之为None
        """
        cur_wait_type = EC.presence_of_element_located
        if wait_type == 'click':
            cur_wait_type = EC.element_to_be_clickable
        try:
            if selector_type == "css":
                ele = self.wait.until(
                    cur_wait_type((By.CSS_SELECTOR, selector)))
            if selector_type == "xpath":
                ele = self.wait.until(cur_wait_type((By.XPATH, selector)))
            return ele
        except TimeoutException as ex:
            print(u"Elements can't loaded {}" + str(ex))
            if retry and self.retry_counter <= 1:  # 默认重试1次，超过重试次数则直接返回结果
                self.retry_counter += 1
                self.is_valid_keywords()
            else:
                return None

    def ele_exist(self, selector, selector_type, is_single):
        """
        判断页面上某个元素是否存在
        :param selector: 元素选择器
        :selector_type: 选择其种类
        :is_single: 是否为单个元素
        存在则返回当前元素，反之为None
        """
        ele = None
        cur_selector_type = By.CSS_SELECTOR
        if selector_type == "xpath":
            cur_selector_type = By.XPATH

        try:
            if is_single:
                ele = self.browser.find_element(cur_selector_type, selector)
            else:
                ele = self.browser.find_elements(cur_selector_type, selector)
        except:
            return ele
        return ele

    def is_valid_keywords(self):
        """
        判断当前关键词是否为有效关键词
        :param kw:等待检查的关键词
        返回当前关键词有效标识；返回当前关键字所有相关词
        """
        # 抓取目标网址
        tip_msg = "打开百度首页超时"
        if self.request_url(self.url, tip_msg) is None:
            print(u'=== %s 打开百度首页超时，继续下一个关键词!' % self.keywords)
            return self.res_keywords

        # 等待搜索框和搜索按钮加载完成
        try:
            txt_search = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#index-kw")))
            btn_search = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#index-bn")))
            # 发送关键词，等待搜索结果
            txt_search.send_keys(self.keywords)
            #btn_search.click()
            #直接执行click无效，使用js脚本执行click
            self.browser.execute_script("arguments[0].click();", btn_search)
        except:
            print(u"=== 页面元素拉取超时，放弃 %s，继续下一个！" % self.keywords)
            self.restart_driver() # 元素发生超时后，重启driver
            return self.res_keywords

        # 判断搜索结果是否为空
        page_result = self.ele_exist(".se-noresult-tips", "css", True)
        if page_result is not None:
            return self.res_keywords

        # 相关搜索词
        str_xpath = ".//a"
        kw_relations = self.ele_exist(".rw-list", "css", True)
        if kw_relations is not None:
            links = kw_relations.find_elements_by_xpath(str_xpath)
            for lnk in links:
                self.res_keywords['sub_keywords'].append(lnk.text)

        # 判断关键词在首页出现次数
        str_xpath = "/html/body/div[3]/div[2]/div[2]/div"
        res_search = self.ele_exist(str_xpath, "xpath", False)
        if res_search is not None:
            for title in res_search:
                if u"其他人还在搜" in title.text:  # 其他人还在搜 相关词
                    kw_others = title.text.replace("其他人还在搜", "").split("\n")
                    for v in kw_others:
                        self.res_keywords['sub_keywords'].append(v.strip())
                    continue
                if u"相关搜索" in title.text:
                    continue
                if self.keywords in title.text and self.title_counter > 0:
                    self.title_counter -= 1

        # 判断当前关键词搜索结果总页数是否大于10页
        str_xpath = "/html/body/div[3]/div[2]/div[4]/div/a"
        paging_url = self.ele_exist(str_xpath, "xpath", True)
        if paging_url is not None:
            paging_url = paging_url.get_attribute("href").replace("pn=10", "pn=90")
            tip_msg = "拉取关键词翻页信息超时"
            if self.request_url(paging_url, tip_msg) is None:  # 拉取关键词翻页信息
                print(u"=== %s 翻页信息拉取失败，无效关键词，继续下一个词！" % self.keywords)
                return self.res_keywords
            str_xpath = "/html/body/div[3]/div[2]/div[4]/div/div[2]/span"
            res_page = self.ele_waiting(str_xpath, "xpath", True, False)
            if res_page is not None:
                res_page_num = res_page.text.split(" ")[1]
                if res_page_num != "":
                    self.page_keywords = int(res_page_num.strip())

        if self.title_counter <= 0 and self.page_keywords >= 10:
            self.res_keywords["valid"] = True

        return self.res_keywords

    def searching(self):
        """
        关键词搜索，以广度为优先（bfs）
        """
        queue = []
        queue_seen = set()  # 保存已处理过的关键词
        sql_datas = []  # 插入数据库所需参数
        file_datas = []  # 插入文件所需数据
        queue.append(self.keywords)
        queue_seen.add(self.keywords)
        len_queue = len(queue)

        while len_queue > 0:
            is_past_keywords = False  # 是否存在过滤词
            is_includ_keywords = False  # 是否包含指定词
            self.keywords = queue.pop(0)  # 取出第一个关键词

            # 关键词存在过滤词不做处理
            for past_kw in self.filter_keywords:
                if past_kw in self.keywords:
                    is_past_keywords = True
                    break
            # 关键词不包含指定词不做处理
            for inl_kw in self.include_keywords:
                if inl_kw in self.keywords:
                    is_includ_keywords = True
                    break
            # 重复关键词，或者存在过滤词的关键词不做处理
            if is_past_keywords or not is_includ_keywords:
                len_queue = len(queue)  # 重新计算队列长度，避免无效的循环
                continue
            # 判断当前关键词状态，并获取相关词
            r_keywords = self.is_valid_keywords()
            # 添加关键词到待处理队列
            for kw in r_keywords["sub_keywords"]:
                if kw.strip() != "" and kw not in queue_seen:
                    queue.append(kw)
                    queue_seen.add(kw)
            # 重新计算队列长度
            len_queue = len(queue)
            # 打印提示信息，方便跟踪进度
            self.print_tips(self.total_keywords, len_queue)
            # 保存有效关键词
            if r_keywords["valid"]:
                if self.keywords != "":
                    self.total_keywords += 1
                    #sql_datas.append((None, self.keywords))
                    file_datas.append(self.keywords)
                # 写入文件 2 个词一写，数据库暂时不考虑
                if self.total_keywords % 2 == 0:
                    self.write_file(file_datas)
            # 重置所有状态值，为下个关键词作准备
            self.status_rest()
        # 将剩余关键词写入文件
        self.write_file(file_datas)

    def print_tips(self, c_index, t_index):
        """
        打印提示消息
        """
        is_valid_kw = u"有效词"
        if not self.res_keywords["valid"]:
            is_valid_kw = u"无效词"
        print(u"== ({} / {}) {}，共有相关词:{} 个,首页出现:{}次，页数为：{}，结果是：{}。".format(
            c_index, t_index, self.keywords,
            len(self.res_keywords["sub_keywords"]),
            str(5 - self.title_counter), self.page_keywords, is_valid_kw))


if __name__ == "__main__":
    seconds = 10
    url = "https://m.baidu.com/"

    #keywords,f_keywords,i_keywords 由.sh提供参数
    f_keywords, i_keywords = [], []
    keywords = sys.argv[1]
    if keywords.strip() == "":
        print(u"主关键词不能为空,请重试...")
        os._exit(0)
    if sys.argv[2].strip() != "_fkw_":
        if "," in sys.argv[2]:
            f_keywords = sys.argv[2].split(",")
        else:
            f_keywords = sys.argv[2]
    if sys.argv[3].strip() != "_iKw_":
        if "," in sys.argv[3]:
            i_keywords = sys.argv[3].split(",")
        else:
            i_keywords = sys.argv[3].strip()


    print(u"====================================")
    # print(u"==初始化数据库")
    # sqlhelper = dbHelper()
    # print(u"==数据库初始完毕")

    mk = MobileKeywords(url, keywords, seconds, f_keywords, i_keywords)
    mk.browser.set_page_load_timeout(seconds)  # 页面超时时间为10S
    # mk.dbHelper = sqlhelper
    mk.init_save_info()
    print(u"==开始采集关键词 %s" % keywords)
    mk.searching()
    mk.browser.quit()
    print(u"==关键词采集结束")
    print(u"====================================")
