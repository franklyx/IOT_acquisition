#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.daily_report
~~~~~~~~~~~~~~~~~~~~~~

实现对每日报表数据的封装
提供对后台定时生成的每日报表进行添加，查找的接口
"""

from connection import client
from bson.objectid import ObjectId
from model.mongo_model.write_cache import insert_cache


class DailyReportDB(object):
    """每日报表操作封装"""

    def __init__(self, factory_id=None, equipment_id=None):
        super(DailyReportDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(equipment_id) + '_daily_report'
        self.db = self.client[self.db_name]
        self.collection = self.db[self.table_name]

    def insert(self, data):
        try:
            data['_id'] = ObjectId().__str__()
            self.collection.insert(data)
            # 插入缓存数据库
            insert_cache(self.db_name, self.table_name, 'insert', [data])
            return data['_id']
        except:
            return None

    # TODO 支持日期时间段查询，关键字查询
    def findall(self, number=None, page=None):
        try:
            result = self.collection.find({}, {"_id": 1, "name": 1}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def get_daily_rep_data(self, start_time, end_time, field):
        """
        从每日报表中提取指定时间段，字符的数据
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param field: 字段
        :return: 成功返回字段的集合
        """
        try:
            if field == "PhaseVin":
                pipe = [{'$match': {'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    'PhaseVinAB': {'$push': '$PhaseVinAB'},
                                    'PhaseVinBC': {'$push': '$PhaseVinBC'},
                                    'PhaseVinCA': {'$push': '$PhaseVinCA'}}}
                        ]
            elif field == "PhaseIin":
                pipe = [{'$match': {'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    'PhaseIinAB': {'$push': '$PhaseIinAB'},
                                    'PhaseIinBC': {'$push': '$PhaseIinBC'},
                                    'PhaseIinCA': {'$push': '$PhaseIinCA'}}}
                        ]
            elif field == "Temperature":
                pipe = [{'$match': {'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    'Temperature1': {'$push': '$Temperature1'},
                                    'Temperature2': {'$push': '$Temperature2'}}}
                        ]
            else:
                pipe = [{'$match': {'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    field: {'$push': '$' + field}}}
                        ]

            data = self.collection.aggregate(pipeline=pipe)
            return list(data)
        except:
            return None

    def get_daily_rep_dict(self, start_time, end_time, field):
        """
        从每日报表中提取指定时间段，字符的数据
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param field: 字段
        :return: 成功返回字段的字典
        """
        try:
            if field == "PhaseVin":
                filter_cond = {"PhaseVinAB": 1, "PhaseVinBC": 1, "PhaseVinBA": 1, 'data': 1}
            elif field == "PhaseIin":
                filter_cond = {"PhaseIinAB": 1, "PhaseIinBC": 1, "PhaseIinCA": 1, 'data': 1}
            elif field == "Temperature":
                filter_cond = {"Temperature1": 1, "Temperature2": 1, 'data': 1}
            else:
                filter_cond = {field: 1, 'data': 1}
            result = self.collection.find(
                {'date': {"$gte": start_time, "$lte": end_time}}, filter_cond)
            return list(result)
        except:
            return None

    def close(self):
        self.client.close()
