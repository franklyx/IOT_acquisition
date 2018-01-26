#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.user
~~~~~~~~~~~~

定义所有用户的api请求的handler
为用户提供增删改查，以及后台提供获取所有用户列表的接口
"""

from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.user import UserDB
from basic import check_token, check_role_one, check_token_and_type


class User(BasicCtrl):
    """用户接口"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过用户id获取该用户的详细信息的json
        :param args:
        :param kwargs: /user_id
        :return: 成功返回用户详细信息的json，未找到该用户返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        user_id = kwargs['user_id']
        if user_id:
            user_obj = UserDB()
            result = user_obj.find(user_id)
            user_obj.close()
            if result:
                SpiderApi.response(200)
                self.write_json(result)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)

    @check_token_and_type
    @check_role_one
    def post(self, *args, **kwargs):
        """
        post请求，单机版添加用户，并绑定用户所属公司
        :param args:
                name: 工厂名称
                role: 角色
                password: 密码
                factory_id: 所属工厂id
        :param kwargs:
        :return: 成功返回201和用户的id,未能成功插入返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        request_data = kwargs['request_data']
        name = request_data.get('name')
        role = request_data.get('role')
        password = request_data.get('password')
        factory_id = request_data.get('factory_id')
        if name and role and password and factory_id:
            user_obj = UserDB()
            # 用户名唯一性检测
            uniqueness = user_obj.find(username=name)
            if uniqueness:
                raise HTTPError(**errors.status_33)
            result = user_obj.insert(username=name, user_role=int(role), password=password,
                                     factory_id=factory_id)
            user_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)

    @check_token_and_type
    @check_role_one
    def put(self, *args, **kwargs):
        """
        put请求，通过工厂id,用户id,和修改的信息，更新用户列表
        工厂id默让不让修改
        :param args:
                name: 用户名
                role: 角色
                password: 密码
        :param kwargs: /user_id
        :return: 成功返回200和修改的用户的id,未找到对象返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        user_id = kwargs['user_id']
        request_data = kwargs['request_data']
        name = request_data.get('name')
        role = request_data.get('role')
        password = request_data.get('password')
        if user_id and name and role and password:
            user_obj = UserDB()
            result = user_obj.update(user_id, username=name, password=password,
                                     user_role=role)
            user_obj.close()
            if result:
                SpiderApi.response(200)
                self.write_json(result)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)

    @check_token
    @check_role_one
    def delete(self, *args, **kwargs):
        """
        delete请求,通过用户id,直接删除用户
        :param args:
        :param kwargs: /user_id
        :return: 成功返回204,未找到返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        user_id = kwargs['user_id']
        if user_id:
            user_obj = UserDB()
            result = user_obj.remove(id=user_id)
            user_obj.close()
            if result:
                SpiderApi.response(204)
                self.write_json(None, 204)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class Basic_inform_modification(BasicCtrl):
    """用户基本信息修改"""

    @check_token_and_type
    def put(self, *args, **kwargs):
        """
        put请求，用户通过该接口直接修改基本信息
        通过解析传递过来的token中的用户id和修改的用户id做对比，相同才能够然他修改
        该接口只能修改用户名和密码
        :param args:
                name: 用户名
                password: 密码
        :param kwargs: /user_id
        :return: 成功返回用户id和200，未找到对象返回status_24
                 参数错误返回status_22, 不是修改自己的信息返回status_29
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        user_id = kwargs['user_id']
        if kwargs['c_user_id'] == user_id:
            request_data = kwargs['request_data']
            name = request_data.get('name')
            password = request_data.get('password')
            if user_id and name and password:
                user_obj = UserDB()
                # 用户名唯一性检测
                uniqueness = user_obj.find(username=name)
                if uniqueness:
                    raise HTTPError(**errors.status_33)
                result = user_obj.update(user_id, username=name, password=password)
                user_obj.close()
                if result:
                    SpiderApi.response(200)
                    self.write_json(result)
                else:
                    SpiderApi.response(errors.status_24)
                    raise HTTPError(**errors.status_24)
            else:
                SpiderApi.response(errors.status_22)
                raise HTTPError(**errors.status_22)
        else:
            SpiderApi.response(errors.status_29)
            raise HTTPError(**errors.status_29)


class UserList(BasicCtrl):
    @check_token_and_type
    @check_role_one
    def post(self, *args, **kwargs):
        """
        post请求，获取用户列表
        :param args:
                page: 第几页
                per_page: 每页显示页数
        :param kwargs:
        :return: 成功返回201和用户列表，未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        request_data = kwargs['request_data']
        page = request_data.get('page')
        per_page = request_data.get('per_page')
        if page and per_page:
            limit = int(per_page)
            offset = (int(page) - 1) * limit
            user_obj = UserDB()
            result = user_obj.findall(offset, limit)
            user_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
