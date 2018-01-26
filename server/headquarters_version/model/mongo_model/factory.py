#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.factory
~~~~~~~~~~~~~~~~~~~~~~

封装对工厂数据库的操作
提供对工厂进行增删改查的接口以及获取所有工厂的方法
"""
from datetime import datetime
from connection import client
from tools.cfgparser import parser
from model.mongodb import insert_cache


class FactoryDB(object):
    """工厂数据库操作"""

    def __init__(self):
        super(FactoryDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db = self.client.factory
        self.collection = self.db.factory

    def __repr__(self):
        return "<Factory('%s')>" % self.dict['name']

    def insert(self, name=None):
        self.dict['_id'] = parser.factoryid
        self.dict['name'] = name
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            # 插入缓存数据库
            insert_cache('factory', 'factory', 'insert', [self.dict])
            return self.dict['_id']
        except:
            return None

    def update(self, id=None, name=None):
        try:
            self.collection.update({"_id": id}, {"$set": {"name": name}})
            # 插入缓存数据库
            insert_cache('factory', 'factory', 'update', [{"_id": id}, {"$set": {"name": name}}])
            return id
        except:
            return None

    def remove(self, id=None):
        try:
            self.collection.remove({"_id": id})
            # 插入缓存数据库
            insert_cache('factory', 'factory', 'remove', [{"_id": id}])
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
        try:
            result = self.collection.find({}, {"_id": 1, "name": 1}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()

    def get_counts(self):
        """
        得到工厂的数量
        :return: 成功返回符合条件的工厂数量，失败或者为空返回None
        """
        try:
            count = self.collection.find().count()
            if count == 0:
                count = None
            return count
        except:
            return None
