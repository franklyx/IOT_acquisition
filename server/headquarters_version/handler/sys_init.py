#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.sys_init
~~~~~~~~~~~~~~~~

定义系统初始化的handler
实现系统初始化判断和初始化管理员的接口
"""
from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.cfgparser import parser
from handler.basic import check_sys_init
from model.mongo_model.user import UserDB
from model.mongo_model.factory import FactoryDB
from tools.jwt_serializer import genTokenSeq, genRfTokenSeq


class SysInit(BasicCtrl):
    """判断系统是否初始化，已经初始化返回True,未初始化返回False"""

    def get(self, *args, **kwargs):
        init_factory_id = parser.factoryid
        result = FactoryDB().find(id=init_factory_id)
        if result:
            self.write_json('True')
        else:
            self.write_json('False')


class InitAdmin(BasicCtrl):
    """ 当系统未进行初始化的时候,来添加管理员
        并返回token和rf_token
    """

    @check_sys_init
    def post(self, *args, **kwargs):
        request_data = kwargs['request_data']
        name = request_data.get('username')
        password = request_data.get('password')
        if name and password:
            factory_id = kwargs['c_factory_id']
            role = 1
            user_obj = UserDB()
            # 用户名唯一性检测
            uniqueness = user_obj.find(username=name)
            if uniqueness:
                raise HTTPError(**errors.status_33)
            result = user_obj.insert(username=name, user_role=role, password=password,
                                     factory_id=factory_id)
            if result:
                token = genTokenSeq(result, role, 7200)
                rf_token = genRfTokenSeq(result, role, 108000)
                self.write_json({'token': token, 'rf_token': rf_token, 'role': role}, 201)
            else:
                raise HTTPError(**errors.status_31)
        else:
            raise HTTPError(**errors.status_22)
