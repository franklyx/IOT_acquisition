#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.alarm_data
~~~~~~~~~~~~~~~~~~~~~~

封装对报警数据库的操作
提供了报警信息的增删改方法
"""
from connection import client
from bson.objectid import ObjectId
from model.redis_model.filter_id import FilterId
from model.mongo_model.write_cache import insert_cache


class AlarmData(object):
    """封装报警数据处理方法"""

    def __init__(self, factory_number, factory_id):
        super(AlarmData, self).__init__()
        self.dict = {}
        self.factory_number = factory_number
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(factory_number) + '_alarm'
        self.db = self.client[self.db_name]
        self.collection = self.db[self.table_name]
        # 添加设备状态的三个字段的索引
        self.collection.ensure_index('OCAlarm')
        self.collection.ensure_index('OVAlarm')
        self.collection.ensure_index('AlarmCode')
        self.collection.ensure_index('Timestamp')

    def __repr__(self):
        return "<Alarm Data for('%s')>" % self.factory_number

    def insert(self, data=None):
        try:
            data['_id'] = ObjectId().__str__()
            self.collection.insert(data)
            insert_cache(self.db_name, self.table_name, 'insert', [data])
            return data['_id']
        except:
            return None

    def remove(self, id=None):
        try:
            self.collection.remove({"_id": ObjectId(id)})
            insert_cache(self.db_name, self.table_name, 'remove', [{"_id": ObjectId(id)}])
            return id
        except:
            return None

    def find(self, id):
        try:
            return self.collection.find_one({"_id": ObjectId(id)})
        except:
            return None

    def findall(self, factory_number, number=None, page=None):
        """这里要对报警信息进行倒序，分割出已处理的报警数据和未处理的报警数据"""
        try:
            result = dict()
            filter_id = FilterId().find(factory_number)
            if filter_id:
                untreated = self.collection.find({"_id": {"$gte": filter_id}}).sort(
                    [("_id", -1)]).skip(number).limit(page)
                has_been = self.collection.find({"_id": {"$lt": filter_id}}).sort(
                    [("_id", -1)]).skip(number).limit(page)
            else:
                untreated = None
                has_been = self.collection.find().sort(
                    [("_id", -1)]).skip(number).limit(page)
            result["has_been"] = list(has_been)
            result["untreated"] = list(untreated)
            return result
        except:
            return None

    def close(self):
        self.client.close()
