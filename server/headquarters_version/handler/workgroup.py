#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.workgroup
~~~~~~~~~~~~~~~~~

定义所有班组的api请求handler
为班组提供增删改查以及为后台提供获取所有班组信息的接口
"""
import json

from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.workgroup import WorkGroupDB
from model.mongo_model.workschedule import WorkScheduleDB
from basic import check_token, check_role_one, check_token_and_type


class WorkGroup(BasicCtrl):
    """班组接口"""

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过工厂id和生产线id获取生产线的json信息
        :param args:
        :param kwargs: /factory_id/group_id
            :return: 成功返回200和班组的json信息,未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            group_id = parameter_list[1]
            group_obj = WorkGroupDB(factory_id=factory_id)
            result = group_obj.find(id=group_id)
            group_obj.close()
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
        post请求,通过工厂id和班组名称，添加班组
        :param args: 利用(application/json)传递
                name: 班组名称
                equipment_list: 设备列表
        :param kwargs: /factory_id/
        :return: 成功返回201和班组的json信息，未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        name = request_data.get('name')
        equipment_list = request_data.get('equipment_list')
        if len(parameter_list) == 2 and name and isinstance(equipment_list, list):
            factory_id = parameter_list[0]
            group_obj = WorkGroupDB(factory_id=factory_id)
            result = group_obj.insert(name=name, equipment_list=equipment_list)
            group_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_24)
            raise HTTPError(**errors.status_22)

    @check_token_and_type
    @check_role_one
    def put(self, *args, **kwargs):
        """
        put请求,通过工厂id和班组id,和需要修改的信息，更新班组
        :param args: 利用(application/json)传递
                name: 班组名称
        :param kwargs: /factory_id/group_id
        :return: 成功返回200和班组id,未找到班组返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        name = request_data.get('name')
        equipment_list = request_data.get('equipment_list')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            group_id = parameter_list[1]
            group_obj = WorkGroupDB(factory_id=factory_id)
            result = group_obj.update(id=group_id, name=name, equipment_list=equipment_list)
            group_obj.close()
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
        delete请求，通过工厂id和班组id,删除班组信息，
        删除班组信息的时候要删除班次中包含班组的记录设置为None
        :param args:
        :param kwargs: /factory_id/group_id
        :return: 成功返回204，未找到班组返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            group_id = parameter_list[1]
            group_obj = WorkGroupDB(factory_id=factory_id)
            result = group_obj.remove(id=group_id)
            schedule_obj = WorkScheduleDB(factory_id=factory_id)
            result1 = schedule_obj.set_none_for_groupid(group_id=group_id)
            group_obj.close()
            schedule_obj.close()
            if result and result1:
                SpiderApi.response(204)
                self.write_json(None, 204)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class WorkGroupList(BasicCtrl):
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过工厂id获取该工厂下所有的班组信息
        :param args:
                page: 第几页
                per_page: 每页显示的个数
        :param kwargs: /factory_id
        :return: 成功返回班组列表，未找到班组信息返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_id = kwargs['factory_id']
        request_data = kwargs['request_data']
        page = request_data.get('page')
        per_page = request_data.get('per_page')
        if factory_id and page and per_page:
            limit = int(per_page)
            offset = (int(page) - 1) * limit
            group_obj = WorkGroupDB(factory_id=factory_id)
            result = group_obj.findall(offset, limit)
            group_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
