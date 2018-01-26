#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
urls.backend
~~~~~~~~~~~~

后台api接口的handler
"""
from handler.user import UserList
from handler.factory import FactoryList
from handler.workshop import WorkshopList
from handler.equipment import EquipmentList
from handler.workgroup import WorkGroupList
from handler.product_line import ProductLineList, LineListForShop
from handler.workschedule import WorkScheduleList

backend_handler = [

    ('/api/v1/list/user', UserList),
    ('/api/v1/list/factory', FactoryList),
    ('/api/v1/list/work-shop/(?P<factory_id>.*)', WorkshopList),
    ('/api/v1/list/product-line/(?P<factory_id>.*)', ProductLineList),
    ('/api/v1/list/equipment/(?P<factory_id>.*)', EquipmentList),
    ('/api/v1/list/work-group/(?P<factory_id>.*)', WorkGroupList),
    ('/api/v1/list/work-schedule/(?P<factory_id>.*)', WorkScheduleList),
    ('/api/v1/list/line-under-shop/(?P<parameter>.*)', LineListForShop)
]
