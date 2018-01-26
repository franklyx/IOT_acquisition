#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
handler.factory
~~~~~~~~~~~~~~~

定义所有关于工厂信息的api请求的handler
通过api实现工厂的增删改查，获取工厂列表和工厂的整个关系树型结构
"""

from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.factory import FactoryDB
from model.mongo_model.workshop import WorkShopDB
from model.mongo_model.equipment import EquipmentDB
from model.mongo_model.product_line import ProductLineDB
from basic import check_token, check_role_one,check_token_and_type


class Factory(BasicCtrl):
    """处理所有公司的API请求"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求,通过工厂id获取工厂的信息json
        :param args:
        :param kwargs: /factory_id
        :return: 成功返回200和设备信息的json,未找到设备信息返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_id = kwargs['parameter']
        if factory_id:
            factory_obj = FactoryDB()
            result = factory_obj.find(factory_id)
            factory_obj.close()
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
        post请求，通过工厂名字插入工厂数据, 单机版只能允许新建一个工厂
        :param args:
                name: 工厂名称
        :param kwargs:
        :return: 成功返回工厂id和201，未成功插入返回status_24
                 参数错误返回status_22,已经有一个工厂返回status_31
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_obj = FactoryDB()
        count = factory_obj.get_counts()
        request_data = kwargs['request_data']
        name = request_data.get('name')
        if not count:
            if name:

                result = factory_obj.insert(name=name)
                # 同步缓存写入
                factory_obj.close()
                if result:
                    SpiderApi.response(201)
                    self.write_json(result, 201)
                else:
                    SpiderApi.response(errors.status_24)
                    raise HTTPError(**errors.status_24)
            else:
                SpiderApi.response(errors.status_22)
                raise HTTPError(**errors.status_22)
        else:
            SpiderApi.response(errors.status_31)
            raise HTTPError(**errors.status_31)

    @check_token_and_type
    @check_role_one
    def put(self, *args, **kwargs):
        """
        put请求，通过工厂id和需要更新的数据
        :param args:
                name: 需要更新的工厂名称
        :param kwargs: /factory_id
        :return: 成功返回200和更新的工厂id，未找到工厂返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_id = kwargs['parameter']
        request_data = kwargs['request_data']
        name = request_data.get('name')
        if factory_id and name:
            factory_obj = FactoryDB()
            result = factory_obj.update(factory_id, name)
            # 同步缓存写入

            factory_obj.close()
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
        delete请求，通过工厂ID删除工厂,删除前需要做判断该工厂的车间数量是否为空
        :param args:
        :param kwargs: /factory_id
        :return: 成功返回204，未找到数据返回status_24
                 参数错误返回status_22,还存在子类返回status_30
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_id = kwargs['parameter']
        workshop_obj = WorkShopDB(factory_id=factory_id)
        workshop_count = workshop_obj.get_counts_by_field('factory_id', factory_id)
        workshop_obj.close()
        if not workshop_count:
            if id:
                factory_obj = FactoryDB()
                result = factory_obj.remove(factory_id)
                # 同步缓存写入

                factory_obj.close()
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


class FactoryList(BasicCtrl):
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，获取所有工厂的列表
        :param args:
                page: 第几页
                per_page: 每页显示几条数据
        :param kwargs:
        :return: 成功返回工厂列表和201,未找到工厂返回status_24
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
            factory_obj = FactoryDB()
            result = factory_obj.findall(offset, limit)
            factory_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class RelateTreeFactory(BasicCtrl):
    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过工厂id获取该工厂下的所有的工厂，生产线，设备，的层级关系树状图
        :param args:
        :param kwargs: /factory_id
        :return: 成功返回包含所有层级关系的列表,参数错误返回status_22
        """
        factory_id = kwargs['factory_id']
        if factory_id:
            workshop_obj = WorkShopDB(factory_id=factory_id)
            product_list_obj = ProductLineDB(factory_id=factory_id)
            equipment_obj = EquipmentDB(factory_id=factory_id)
            workshop_list = []  # 车间列表
            for workshop in workshop_obj.find(factory_id=factory_id):
                workshop_list.append(workshop)
                product_list = []  # 生产线列表
                for product_line in product_list_obj.find(workshop_id=workshop['_id']):
                    equipment_list = []  # 设备列表
                    for equipment in equipment_obj.find(line_id=product_line['_id']):
                        equipment_list.append(equipment)
                    product_line['equipment'] = equipment_list
                    product_list.append(product_line)
                workshop['product_line'] = product_list
                workshop_list.append(workshop)
            workshop_obj.close()
            product_list_obj.close()
            equipment_obj.close()
            self.write_json(workshop_list)
        else:
            raise HTTPError(**errors.status_22)
