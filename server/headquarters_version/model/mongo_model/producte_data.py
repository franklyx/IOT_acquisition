#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.product_data
~~~~~~~~~~~~~~~~~~~~~~

封装对生产数据的操作
提供插入和查找的接口，以及生成班组报表的统计方法
"""

from connection import client
from bson.objectid import ObjectId
from model.mongodb import insert_cache


class ProductData(object):
    """生产数据操作"""

    def __init__(self, equip_id, factory_id):
        super(ProductData, self).__init__()
        self.dict = {}
        self.equip_id = equip_id
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(equip_id)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.table_name]
        self.collection.ensure_index('ManufacturingCode')

    def __repr__(self):
        return "<Product data for('%s')>" % self.equip_id

    def insert(self, data=None):
        try:
            data['_id'] = ObjectId().__str__()
            self.collection.insert(data)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [data])
            return data['_id']
        except:
            return None

    def remove(self, id=None):
        try:
            self.collection.remove({"_id": ObjectId(id)})
            # 插入缓存数据库
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

    def get_group_report(self, factory_number, start_time, end_time):
        """
        从生产数据中统计出指定设备在指定指定时间段的信息
        :param factory_number: 工厂id
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: 返回记录的条数以及统计出来的信息字典
        """
        try:
            pipe = [{'$match': {'ManufacturingCode': factory_number,
                                "Timestamp": {"$gte": start_time, "$lte": end_time}}},
                    {"group": {'_id': None,
                               'Avg_State': {'$avg': '$State'},
                               'Avg_PhaseVoltageInput': {'$avg': '$PhaseVoltageInput'},
                               'Avg_LineVin': {'$avg': '$LineVin'},
                               'Avg_LineIin': {'$avg': '$LineIin'},
                               'Avg_PhaseVinAB': {'$avg': '$PhaseVinAB'},
                               'Avg_PhaseVinBC': {'$avg': '$PhaseVinBC'},
                               'Avg_PhaseVinCA': {'$avg': '$PhaseVinCA'},
                               'Avg_PhaseIinAB': {'$avg': '$PhaseIinAB'},
                               'Avg_PhaseIinBC': {'$avg': '$PhaseIinBC'},
                               'Avg_PhaseIinCA': {'$avg': '$PhaseIinCA'},
                               'Avg_InputPower': {'$avg': '$InputPower'},
                               'Avg_DCVout': {'$avg': '$DCVout'},
                               'Avg_DCIout': {'$avg': '$DCIout'},
                               'Avg_EfficiencyRatio': {'$avg': '$EfficiencyRatio'},
                               'Avg_GasFlow ': {'$avg': '$GasFlow'},
                               'Avg_Temperature1': {'$avg': '$Temperature1'},
                               'Avg_Temperature2': {'$avg': '$Temperature2'},
                               'Avg_OCAlarm ': {'$avg': '$OCAlarm'},
                               'Avg_OVAlarm': {'$avg': '$OVAlarm'}}}

                    ]
            count = self.collection.find({"ManufacturingCode": factory_number},
                                         {"Timestamp": {"$gte": start_time,
                                                        "$lte": end_time}}).count()
            data = self.collection.aggregate(pipeline=pipe)
            return count, data
        except:
            return None

    def close(self):
        self.client.close()
