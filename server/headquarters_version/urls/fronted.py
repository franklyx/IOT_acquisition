#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
urls.fronted
~~~~~~~~~~~~

前台api接口的handler
"""
from handler.user import User
from handler.posts import PostsCtrl
from handler.workshop import Workshop
from handler.equipment import Equipment
from handler.workgroup import WorkGroup
from handler.product_line import ProductLine
from handler.workschedule import WorkSchedule
from handler.user import Basic_inform_modification
from handler.factory import Factory, RelateTreeFactory
from handler.websocket import NewsSocketHandler, WebSocket
from handler.equipment_data import AlarmInfo, RealTimeData, HistoryInfo, ReportInfo

fronted_handler = [
    ('/', PostsCtrl),
    ('/api/v1/factory/(?P<parameter>.*)', Factory),
    ('/api/v1/user/(?P<user_id>.*)', User),
    ('/api/v1/user-inform/(?P<user_id>.*)', Basic_inform_modification),
    ('/api/v1/work-group/(?P<parameter>.*)', WorkGroup),
    ('/api/v1/work-schedule/(?P<parameter>.*)', WorkSchedule),
    ('/api/v1/work-shop/(?P<parameter>.*)', Workshop),
    ('/api/v1/equipment/(?P<parameter>.*)', Equipment),
    ('/api/v1/product-line/(?P<parameter>.*)', ProductLine),
    ('/api/v1/relate-tree/factory/(?P<factory_id>.*)', RelateTreeFactory),
    ('/api/v1/socket', WebSocket),
    ('/api/v1/join-socket', NewsSocketHandler),
    ('/api/v1/realtime-data/(?P<equipment_id>.*)', RealTimeData),
    ('/api/v1/alarm-data/(?P<parameter>.*)', AlarmInfo),

]
