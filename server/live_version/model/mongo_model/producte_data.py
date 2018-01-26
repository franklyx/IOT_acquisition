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
from model.mongo_model.write_cache import insert_cache


class ProductData(object):
    """生产数据操作"""

    def __init__(self, factory_number, factory_id):
        super(ProductData, self).__init__()
        self.dict = {}
        self.equip_id = factory_number
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(factory_number)
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

    def get_group_report(self, start_time, end_time):
        """
        从生产数据中计算出指定设备在指定指定时间段的平均值
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: 统计出来的平均值
        """
        try:
            pipe = [{'$match': {'Timestamp': {"$gte": start_time, "$lte": end_time}
                                }},
                    {"$group": {'_id': None,
                                'State': {'$avg': '$State'},
                                'PhaseVoltageInput': {'$avg': '$PhaseVoltageInput'},
                                'LineVin': {'$avg': '$LineVin'},
                                'LineIin': {'$avg': '$LineIin'},
                                'PhaseVinAB': {'$avg': '$PhaseVinAB'},
                                'PhaseVinBC': {'$avg': '$PhaseVinBC'},
                                'PhaseVinCA': {'$avg': '$PhaseVinCA'},
                                'PhaseIinAB': {'$avg': '$PhaseIinAB'},
                                'PhaseIinBC': {'$avg': '$PhaseIinBC'},
                                'PhaseIinCA': {'$avg': '$PhaseIinCA'},
                                'InputPower': {'$avg': '$InputPower'},
                                'DCVout': {'$avg': '$DCVout'},
                                'DCIout': {'$avg': '$DCIout'},
                                'EfficiencyRatio': {'$avg': '$EfficiencyRatio'},
                                'GasFlow ': {'$avg': '$GasFlow'},
                                'Temperature1': {'$avg': '$Temperature1'},
                                'Temperature2': {'$avg': '$Temperature2'},
                                'OCAlarm ': {'$avg': '$OCAlarm'},
                                'OVAlarm': {'$avg': '$OVAlarm'}}}

                    ]

            data = self.collection.aggregate(pipeline=pipe)
            return list(data)
        except:
            return None

    def get_counts_by_equipment(self, factory_number):
        """
        获取设备在生产数据中的条数
        :param factory_number: 出厂编号
        :return: 成功返回总条数
        """
        try:
            count = self.collection.find({"ManufacturingCode": factory_number}).count()
            return count
        except:
            return None

    def get_product_data(self, field, start_time, end_time):
        """
        从生产数据中统计出设备在指定时间段的指定参数的数据集合
        :param field: 查询字段
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: 成功返回数据的list
        """
        try:
            if field == "PhaseVin":
                pipe = [{'$match': {'Timestamp': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$Timestamp'},
                                    'PhaseVinAB': {'$push': '$PhaseVinAB'},
                                    'PhaseVinBC': {'$push': '$PhaseVinBC'},
                                    'PhaseVinCA': {'$push': '$PhaseVinCA'}}}
                        ]
            elif field == "PhaseIin":
                pipe = [{'$match': {'Timestamp': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$Timestamp'},
                                    'PhaseIinAB': {'$push': '$PhaseIinAB'},
                                    'PhaseIinBC': {'$push': '$PhaseIinBC'},
                                    'PhaseIinCA': {'$push': '$PhaseIinCA'}}}
                        ]
            elif field == "Temperature":
                pipe = [{'$match': {'Timestamp': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$Timestamp'},
                                    'Temperature1': {'$push': '$Temperature1'},
                                    'Temperature2': {'$push': '$Temperature2'}}}
                        ]
            else:
                pipe = [{'$match': {'Timestamp': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$Timestamp'},
                                    field: {'$push': '$' + field}}}
                        ]

            data = self.collection.aggregate(pipeline=pipe)
            return list(data)
        except:
            return None

    def close(self):
        self.client.close()
