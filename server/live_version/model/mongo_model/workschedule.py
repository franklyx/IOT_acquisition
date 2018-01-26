#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.workshop
~~~~~~~~~~~~~~~~~~~~

封装对于班次的数据库的基本操作
提供增删改查接口以及一些特定的方法
"""
from datetime import datetime
from bson.objectid import ObjectId

from connection import client
from model.mongo_model.write_cache import insert_cache
from model.mongo_model.workgroup import WorkGroupDB


class WorkScheduleDB(object):
    """班次操作的封装"""

    def __init__(self, factory_id=None):
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = 'workschedule'
        self.db = self.client[self.db_name]
        self.collection = self.db['workschedule']

    def __repr__(self):
        return "<WorkSchedule('%s')>" % self.dict['group_id']

    def insert(self, group_id=None, start_time=None, end_time=None, name=None):
        self.dict['_id'] = ObjectId().__str__()
        self.dict['group_id'] = group_id
        self.dict['name'] = name
        self.dict['start_time'] = start_time
        self.dict['end_time'] = end_time
        self.dict['create_time'] = datetime.now()
        try:
            self.collection.insert(self.dict)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [self.dict])
            return self.dict['_id']
        except:
            return None

    def update(self, id=None, group_id=None, start_time=None, end_time=None, name=None):
        update_dict = {}
        if group_id:
            update_dict['group_id'] = group_id
        if start_time:
            update_dict['start_time'] = start_time
        if name:
            update_dict['name'] = name
        if end_time:
            update_dict['end_time'] = end_time
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

    def find(self, id=None, group_id=None):
        try:
            if id:
                result = self.collection.find_one({"_id": id})
                return result
            elif group_id:
                result = self.collection.find_one({"group_id": group_id})
                return result
            else:
                return None
        except:
            return None

    def findall(self, factory_id=None, number=None, page=None):
        """
        返回该工厂下的所有的班次信息
        :param factory_id: 工厂id
        :param number: 开始条数
        :param page: 返回条数
        :return: 成功返回制定位置的班次信息列表
        """
        try:
            result = []
            workschedules = self.collection.find({}, {"create_time": 0}).skip(number).limit(page)
            for workschedule in workschedules:
                workgroup_name = None
                if workschedule['group_id']:
                    print workschedule['group_id']
                    workgroup_name = WorkGroupDB(factory_id=factory_id).find(
                        id=workschedule['group_id'])['name']
                workschedule['workgroup_name'] = workgroup_name
                result.append(workschedule)
            return result
        except:
            return None

    def get_group_and_schedule(self):
        """返回所有班次的对象信息（迭代器）"""
        try:
            schedule_iter = self.collection.find({}, {"create_time": 0})
            return schedule_iter
        except:
            return None

    def set_none_for_groupid(self, group_id):
        """当班组被删除时，要在班次中将绑定了的班次的group_id设置为None"""
        try:
            self.collection.update({'group_id': group_id}, {"$set": {'group_id': None}}, multi=True)
            return group_id
        except:
            return None

    def close(self):
        self.client.close()
