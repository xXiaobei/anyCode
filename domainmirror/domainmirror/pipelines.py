# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join


class FileDownloandPipeline(FilesPipeline):
    """
    文件下载处理管道 FSFilesStore
    TODO：暂时没有处理重复的情况，测试框架去重功能
    """

    def process_item(self, item, spider):
        pass

    def file_path(self, request, response=None, info=None):
        """
        重写file_path 自定义文件保存路径
        :param request:
        :param response:
        :param info:
        :return:
        """
        path = urlparse(request.url).path
        temp = join(basename(dirname(path)), basename(path))
        return '%s/%s' % (basename(dirname(path)), basename(path))
