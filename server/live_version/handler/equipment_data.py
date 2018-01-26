#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
handler.equipment
~~~~~~~~~~~~~~~~~

定义所有设备信息数据的api请求handler
通过api实现获取设备的实时信息，报警信息，历史信息和报表信息
"""
import calendar
import datetime

from tornado.web import HTTPError

from handler import errors
from basic import BasicCtrl
from tools.write_logs import SpiderApi
from model.mongo_model.alarm_data import AlarmData
from basic import check_token, check_token_and_type
from model.mongo_model.producte_data import ProductData
from model.mongo_model.group_report import GroupReportDB
from model.mongo_model.workschedule import WorkScheduleDB
from model.mongo_model.daily_report import DailyReportDB
from model.redis_model.latest_equip_info import LatestEquipInfoDB

# 定义历史查询，允许查询的参数
ALLOWED_PARA = (
    'State', 'PhaseVoltageInput', 'LineVin', 'LineIin', 'PhaseVin', 'PhaseIin', 'InputPower',
    'DCVout', 'DCIout', 'EfficiencyRatio', 'GasFlow', 'Temperature', 'OCAlarm', 'OVAlarm')


class RealTimeData(BasicCtrl):
    """获取设备的实时信息"""

    def data_received(self, chunk):
        pass

    @check_token
    def get(self, *args, **kwargs):
        """
        get请求，通过设备编号获取设备存储在redis的最新信息
        :param args:
        :param kwargs: /factory_number
        :return: 成功返回200和设备信息的json,未找到信息返回status_24
                 参数错误返回status_22
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        factory_number = kwargs['factory_number']
        if factory_number:
            real_obj = LatestEquipInfoDB()
            result = real_obj.find(factory_number)
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
        post请求，通过设备编号和工厂id获取设备的警告信息
        :param args:
                page: 第几页
                per_page: 每页显示几条记录
        :param kwargs: /factory_id/factory_number
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
            factory_number = parameter_list[1]
            alarm_obj = AlarmData(factory_number=factory_number, factory_id=factory_id)
            result = alarm_obj.findall(factory_number, number=offset, page=limit)
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

    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过设备编号和工厂id获取设备的历史信息
        :param args:
                group_id: 班组id ,全选为None
                start_time: 开始时间
                end_time: 结束时间
                search_field: 查找字段
                equipment_id: 设备id
        :param kwargs: /factory_id/factory_number
        :return: 成功返回201以及包含警报信息的json,为请求到数据返回status_24
                 参数错误返回status_22,设备未绑定班次返回status_38
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
        search_field = request_data.get('search_field')
        equipment_id = request_data.get('equipment_id')
        factory_id = parameter_list[0]
        factory_number = parameter_list[1]
        # 对查询的参数进行判断
        if search_field not in ALLOWED_PARA:
            SpiderApi.response(errors.status_37)
            raise HTTPError(**errors.status_37)
        if len(parameter_list) == 2 and start_time and end_time and search_field:
            # 对时间间隔进行处理
            start_time_list = map(int, start_time.split("-"))
            end_time_list = map(int, end_time.split("-"))
            start_datetime = datetime.datetime.combine(
                datetime.date(start_time_list[0], start_time_list[1], start_time_list[2]),
                datetime.time.min)
            end_datetime = datetime.datetime.combine(
                datetime.date(end_time_list[0], end_time_list[1], end_time_list[2]),
                datetime.time.min)
            # 读取中间表获取数据
            # 首先要对时间进行区间和是否选择班次进行判断 大于30天 去每日报表查找，小于30天，去生产数据查找
            time_interval = end_datetime - start_datetime
            if time_interval >= datetime.timedelta(30):
                if group_id:
                    # 去班组报表中查询
                    group_report_obj = GroupReportDB(factory_id=factory_id,
                                                     equipment_id=equipment_id)
                    result = group_report_obj.get_group_rep_data(group_id=group_id,
                                                                 start_time=start_datetime,
                                                                 end_time=end_datetime,
                                                                 field=search_field)
                    group_report_obj.close()
                else:
                    # 去每日报表查询
                    daily_report_obj = DailyReportDB(factory_id=factory_id,
                                                     equipment_id=equipment_id)
                    result = daily_report_obj.get_daily_rep_data(start_time=start_datetime,
                                                                 end_time=end_datetime,
                                                                 field=search_field)
                    daily_report_obj.close()
            else:
                # 获取班组绑定的班次
                schedule_obj = WorkScheduleDB(factory_id=factory_id)
                schedule = schedule_obj.find(group_id=group_id)
                schedule_obj.close()
                # 对查找的设备id进行校验,判断是否传班组id,判断是否绑定了班次
                if schedule is None and group_id:
                    SpiderApi.response(errors.status_38)
                    raise HTTPError(**errors.status_38)
                if group_id:
                    # 对时间进行处理
                    start_list = map(int, schedule['start_time'].split(":"))
                    end_list = map(int, schedule['end_time'].split(":"))
                    start_datetime += datetime.timedelta(hours=start_list[0],
                                                         minutes=start_list[1], microseconds=1)
                    end_datetime += datetime.timedelta(hours=end_list[0],
                                                       minutes=end_list[1], microseconds=1)
                # 去生产数据中查询，班次所绑定班次的记录
                product_data_obj = ProductData(factory_number=factory_number,
                                               factory_id=factory_id)
                result = product_data_obj.get_product_data(field=search_field,
                                                           start_time=start_datetime,
                                                           end_time=end_datetime)
                product_data_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)


class ReportInfo(BasicCtrl):
    """获取设备的表报信息"""

    @check_token_and_type
    def post(self, *args, **kwargs):
        """
        post请求，通过该接口能够查询设备在指定月份的报表信息
        :param args:
                date: 年月字符串
                search_field: 查找字段
        :param kwargs: /factory_id/equipment_id
        :return: 成功返回报表信息
        """
        # api日志记录
        SpiderApi.request(kwargs['c_user_id'], self.request.remote_ip, self.request.method,
                          self.request.uri)
        parameter = kwargs['parameter']
        parameter_list = parameter.split('/')
        request_data = kwargs['request_data']
        date = request_data.get('date')
        search_field = request_data.get('search_field')
        # 对查询的参数进行判断
        if search_field not in ALLOWED_PARA:
            SpiderApi.response(errors.status_37)
            raise HTTPError(**errors.status_37)
        if len(parameter_list) == 2 and date and search_field:
            factory_id = parameter_list[0]
            equipment_id = parameter_list[1]
            # 对传递过来的date时间字符串进行处理
            date_list = map(int, date.split("-"))
            year = date_list[0]
            month = date_list[1]
            start_datetime = datetime.datetime.combine(datetime.date(year, month, 1),
                                                       datetime.time.min)
            # 获取查询月的最后一天日期
            _, last_day_num = calendar.monthrange(year, month)
            end_datetime = datetime.datetime.combine(datetime.date(year, month, last_day_num),
                                                     datetime.time.min)
            # 从每日报表中获取查询的数据
            daily_report_obj = DailyReportDB(factory_id=factory_id,
                                             equipment_id=equipment_id)
            result = daily_report_obj.get_daily_rep_dict(start_time=start_datetime,
                                                         end_time=end_datetime,
                                                         field=search_field)
            daily_report_obj.close()
            if result:
                SpiderApi.response(201)
                self.write_json(result, 201)
            else:
                SpiderApi.response(errors.status_24)
                raise HTTPError(**errors.status_24)
        else:
            SpiderApi.response(errors.status_22)
            raise HTTPError(**errors.status_22)
