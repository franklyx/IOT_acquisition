#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
redis_model.latest_equipment_info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

定义设备实时信息的插入和查找接口
"""
from connection import client


class LatestEquipInfoDB(object):
    def __init__(self):
        self.client = client

    def __repr__(self):
        return "<The latest equipment information object>"

    def insert(self, id, value):
        try:
            self.client.set(id, value)
            self.client.save()
            return id
        except:
            return None

    def find(self, id):
        try:
            result = self.client.get(id)
            return result
        except:
            return None
