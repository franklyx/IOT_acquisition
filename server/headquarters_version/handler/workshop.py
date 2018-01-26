#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.workshop
~~~~~~~~~~~~~~~~

定义所有的车间的api请求的handler
为车间提供增删改查以及后台获取所有的车间接口
默认设置是不允许修改车间所属的工厂
"""
from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.workshop import WorkShopDB
from model.mongo_model.product_line import ProductLineDB
from basic import check_token, check_role_one, check_token_and_type


class Workshop(BasicCtrl):
    """车间接口"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过工厂id和车间id获取该车间的详细信息
        :param args:
        :param kwargs:  /factory_id/workshop_id
        :return: 成功返回车间的信息，未找到数据返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            workshop_id = parameter_list[1]
            workshop_obj = WorkShopDB(factory_id)
            result = workshop_obj.find(id=workshop_id)
            workshop_obj.close()
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
        post请求，通过工厂id和车间信息，写入车间信息
        :param args:
        :param kwargs: /factory_id/
        :return: 成功返回车间id和201，插入失败返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        name = request_data.get('name')
        if len(parameter_list) == 2 and name:
            factory_id = parameter_list[0]
            workshop_obj = WorkShopDB(factory_id)
            result = workshop_obj.insert(name)
            workshop_obj.close()
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
        put请求，通过工厂id和车间id,和修改的车间信息，更新车间
        :param args:
                name: 车间名称
        :param kwargs: /factory_id/workshop_id
        :return: 成功返回车间的id和200,未找到车间返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        request_data = kwargs['request_data']
        name = request_data.get('name')
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2 and name:
            factory_id = parameter_list[0]
            workshop_id = parameter_list[1]
            workshop_obj = WorkShopDB(factory_id)
            result = workshop_obj.update(workshop_id, name)
            workshop_obj.close()
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
        delete请求，通过工厂id和车间id,删除车间,删除之前要判断该车间下是否还有生产线
        :param args:
        :param kwargs: /factory_id/workshop_id
        :return: 成功返回204，未找到车间返回status_24
                 参数错误返回status_22,如果该车间下还有生产线则返回status_30
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        factory_id = parameter_list[0]
        workshop_id = parameter_list[1]
        pro_line_obj = ProductLineDB(factory_id=factory_id)
        pro_line_count = pro_line_obj.get_counts_by_field('workshop_id', workshop_id)
        pro_line_obj.close()
        if not pro_line_count:
            if len(parameter_list) == 2:
                workshop_obj = WorkShopDB(factory_id)
                result = workshop_obj.remove(workshop_id)
                workshop_obj.close()
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


class WorkshopList(BasicCtrl):
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过工厂id获取该工厂下的所有的车间列表
        :param args:
                page: 第几页
                per_page: 每页显示几条记录
        :param kwargs:  /factory_id
        :return: 成功返回该工厂的车间列表，未找到返回status_24
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
            workshop_obj = WorkShopDB(factory_id)
            limit = int(per_page)
            offset = (int(page) - 1) * limit
            result = workshop_obj.findall(offset, limit)
            workshop_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
