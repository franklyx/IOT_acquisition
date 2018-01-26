#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.group_report
~~~~~~~~~~~~~~~~~~~~~~

封装了对后台生成的班组报告的操作
提供插入和查找的接口
"""

from connection import client
from bson.objectid import ObjectId
from model.mongodb import insert_cache


class GroupReportDB(object):
    """操作班组报表"""

    def __init__(self, factory_id=None, equipment_id=None):
        super(GroupReportDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(equipment_id) + '_group_report'
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

    # TODO 支持班组记录查询
    def findall(self, number=None, page=None):
        try:
            result = self.collection.find({}, {"_id": 1, "name": 1}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()
