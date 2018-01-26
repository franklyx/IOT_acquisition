#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.token
~~~~~~~~~~~~~

定义所有有关token的api请求handler
为token 提供生产token,rf_token的接口
以及通过tf_token更新token的接口
"""
import json

from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.cfgparser import parser
from tools.encryption import Encryption
from tools.write_logs import SpiderApi
from model.mongo_model.user import UserDB
from model.mongo_model.factory import FactoryDB
from tools.jwt_serializer import genTokenSeq, genRfTokenSeq, RftokenAuth


class Token(BasicCtrl):
    """生产token和rf_token的接口"""

    def post(self, *args, **kwargs):
        """
        post请求，通过用户名和密码获取token,rf_token以及用户的角色
        token的有效期为两小时，rf_token的有效期为30小时
        :param args:
                username: 用户名
                password: 密码
        :param kwargs:
        :return: 成功返回token,rf_token,role的json以及201,密码验证错误返回status_23
                 没有该用户返回status_26,缺少参数返回status_22
        """
        # 请求数据检查
        content_type = self.request.headers.get('Content-Type')
        if content_type != 'application/json':
            raise HTTPError(**errors.status_34)
        try:
            request_data = json.loads(self.request.body)
        except:
            raise HTTPError(**errors.status_35)
        username = request_data.get("username")
        password = request_data.get("password")
        # api日志记录
        SpiderApi.request(username, self.request.remote_ip, self.request.method,
                          self.request.uri)
        if username and password:
            user = UserDB().find(username=username)
            if user:
                encrypt_password = Encryption.generate_password(password, parser.auth_salt)
                if encrypt_password == user["password"]:
                    token = genTokenSeq(user["_id"], user["user_role"], 7200)
                    rf_token = genRfTokenSeq(user["_id"], user["user_role"], 108000)
                    SpiderApi.response(201)
                    # 获取工厂名称
                    factory_obj = FactoryDB()
                    factory_name = factory_obj.find(id=user["factory_id"])['name']
                    self.write_json(
                        {'token': token, 'rf_token': rf_token, 'role': user["user_role"],
                         'factory_id': user["factory_id"], "factory_name": factory_name,
                         "username": user['username'], "user_id": user["_id"]}, 201)
                else:
                    SpiderApi.response(errors.status_23)
                    raise HTTPError(**errors.status_23)
            else:
                SpiderApi.response(errors.status_26)
                raise HTTPError(**errors.status_26)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class RfToken(BasicCtrl):
    """根据rf_token更新token"""

    def post(self, *args, **kwargs):
        """
        post请求，通过rf_token获取最新的token值
        :param args:
                rf_token: 有效期为30小时的rf_token，用来获取最新的token
        :param kwargs:
        :return: 成功返回201和token的json,rf_token错误返回status_28
                 参数错误返回status_27
        """
        # 请求数据检查
        content_type = self.request.headers.get('Content-Type')
        if content_type != 'application/json':
            raise HTTPError(**errors.status_34)
        try:
            request_data = json.loads(self.request.body)
        except:
            raise HTTPError(**errors.status_35)
        rf_token = request_data.get("rf_token")
        # api日志记录
        SpiderApi.request(None, self.request.remote_ip, self.request.method,
                          self.request.uri)
        if rf_token:
            result = RftokenAuth(rf_token)
            if result[0] and result[1]:
                SpiderApi.response(201)
                self.write_json({'token': result[2]}, 201)
            else:
                SpiderApi.response(errors.status_28)
                raise HTTPError(**errors.status_28)
        else:
            SpiderApi.response(errors.status_27)
            raise HTTPError(**errors.status_27)
