from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    opt = ChromeOptions()
    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")
    opt.add_argument("blink-settings=imagesEnabled=false")
    opt.add_argument(
        "user-agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'"
    )
    opt.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=opt)

    browser.get("https://m.baidu.com")

    print(browser.page_source)
    browser.close()