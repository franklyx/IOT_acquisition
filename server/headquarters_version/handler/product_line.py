#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.product_line
~~~~~~~~~~~~~~~~~~~~

定义所有设备生产线的api请求handler
为生产线提供增删改查以及后台的获取所有的设备生产线接口
"""
from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.equipment import EquipmentDB
from model.mongo_model.product_line import ProductLineDB
from basic import check_token, check_role_one,check_token_and_type


class ProductLine(BasicCtrl):
    """生产线接口"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过工厂id和生产线id获取生产线的json信息
        :param args:
        :param kwargs: /factory_id/product_line_id
        :return: 成功返回200和设备json信息，未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            product_line_id = parameter_list[1]
            product_line_obj = ProductLineDB(factory_id)
            result = product_line_obj.find(product_line_id)
            product_line_obj.close()
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
        post请求，通过工厂id和需要更新的信息，完成生产线的插入
        :param args:
                name: 生产线名称
                workshop_id: 所属车间
        :param kwargs: /factory_id/
        :return: 成功返回201和生产线id,未能成功插入数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        name = request_data.get('name')
        workshop_id = request_data.get('workshop_id')
        if len(parameter_list) == 2 and name and workshop_id:
            factory_id = parameter_list[0]
            product_line_obj = ProductLineDB(factory_id)
            result = product_line_obj.insert(name, workshop_id)
            product_line_obj.close()
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
        put请求，通过工厂id,生产线id和更新的数据，完成生产线的更新
        :param args:
                name: 生产线名称
                workshop_id: 所属车间id
        :param kwargs: /factory_id/product_line_id
        :return: 成功返回200和生产线id,未找到设备返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        name = request_data.get('name')
        workshop_id = request_data.get('workshop_id')
        if len(parameter_list) == 2 and name and workshop_id:
            factory_id = parameter_list[0]
            product_line_id = parameter_list[1]
            product_line_obj = ProductLineDB(factory_id)
            result = product_line_obj.update(product_line_id, name, factory_id, workshop_id)
            product_line_obj.close()
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
        delete请求，通过工厂id和生产线id,删除生产线,删除之前判断该生产线下是否还有设备
        :param args:
        :param kwargs: /factory_id/product_line_id/
        :return: 成功返回204和None，未找到数据返回status_24
                 参数错误返回status_22，该生产线下还有设备返回status_30
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        factory_id = parameter_list[0]
        product_line_id = parameter_list[1]
        equipment_obj = EquipmentDB(factory_id=factory_id)
        equipment_count = equipment_obj.get_counts_by_field('line_id', product_line_id)
        equipment_obj.close()
        if not equipment_count:
            if len(parameter_list) == 2:
                product_line_obj = ProductLineDB(factory_id)
                result = product_line_obj.remove(product_line_id)
                product_line_obj.close()
                if result:
                    SpiderApi.response(204)
                    self.write_json(None, 204)
                else:
                    SpiderApi.response(errors.status_24)
                    raise HTTPError(**errors.status_24)
            else:
                SpiderApi.response(errors.status_22)
                raise HTTPError(**errors.status_22)
        else:
            SpiderApi.response(errors.status_30)
            raise HTTPError(**errors.status_30)


class ProductLineList(BasicCtrl):
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过工厂id，获取工厂下的所有的生产线
        :param args:
                page: 第几页
                per_page: 每页显几条数据
        :param kwargs: /factory_id
        :return: 成功返回201和该工厂的生产线列表，未找到数据返回status_24
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
            product_line_obj = ProductLineDB(factory_id)
            limit = int(per_page)
            offset = (int(page) - 1) * limit
            result = product_line_obj.findall(offset, limit)
            product_line_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
