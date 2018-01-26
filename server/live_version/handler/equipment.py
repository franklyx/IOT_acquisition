#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
handler.equipment
~~~~~~~~~~~~~~~~~

定义处理关于设备的API请求的handler
通过api接口实现设备的增删改查，以及为后台管理提供获取所有设备的接口
"""

from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.equipment import EquipmentDB
from model.mongo_model.workgroup import WorkGroupDB
from basic import check_token, check_role_one, check_token_and_type


class Equipment(BasicCtrl):
    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过设备id和工厂id获取该设备详细信息接口
        :param args:
        :param kwargs: /factory_id/equipment_id
        :return: 成功返回200和设备信息的json,未找到设备返回status_24
                 传参错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            equipment_id = parameter_list[1]
            equipment_obj = EquipmentDB(factory_id)
            result = equipment_obj.find(id=equipment_id)
            equipment_obj.close()
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
        # TODO 插入之前要判断出厂编号的唯一性
        """
        post请求，通过工厂ID和插入的设备详细插入设备: 插入之前要判断出厂编号的唯一性
        :param args:
                name: 设备名
                workshop_id: 工厂id
                line_id: 生产线id
                factory_number: 出厂编号
                factory_time: 出厂时间
                product_number: 产品型号
        :param kwargs: /factory_id/
        :return: 成功返回设备的id和201，未能成功插入返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        # 这里要记得切分字符串 不然连接数据库的时候会多'/'
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        name = request_data.get('name')
        workshop_id = request_data.get('workshop_id')
        line_id = request_data.get('line_id')
        factory_number = request_data.get('factory_number')
        factory_time = request_data.get('factory_time')
        product_number = request_data.get('product_number')
        factory_id = parameter_list[0]
        equipment_obj = EquipmentDB(factory_id)
        # 出厂编号唯一性验证
        count = equipment_obj.get_counts_by_field('factory_number', factory_number)
        if not count:
            if parameter_list and name and workshop_id and line_id and factory_number and factory_time and product_number:

                result = equipment_obj.insert(name, workshop_id, line_id, factory_number,
                                              factory_time,
                                              product_number)
                equipment_obj.close()
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
            SpiderApi.response(errors.status_36)
            raise HTTPError(**errors.status_36)

    @check_token_and_type
    @check_role_one
    def put(self, *args, **kwargs):
        """
        put请求，通过工厂和设备id以及需要修改的字段，更新设备信息
        :param args:
                name: 设备名
                workshop_id: 工厂id
                line_id: 生产线id
                factory_number: 出厂编号
                factory_time: 出厂时间
                product_number: 产品型号
        :param kwargs: /factory_id/equipment_id
        :return: 成功返回设备的id和200，未能成功插入返回status_24
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
        line_id = request_data.get('line_id')
        factory_number = request_data.get('factory_number')
        factory_time = request_data.get('factory_time')
        product_number = request_data.get('product_number')
        factory_id = parameter_list[0]
        equipment_id = parameter_list[1]
        equipment_obj = EquipmentDB(factory_id)
        if factory_number:
            # 先判断是否更新factory_number
            if factory_number != equipment_obj.find(id=equipment_id)['factory_number']:
                # 出厂编号唯一性验证
                count = equipment_obj.get_counts_by_field('factory_number', factory_number)
                if count:
                    SpiderApi.response(errors.status_36)
                    raise HTTPError(**errors.status_36)
        if len(parameter_list) == 2 and name and workshop_id and line_id and factory_number \
                and factory_time and product_number:
            result = equipment_obj.update(equipment_id, name, factory_id, workshop_id, line_id,
                                          factory_number, factory_time, product_number)
            equipment_obj.close()
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
        delete请求，通过设备id和工厂id删除指定设备
        删除设备的时候不需要检测该分类下是否还有子类，但是需要在班组的设备列表中删除该设备
        :param args:
        :param kwargs:/factory_id/equipment_id
        :return:成功返回204,未能成功删除返回status_24
                参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        if len(parameter_list) == 2:
            factory_id = parameter_list[0]
            equipment_id = parameter_list[1]
            equipment_obj = EquipmentDB(factory_id)
            workgroup_obj = WorkGroupDB(factory_id=factory_id)
            result = equipment_obj.remove(equipment_id)
            result1 = workgroup_obj.del_equipment_in_list(equipment_id)  # 在班组的设备列表中删除该设备
            equipment_obj.close()
            workgroup_obj.close()
            if result and result1:
                SpiderApi.response(204)
                self.write_json(None, status_code=204)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class EquipmentList(BasicCtrl):
    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过工厂id，页数和每页个数返回设备信息的列表
        :param args:
                page: 第几页
                per_page: 每页实现几条数据
        :param kwargs: /factory_id
        :return: 成功返回201和包含设备信息的列表，未请求到数据返回
                 status_24,参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_id = kwargs['factory_id']
        request_data = kwargs['request_data']
        page = request_data.get('page')
        per_page = request_data.get('per_page')
        if factory_id and page and per_page:
            equipment_obj = EquipmentDB(factory_id)
            limit = int(per_page)
            offset = (int(page) - 1) * limit
            result = equipment_obj.findall(offset, limit)
            equipment_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
