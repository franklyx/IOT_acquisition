#!/usr/bin/env python
# -*- coding:utf-8 -*-

# from model.mongo_model.producte_data import ProductData
from model.mongo_model.workschedule import WorkScheduleDB

data = {
    "Timestamp": "2017-02-21 22:30:21",
    "ManufacturingCode": "2323232",
    "ManufacturingDate": "2016-05-30",
    "ProductModel": "NSINE03-3932-38923",
    "State": 2,
    "PhaseVoltageInput": 1,
    "LineVin": 220.0,
    "LineIin": 120.0,
    "PhaseVinAB": 380.0,
    "PhaseVinBC": 380.0,
    "PhaseVinCA": 380.0,
    "PhaseIinAB": 100.0,
    "PhaseIinBC": 100.0,
    "PhaseIinCA": 100.0,
    "InputPower": 120.0,
    "DCVout": 60.0,
    "DCIout": 200.0,
    "OutputPower": 120.0,
    "EfficiencyRatio": 0.89,
    "GasFlow": 100.99,
    "Temperature1": 100.0,
    "Temperature2": 100.0,
    "OCAlarm": 1,
    "OVAlarm": 1,
    "AlarmCode": "ada989128983209432"}

# obj = ProductData(factory_number='2323232', factory_id='59634a825751360333139093')
# # for i in range(50):
# #     obj.insert(data=data)
# #
# obj.get_group_report(1, 1)

# print WorkScheduleDB(factory_id='59634a825751360333139093').find(group_id='597af700e9b5b30235cb8b67')

# from model.redis_model.filter_id import FilterId
#
# print FilterId().find('782ABC292320')
