# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse
from os.path import basename, dirname, join
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import FilesPipeline


class FileDownloandPipeline(object):
    """
    文件下载处理管道 FSFilesStore
    """
    def process_item(self,item,spider):
        return item

    # 重写 open_spider 蜘蛛被开启时，调用该函数
    # def open_spider(self, spider)

    # 重写 close_spider 蜘蛛关闭后，调用该函数
    # def close_spider(self, spider)

    # def get_media_requests(self, item, info):
    #     """
    #     重写get_media_requests
    #     让scrapy 引擎告诉 调度器scheduled 下载对应url
    #     下载任务的优先级高于爬取页面的优先级
    #     所有的下载任务完成后会回调函数 item_completed
    #     """
    #     for file_url in item["file_urls"]:
    #         yield Request(file_url, meta={'item', item})

    # def file_path(self, request, response=None, info=None):
    #     """
    #     重写file_path 自定义文件名
    #     :param request:
    #     :param response:
    #     :param info:
    #     :return:
    #     """
    #     path = urlparse(request.url).path
    #     # temp = join(basename(dirname(path)), basename(path))
    #     return '%s/%s' % (basename(dirname(path)), basename(path))

    # def item_completed(self, results, item, info):
    #     """
    #     所有文件下载完成后的回调函数,失败的item不用监测
    #     """
    #     #当单个Item完成下载时的处理办法。因为并不是每张图片都会下载成功，所以需要分析下载结果和剔除下载失败的图片。
    #     #如果某张图片下载失败，就不需要保存此item到数据库。
    #     #参数results就是该Item对应的下载结果，它是一个列表形式，列表每一个元素是一个元组，其中包含下载成功或失败的信息。
    #     #在这里，我们遍历下载结果找出所有成功的下载列表,如果列表为空,该item对应的图片下载失败，跑出DropItem异常，该Item忽略，否则返回Item
    #     image_paths = [x["path"] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem('Image Downloaded Failed')
    #     return item