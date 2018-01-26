#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.workschedule
~~~~~~~~~~~~~~~~~~~~

定义所有班次的api请求handler
为生产线提供增删改查以及后台获取所有的班次接口
"""
from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from basic import check_token, check_role_one, check_token_and_type
from model.mongo_model.workschedule import WorkScheduleDB


class WorkSchedule(BasicCtrl):
    """班次接口"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求: 通过工厂id和班次id获取班次的详细信息
        :param args:
        :param kwargs: /factory_id/schedule_id
        :return: 成功返回班次的信息，未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            schedule_id = parameter_list[1]
            schedule_obj = WorkScheduleDB(factory_id=factory_id)
            result = schedule_obj.find(id=schedule_id)
            schedule_obj.close()
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
        post:通过工厂id和班组的详细信息，添加班次信息
        :param args:
                group_id: 班组信息
                start_time: 开始时间
                end_time: 结束时间
                name: 班次名称
        :param kwargs: /factory_id/
        :return: 成功返回插入的班次id和201,插入失败返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        group_id = request_data.get('group_id')
        start_time = request_data.get('start_time')
        end_time = request_data.get('end_time')
        name = request_data.get('name')
        if len(parameter_list) == 2 and group_id and start_time and end_time and name:
            factory_id = parameter_list[0]
            schedule_obj = WorkScheduleDB(factory_id=factory_id)
            result = schedule_obj.insert(group_id=group_id, start_time=start_time,
                                         end_time=end_time, name=name)
            schedule_obj.close()
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
        put请求，通过工厂id和班次id和需要更新的参数，更新班次
        :param args:
                group_id: 班组信息
                start_time: 开始时间
                end_time: 结束时间
                name: 班次名称
        :param kwargs: /factory_id/schedule_id
        :return: 成功返回更新的设备id,未找到班次返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        group_id = request_data.get('group_id')
        start_time = request_data.get('start_time')
        end_time = request_data.get('end_time')
        name = request_data.get('name')
        if len(parameter_list) == 2 :
            factory_id = parameter_list[0]
            schedule_id = parameter_list[1]
            schedule_obj = WorkScheduleDB(factory_id=factory_id)
            result = schedule_obj.update(id=schedule_id, group_id=group_id, start_time=start_time,
                                         end_time=end_time, name=name)
            schedule_obj.close()
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
        delete请求：通过factory_id和schedule_id，删除班次
        :param args:
        :param kwargs: /factory_id/schedule_id
        :return: 成功返回204,未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            schedule_id = parameter_list[1]
            schedule_obj = WorkScheduleDB(factory_id=factory_id)
            result = schedule_obj.remove(id=schedule_id)
            schedule_obj.close()
            if result:
                SpiderApi.response(204)
                self.write_json(None, 204)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class WorkScheduleList(BasicCtrl):
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求:通过工厂id,获取该工厂下所有的班次信息
        :param args:
                page: 第几页
                per_page: 每页显示的条数
        :param kwargs: /factory_id
        :return: 成功返回班次详细信息列表和201，未找到班次信息返回status_24
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
            schedule_obj = WorkScheduleDB(factory_id=factory_id)
            result = schedule_obj.findall(factory_id, offset, limit)
            schedule_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
