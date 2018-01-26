#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.workshop
~~~~~~~~~~~~~~~~~~~~

封装对于车间的数据库的基本操作
提供增删改查接口以及一些特定的方法
"""

from datetime import datetime
from bson.objectid import ObjectId

from connection import client
from model.mongodb import insert_cache
from model.mongo_model.factory import FactoryDB


class WorkShopDB(object):
    """车间操作的封装"""

    def __init__(self, factory_id=None):
        super(WorkShopDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = 'workshop'
        self.db = self.client[self.db_name]
        self.collection = self.db['workshop']
        self.dict['factory_id'] = factory_id

    def __repr__(self):
        return "<WorkShop('%s')>" % self.dict['name']

    def insert(self, name=None):
        self.dict['_id'] = ObjectId().__str__()
        self.dict['name'] = name
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [self.dict])
            return self.dict['_id']
        except:
            return None

    # 车间不能更改所属的工厂
    def update(self, id=None, name=None):
        update_dict = dict()
        update_dict['name'] = name
        try:
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

    def find(self, id=None, factory_id=None):
        if id:
            return self.collection.find_one({"_id": id}, {'create_time': 0})
        elif factory_id:
            return self.collection.find({"factory_id": factory_id}, {"_id": 1, "name": 1})
        else:
            return None

    def findall(self, number=None, page=None):
        # 返回该工厂下的所有的车间
        try:
            result = []
            workshops = self.collection.find({}, {'create_time': 0}).skip(number).limit(
                page)
            for workshop in workshops:
                factory_name = FactoryDB().find(workshop['factory_id'])['name']
                workshop['factory_name'] = factory_name
                result.append(workshop)
            return result
        except:
            return None

    def close(self):
        self.client.close()

    def get_counts_by_field(self, field, value):
        """
        通过字段和该字段的值，在数据库中进行索引获取符合条件的车间数量
        :param field: 字段
        :param value: 值
        :return: 成功返回符合条件的车间数量，失败或者为空返回None
        """
        try:
            count = self.collection.find({field: value}).count()
            if count == 0:
                count = None
            return count
        except:
            return None
