#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.user
~~~~~~~~~~~~~~~~

封装对用户数据库的操作
实现用户的增删改查，以及用户获取所有用户的接口
"""

from datetime import datetime
from tools.encryption import Encryption
from bson.objectid import ObjectId

from connection import client
from tools.cfgparser import parser


class UserDB(object):
    """用户数据库的操作"""

    def __init__(self):
        super(UserDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db = self.client.factory
        self.collection = self.db.user

    def __repr__(self):
        return "<User('%s')>" % self.dict['username']

    def insert(self, username=None, user_role=None, password=None, factory_id=None):
        self.dict['_id'] = ObjectId().__str__()
        self.dict['user_role'] = user_role
        self.dict['username'] = username
        self.dict['factory_id'] = factory_id
        self.dict['password'] = Encryption.generate_password(password, parser.auth_salt)
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            return self.dict['_id']
        except:
            return None

    def update(self, id, username=None, password=None, user_role=None):
        update_dict = {}
        if username:
            update_dict['username'] = username
        if password:
            update_dict['password'] = Encryption.generate_password(password, parser.auth_salt)
        if user_role:
            update_dict['user_role'] = int(user_role)
        if update_dict:
            try:
                self.collection.update({"_id": id}, {"$set": update_dict})
                return id
            except:
                return None

    def remove(self, id=None):
        try:
            self.collection.remove({"_id": id})
            return id
        except:
            return None

    def find(self, id=None, username=None):
        if id:
            try:
                return self.collection.find_one({"_id": id}, {"create_time": 0})
            except:
                return None
        elif username:
            try:
                return self.collection.find_one({"username": username}, {"create_time": 0})
            except:
                return None
        else:
            return None

    def findall(self, number=None, page=None):
        try:
            result = self.collection.find({}, {'create_time': 0}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()
