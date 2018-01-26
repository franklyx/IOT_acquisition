#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.daily_report
~~~~~~~~~~~~~~~~~~~~~~

实现对每日报表数据的封装
提供对后台定时生成的每日报表进行添加，查找的接口
"""

from connection import client
from bson.objectid import ObjectId
from model.mongodb import insert_cache


class DailyReportDB(object):
    """每日报表操作封装"""

    def __init__(self, factory_id=None, equipment_id=None):
        super(DailyReportDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(equipment_id) + '_daily_report'
        self.db = self.client[self.db_name]
        self.collection = self.db[self.table_name]

    def insert(self, data):
        try:
            data['_id'] = ObjectId().__str__()
            self.collection.insert(data)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [data])
            return data['_id']
        except:
            return None

    # TODO 支持日期时间段查询，关键字查询
    def findall(self, number=None, page=None):
        try:
            result = self.collection.find({}, {"_id": 1, "name": 1}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()
