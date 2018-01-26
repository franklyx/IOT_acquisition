#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
redis_model.filter_id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

定义设备分割已处理报警信息和未处理报警信息的插入和查找接口
"""
from connection import client


class FilterId(object):
    def __init__(self):
        self.client = client

    def __repr__(self):
        return "<The filter id information object>"

    def insert(self, factory_number, value):
        try:
            id = factory_number + '_alarm'
            self.client.set(id, value)
            self.client.save()
            return id
        except:
            return None

    def find(self, factory_number):
        try:
            id = factory_number + '_alarm'
            result = self.client.hgetall(id)
            return result['start_id']
        except:
            return None
