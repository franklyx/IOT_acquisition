#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
handler.equipment
~~~~~~~~~~~~~~~~~

定义所有设备信息数据的api请求handler
通过api实现获取设备的实时信息，报警信息，历史信息和报表信息
"""
from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.alarm_data import AlarmData
from basic import check_token,check_token_and_type
from model.redis_model.latest_equip_info import LatestEquipInfoDB


class RealTimeData(BasicCtrl):
    """获取设备的实时信息"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过设备id获取设备存储在redis的最新信息
        :param args:
        :param kwargs:/equipment_id
        :return: 成功返回200和设备信息的json,未找到信息返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        equipment_id = kwargs['equipment_id']
        if equipment_id:
            real_obj = LatestEquipInfoDB()
            result = real_obj.find(equipment_id)
            if result:
                SpiderApi.response(200)
                self.write_json(result)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class AlarmInfo(BasicCtrl):
    """获取设备的警告信息"""

    # TODO 根据前端信息返回需要的字段，不要全部返回
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过设备id和工厂id获取设备的警告信息
        :param args:
                page: 第几页
                per_page: 每页显示几条记录
        :param kwargs: /factory_id/equipment_id
        :return: 成功返回201以及包含警报信息的json,为请求到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        page = request_data.get('page')
        per_page = request_data.get('per_page')
        if len(parameter_list) == 2 and page and per_page:
            limit = int(per_page)
            offset = (int(page) - 1) * limit
            factory_id = parameter_list[0]
            equipment_id = parameter_list[1]
            alarm_obj = AlarmData(equip_id=equipment_id, factory_id=factory_id)
            result = alarm_obj.findall(number=offset, page=limit)
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class HistoryInfo(BasicCtrl):
    """获取设备的历史信息"""

    @check_token
    def get(self, *args, **kwargs):
        pass


class ReportInfo(BasicCtrl):
    """获取设备的中间表报信息"""

    @check_token
    def get(self, *args, **kwargs):
        pass
