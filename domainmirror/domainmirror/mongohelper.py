#encoding:utf-8

from pymongo import MongoClient


class mongoHelper:
    """
    数据库辅助类
    """

    def __init__(self):
        """
        数据库初始化
        """
        self.conn = MongoClient("mongodb://localhost:27017")

    def db_close(self):
        """
        关闭数据库操作
        """
        if self.conn:
            self.conn.close()

    def insert_category(self, list_cats, site_name):
        """
        插入当前网站的栏目信息
        :param list_cats:栏目信息列表
        :param site_name:栏目所属网站名称
        return 返回插入成功的数据id
        """
        # 栏目相对于网站根目录的路径
        # 栏目的关键词（如果没有，默认给数据库中存储的新闻标签）
        # 首页的更新区域如何与栏目页的更新区域结合起来
        # 关键词挂tdk还是挂对联？
        # 新闻标签库的设计？
        # 关键词库的设计
        try:
            collection = self.conn['ironman']['categories']
            cate_parames = {"sn": site_name, "lc": []}
            for c in list_cats:
                cate_parames["lc"].append({
                    "p": c.path, # 栏目路径
                    "k": c.keywords, # 栏目关键词
                    "t": c.template, # 栏目模板
                    "ti": c.template_arc # 内容页模板
                })
        except:
            print(u"数据库操作错误")
        return collection.insert_one(cate_parames) # 插入到数据库

    def icn_get_all(self):
        """
        获取所有过滤的栏目名称
        icn为集合 invalid_cat_name 的缩写
        """
        return self.conn['ironman']['invalid_cat_name'].find()

    def pt_by_type(self, _type):
        """
        获取指定类型的模板
        :param _type:模板类型 list-栏目 page-内页
        pt为集合 page_template 的缩写
        """
        conditions = {}
        conditions["type"] = _type
        return self.conn['ironman']['page_template'].find(conditions)
