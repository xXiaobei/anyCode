"""
#百度m端挖词工具
#无效关键词判断标准：
# 1：没有搜索结果
# 2：搜索结果没有10页，且第一页搜索结果没有包含5条关键词收录
"""

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MobileKeywords:
    """
    百度手机端关键词挖掘
    """

    def __init__(self, tag_url, tag_kw, wait_seconds):
        """
        初始化
        :param tag_url:需要加载的网页地址
        :param wait_seconds:显示等待时间，默认为10S
        """
        self.url = tag_url
        self.keywords = tag_kw
        self.retry_counter = 1  # 失败重试次数
        self.title_counter = 5  # 关键词在搜索结果中出现的次数
        self.page_keywords = 0  # 关键词搜索结果总页
        self.res_keywords = {"valid": True, "sub_keywords": []}
        self.browser = webdriver.Chrome(chrome_options=self.init_driver())
        self.wait = WebDriverWait(self.browser, wait_seconds)

    def init_driver(self):
        """
        webdriver 配置项
        """
        opt = ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2} # 禁止加载图片
        opt.add_experimental_option("prefs", prefs)
        opt.add_argument("blink-settings=imagesEnabled=false")  # 禁止加载图片
        opt.add_argument('--headless')  # 无界面模式
        opt.add_argument('--disable-gpu')  # 禁止使用硬件加速
        opt.add_argument(
            "user-agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'"
        )  # 自定义请求头
        return opt

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
        except TimeoutError as ex:
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
        self.browser.get(self.url)

        # 等待搜索框和搜索按钮加载完成
        txt_search = self.ele_waiting("#index-kw", "css", "located", True)
        btn_search = self.ele_waiting("#index-bn", "css", "click", True)

        # 发送关键词，等待搜索结果
        txt_search.send_keys(self.keywords)
        btn_search.click()

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
            #str_xpath = "//div[1]/article/header/div/a/h3"
            for title in res_search:
                if u"其他人还在搜" in title.text: # 其他人还在搜 相关词
                    kw_others = title.text.split("\n")
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
            paging_url = paging_url.get_attribute("href").replace(
                "pn=10", "pn=90")
            self.browser.get(paging_url)
            str_xpath = "/html/body/div[3]/div[2]/div[4]/div/div[2]/span"
            res_page = self.ele_waiting(str_xpath, "xpath", True, False)
            if res_page is not None:
                res_page_num = res_page.text.split(" ")[1]
                if res_page_num != "":
                    self.page_keywords = int(res_page_num.strip())

        if self.title_counter <= 0 and self.page_keywords >= 10:
            self.res_keywords["valid"] = True

        return self.res_keywords


if __name__ == "__main__":
    seconds = 10
    url = "https://m.baidu.com/"
    keywords = "明晚开什么生肖"

    # 提示初始化方法，每次循环后不用重新声明对象，调用对象的初始化方法即可。（清空对应的标识和值即可）

    mk = MobileKeywords(url, keywords, seconds)
    mk.browser.get(mk.url)
    # print(mk.browser.page_source)
    mk.is_valid_keywords()
    mk.browser.quit()
