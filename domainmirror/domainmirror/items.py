# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UlrItem(Item):
    """
    用于下载css、image、js文件
    """
    # file_urls 用于存储文件下载的url信息
    # file_urls 是存储在list中,赋值时注意
    # scrapy engine 会将给url发送给调度器
    file_urls = Field()
    # files 用于存储文件下载成功后的信息（路径、网络地址等）
    files = Field()


class PageItem(Item):
    """
    用于将所有的静态页面本地化
    """
    # 页面标题
    title = Field()
    # 页面关键词
    keywords = Field()
    # 页面描述
    description = Field()
    # 页面所属栏目
    category = Field()
    # 栏目路径
    category_path = Field()
    # 页面内容
    content = Field()
