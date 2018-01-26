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
from model.mongodb import insert_cache


class AlarmData(object):
    """封装报警数据处理方法"""

    def __init__(self, equip_id, factory_id):
        super(AlarmData, self).__init__()
        self.dict = {}
        self.equip_id = equip_id
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(equip_id) + '_alarm'
        self.db = self.client[self.db_name]
        self.collection = self.db[self.table_name]
        # 添加设备状态的三个字段的索引
        self.collection.ensure_index('OCAlarm')
        self.collection.ensure_index('OVAlarm')
        self.collection.ensure_index('AlarmCode')
        self.collection.ensure_index('Timestamp')

    def __repr__(self):
        return "<Alarm Data for('%s')>" % self.equip_id

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

    def findall(self, number=None, page=None):
        try:
            result = self.collection.find().skip(number).limit(page)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()
