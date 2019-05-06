"""
挖词工具
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re,time

# browser = webdriver.Chrome(executable_path='/home/bbei/envPython/anycode/chromedriver')
# 在网上下载好 chromedriver 后，移动到 /usr/local/bin 下，不用在启动chrome指定 chromedriver的路径
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10) # 默认等待操作超时时间为10s
res_keywords = []

def search(start_kw):
    """
    获取百度下拉词，相关词
    """
    try:
        browser.get("https://www.baidu.com")
        ipt_search = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#kw')))
        ipt_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#su")))

        ipt_search.send_keys(start_kw)
        ipt_submit.click()

        ipt_nextbtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#page > a.n")))
        if not ipt_nextbtn:
            if len(res_keywords) > 0:
                return res_keywords
            else:
                return []
        
        res_search = browser.find_element_by_css_selector("#rs")

        if(res_search):
            res_links = []
            links = res_search.find_elements_by_xpath(".//table/tbody/tr/th/a")
            if len(links) > 0:
                res_keywords.append(links[0].text)
                print(len(res_keywords))
                if len(res_keywords) <= 1000:
                    search(links[0].text)

    except TimeoutException:
        pass
    
    return res_keywords

def main():
    """
    入口函数
    """
    start_kw = u'生肖'
    res_list_kw = search(start_kw)

    if res_list_kw:
        print(res_list_kw)
    else:
        print("{} 已屏蔽,更换起始词重新搜索！".format(start_kw))

    browser.quit()

if __name__ == "__main__":
    main()
    time.sleep(5)
    browser.quit()
