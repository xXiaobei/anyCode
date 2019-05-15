"""
sqlite3 数据库辅助类
"""

import sqlite3
from os.path import dirname, join

db_file_path = join(dirname(__file__), "keywords.db")


class dbHelper:
    """
    sqlite3 工具类
    """

    def __init__(self):
        """
        初始化链接对象和游标
        """
        # isolation_level 自动提交（非智能提交）
        try:
            self.conn = sqlite3.connect(db_file_path, isolation_level=None)
            self.curs = self.conn.cursor()
        except:
            print('=============db init error!===========')

    def sql_list_comit(self, list_data):
        """
        批量事务执行sql语句
        """
        self.curs.execute("BEGIN TRANSACTION")  # 开启事务
        self.curs.executemany("INSERT INTO words VALUES (?,?)", list_data)
        self.curs.execute("COMMIT")  # 提交事务


if __name__ == "__main__":
    db = dbHelper()
    list_datas = []
    for i in range(1, 1000):
        list_datas.append((None, 'zhangsan' + str(i)))

    db.sql_list_comit(list_datas)
    print("ok")
