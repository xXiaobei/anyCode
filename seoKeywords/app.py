"""
挖词工具
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re, time, os

# browser = webdriver.Chrome(executable_path='/home/bbei/envPython/anycode/chromedriver')
# 在网上下载好 chromedriver 后，移动到 /usr/local/bin 下，不用在启动chrome指定 chromedriver的路径
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)  # 默认等待操作超时时间为5s
res_keywords = []


def keywords_relations(kw_search):
    """
    获取但前关键词的相关词
    :param kw_search: 代检索的关键词
    :return: list 相关词
    """
    list_relations = []
    try:
        browser.get("https://www.baidu.com")
        txt_search = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#kw')))
        bnt_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#su")))

        txt_search.send_keys(kw_search)
        bnt_submit.click()

        # 当出现“下一页”按钮时，认为当前所有页面完全加载
        # 或者出现相关搜索（#rs > div）时，认为当前页面完全加载
        # 若没有相关搜索和“下一页”按钮，则认为该关键词被屏蔽
        bnt_next = right_conditions(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page > a.n")))
        kw_relations = right_conditions(EC.presence_of_element_located((By.CSS_SELECTOR, "#rs")))
        if not bnt_next and not kw_relations:
            return []

        if kw_relations:
            links = kw_relations.find_elements_by_xpath(".//table/tbody/tr/th/a")
            if links:
                for lnk in links:
                    list_relations.append(lnk.text)
    except TimeoutException:
        return keywords_relations(kw_relations)  # 超时则重试
    return list_relations


def keywords_bfs(kw_start):
    """
    关键词 bfs算法搜索
    :return:
    """
    queue = []
    queue.append(kw_start)
    res_keywords.append(kw_start)

    while len(queue) > 0:
        kw_current = queue.pop(0)
        kw_relations = keywords_relations(kw_current)

        # 停止条件 用于测试
        if len(res_keywords) > 1200:
            result_file()  # 结果写入文件
            browser.quit()  # 清理资源
            break

        for kw in kw_relations:
            if kw not in res_keywords:
                queue.append(kw)
                res_keywords.append(kw)


def right_conditions(condition):
    """
    从当前页面中判断当前的expected_conditions 是否成立
    :param condition: 等待检测的condition
    :return: 返回conditions 所查询的 element, 失败返回None
    """
    try:
        return wait.until(condition)
    except TimeoutException:
        return None


def result_file():
    """
    将搜索结果写入到文件
    :return:
    """
    file_content = ''
    file_path = "/home/bbei/Documents/zhaoshengxiao.txt"
    for kw in res_keywords:
        file_content += kw + "\n"
    with open(file_path, 'w') as f:
        f.write(file_content)
    print('关键词结果已经保存到文件 zhaoshengxiao.txt ')


def main():
    """
    入口函数
    """
    start_kw = u'找生肖'
    keywords_bfs(start_kw)  # 测试以广度优先（bfs）算法拉取关键词


if __name__ == "__main__":
    main()
