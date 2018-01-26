#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.workgroup
~~~~~~~~~~~~~~~~~~~~~~

封装班组数据库的操作
实现真删改查以及其他特定的方法
"""
from datetime import datetime
from connection import client
from bson.objectid import ObjectId
from model.mongodb import insert_cache


class WorkGroupDB(object):
    """班组数据库的操作"""

    def __init__(self, factory_id=None):
        super(WorkGroupDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = 'workgroup'
        self.db = self.client[self.db_name]
        self.collection = self.db['workgroup']

    def __repr__(self):
        return "<WorkGroup('%s')>" % self.dict['name']

    def insert(self, name=None, equipment_list=None):
        self.dict['_id'] = ObjectId().__str__()
        self.dict['name'] = name
        self.dict['equipment_list'] = equipment_list
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [self.dict])
            return self.dict['_id']
        except:
            return None

    def update(self, id=None, name=None, equipment_list=None):
        try:
            update_dict = dict()
            if name:
                update_dict['name'] = name
            if isinstance(equipment_list, list):
                update_dict['equipment_list'] = equipment_list
            self.collection.update({"_id": id}, {"$set": update_dict})
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'update',
                         [{"_id": id}, {"$set": update_dict}])
            return id
        except:
            return None

    def remove(self, id=None):
        try:
            self.collection.remove({"_id": id})
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'remove', [{"_id": id}])
            return id
        except:
            return None

    def find(self, id=None):
        try:
            result = self.collection.find_one({"_id": id}, {"create_time": 0})
            return result
        except:
            return None

    def findall(self, number=None, page=None):
        # 返回所有的文档
        try:
            result = self.collection.find({}, {"_id": 1, "name": 1}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()

    def del_equipment_in_list(self, equipment_id):
        """
        删除设备时候，在班组中的设备列表中删除该设备
        :param equipment_id: 设备id
        :return: 成功返回该id,失败返回None
        """
        try:
            self.collection.update({'_id': {"$exists": 'true'}},
                                   {"$pull": {"equipment_list": equipment_id}}, multi=True)
            return equipment_id
        except:
            return None
