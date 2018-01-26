#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.product_line
~~~~~~~~~~~~~~~~~~~~~~~~

封装对于生产线的基本操作
提供增删改擦以及一些特定方法
"""

from datetime import datetime
from bson.objectid import ObjectId

from connection import client
from model.mongo_model.factory import FactoryDB
from model.mongo_model.workshop import WorkShopDB
from model.mongodb import insert_cache


class ProductLineDB(object):
    """生产线操作的封装"""

    def __init__(self, factory_id=None):
        super(ProductLineDB, self).__init__()
        self.dict = {}
        self.factory_id = factory_id
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = 'productline'
        self.db = self.client[self.db_name]
        self.collection = self.db['productline']

    def __repr__(self):
        return "<ProductLine('%s')>" % self.dict['name']

    def insert(self, name=None, workshop_id=None):
        self.dict['_id'] = ObjectId().__str__()
        self.dict['name'] = name
        self.dict['factory_id'] = self.factory_id
        self.dict['workshop_id'] = workshop_id
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [self.dict])
            return self.dict['_id']
        except:
            return None

    def update(self, id=None, name=None, factory_id=None, workshop_id=None):
        update_dict = dict()
        if name:
            update_dict['name'] = name
        if factory_id:
            update_dict['factory_id'] = factory_id
        if workshop_id:
            update_dict['workshop_id'] = workshop_id
        if update_dict:
            self.collection.update({"_id": id}, {"$set": update_dict})
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'update',
                         [{"_id": id}, {"$set": update_dict}])
            return id
        else:
            return None

    def remove(self, id=None):
        try:
            self.collection.remove({"_id": id})
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'remove', [{"_id": id}])
            return id
        except:
            return None

    def find(self, id=None, factory_id=None, workshop_id=None):
        if id:
            return self.collection.find_one({"_id": id}, {"create_time": 0})
        elif factory_id:
            return self.collection.find({"factory_id": factory_id})
        elif workshop_id:
            return self.collection.find({"workshop_id": workshop_id}, {"_id": 1, "name": 1})
        else:
            return None

    def findall(self, number=None, page=None):
        # 返回该工厂下的所有生产线
        try:
            result = []
            lines = self.collection.find({}, {"create_time": 0}).skip(number).limit(page)
            for line in lines:
                factory_name = FactoryDB().find(line['factory_id'])['name']
                workshop_name = WorkShopDB(line['factory_id']).find(id=line['workshop_id'])['name']
                line['factory_name'] = factory_name
                line['workshop_name'] = workshop_name
                result.append(line)
            return result
        except Exception as e:
            return None

    def close(self):
        self.client.close()

    def get_counts_by_field(self, field, value):
        """
        通过字段和该字段的值，在数据库中进行索引获取符合条件的工厂数量
        :param field: 字段
        :param value: 值
        :return: 成功返回符合条件的工厂数量，失败或者为空返回None
        """
        try:
            count = self.collection.find({field: value}).count()
            if count == 0:
                count = None
            return count
        except:
            return None
