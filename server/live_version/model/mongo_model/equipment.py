#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.workshop
~~~~~~~~~~~~~~~~~~~~

封装对于设备的数据库的基本操作
提供增删改查接口以及一些特定的方法
"""
from datetime import datetime
from connection import client
from bson.objectid import ObjectId

from model.mongo_model.write_cache import insert_cache
from model.mongo_model.factory import FactoryDB
from model.mongo_model.workshop import WorkShopDB
from model.mongo_model.product_line import ProductLineDB


class EquipmentDB(object):
    """设备操作的封装"""

    def __init__(self, factory_id=None):
        super(EquipmentDB, self).__init__()
        self.dict = {}
        self.factory_id = factory_id
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = 'equipment'
        self.db = self.client[self.db_name]
        self.collection = self.db['equipment']

    def __repr__(self):
        return "<Equipment for factory('%s')>" % self.factory_id

    def insert(self, name=None, workshop_id=None, line_id=None,
               factory_number=None, factory_time=None,
               product_number=None):
        self.dict['_id'] = ObjectId().__str__()
        self.dict['name'] = name
        self.dict['line_id'] = line_id
        self.dict['factory_id'] = self.factory_id
        self.dict['workshop_id'] = workshop_id
        self.dict['factory_time'] = factory_time
        self.dict['factory_number'] = factory_number
        self.dict['product_number'] = product_number
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [self.dict])
            return self.dict['_id']
        except:
            return None

    def update(self, id=None, name=None, factory_id=None, workshop_id=None, line_id=None,
               factory_number=None, factory_time=None,
               product_number=None):
        update_dict = {}
        if name:
            update_dict['name'] = name
        if factory_id:
            update_dict['factory_id'] = factory_id
        if workshop_id:
            update_dict['workshop_id'] = workshop_id
        if line_id:
            update_dict['line_id'] = line_id
        if factory_number:
            update_dict['factory_number'] = factory_number
        if factory_time:
            update_dict['factory_time'] = factory_time
        if product_number:
            update_dict['product_number'] = product_number
        if update_dict:
            try:
                self.collection.update({"_id": id}, {"$set": update_dict})
                # 插入缓存数据库
                insert_cache(self.db_name, self.table_name, 'update',
                             [{"_id": id}, {"$set": update_dict}])
                return id
            except:
                return None
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

    def find(self, id=None, factory_id=None, workshop_id=None, line_id=None, factory_number=None,
             factory_time=None, product_number=None):
        if id:
            return self.collection.find_one({"_id": id}, {"create_time": 0})
        elif factory_id:
            return self.collection.find({"factory_id": factory_id}, {"create_time": 0})
        elif workshop_id:
            return self.collection.find({"workshop_id": workshop_id}, {"create_time": 0})
        elif line_id:
            return self.collection.find({"line_id": line_id}, {"create_time": 0})
        elif factory_number:
            return self.collection.find({"factory_number": factory_number}, {"create_time": 0})
        elif factory_time:
            return self.collection.find({"factory_time": factory_time}, {"create_time": 0})
        elif product_number:
            return self.collection.find({"product_number": product_number}, {"create_time": 0})
        else:
            return None

    def findall(self, number=None, page=None):
        # 返回该工厂下的所有的车间
        try:
            result = []
            equipments = self.collection.find({}, {'create_time': 0}).skip(number).limit(page)
            for equipment in equipments:
                factory_name = FactoryDB().find(equipment['factory_id'])['name']
                workshop_name = \
                    WorkShopDB(equipment['factory_id']).find(id=equipment['workshop_id'])['name']
                line_name = ProductLineDB(equipment['factory_id']).find(id=equipment['line_id'])[
                    'name']
                equipment['factory_name'] = factory_name
                equipment['workshop_name'] = workshop_name
                equipment['line_name'] = line_name
                result.append(equipment)
            return result
        except:
            return None

    def get_id_and_number(self):
        # 获取所有设备的id和出厂编号的字典组合成的迭代器对象
        try:
            equipments = self.collection.find({}, {"_id": 1, "factory_number": 1})
            return equipments
        except:
            return None

    def close(self):
        self.client.close()

    def get_counts_by_field(self, field, value):
        """
        通过字段和该字段的值，在数据库中进行索引获取符合条件的设备数量
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
