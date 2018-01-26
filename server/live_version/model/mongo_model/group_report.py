#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.group_report
~~~~~~~~~~~~~~~~~~~~~~

封装了对后台生成的班组报告的操作
提供插入和查找的接口
"""

from connection import client
from bson.objectid import ObjectId
from model.mongo_model.write_cache import insert_cache


class GroupReportDB(object):
    """操作班组报表"""

    def __init__(self, factory_id=None, equipment_id=None):
        super(GroupReportDB, self).__init__()
        self.dict = {}
        self.client = client
        self.db_name = str(factory_id)
        self.table_name = str(equipment_id) + '_group_report'
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

    # TODO 支持班组记录查询
    def findall(self, number=None, page=None):
        try:
            result = self.collection.find({}, {"_id": 1, "name": 1}).skip(number).limit(page)
            return list(result)
        except:
            return None

    def get_daily_report(self, equipment_id, date):
        """
        从班次报表中求平均值，整合生成每日报表
        :param equipment_id: 设备id
        :param date: 日期
        :return: 统计出来的信息字典
        """
        try:
            pipe = [{'$match': {'equipment_id': equipment_id,
                                "date": date}},
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

    def get_group_rep_data(self, group_id, start_time, end_time, field):
        """
        从班组报表中提取指定时间段，字符的数据
        :param group_id: 班组id
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param field: 字段
        :return: 成功返回字段的集合
        """
        try:
            if field == "PhaseVin":
                pipe = [{'$match': {'work_group_id': group_id,
                                    'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    'PhaseVinAB': {'$push': '$PhaseVinAB'},
                                    'PhaseVinBC': {'$push': '$PhaseVinBC'},
                                    'PhaseVinCA': {'$push': '$PhaseVinCA'}}}
                        ]
            elif field == "PhaseIin":
                pipe = [{'$match': {'work_group_id': group_id,
                                    'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    'PhaseIinAB': {'$push': '$PhaseIinAB'},
                                    'PhaseIinBC': {'$push': '$PhaseIinBC'},
                                    'PhaseIinCA': {'$push': '$PhaseIinCA'}}}
                        ]
            elif field == "Temperature":
                pipe = [{'$match': {'work_group_id': group_id,
                                    'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    'Temperature1': {'$push': '$Temperature1'},
                                    'Temperature2': {'$push': '$Temperature2'}}}
                        ]
            else:
                pipe = [{'$match': {'work_group_id': group_id,
                                    'date': {"$gte": start_time, "$lte": end_time}
                                    }},
                        {"$group": {'_id': None,
                                    'DateTime': {'$push': '$date'},
                                    field: {'$push': '$' + field}}}
                        ]

            data = self.collection.aggregate(pipeline=pipe)
            return list(data)
        except:
            return None

    def close(self):
        self.client.close()
