#!/usr/bin/env python
# coding:utf-8
"""
timing_task.tasks
~~~~~~~~~~~~~~~~~
用celery定义任务队列
包含如下任务
    1.中间表的生成
"""
import datetime

from celery import chord
from celery import shared_task

from tools.cfgparser import parser
from model.mongo_model.equipment import EquipmentDB
from model.mongo_model.producte_data import ProductData
from model.mongo_model.daily_report import DailyReportDB
from model.mongo_model.group_report import GroupReportDB
from model.mongo_model.workschedule import WorkScheduleDB
from model.mongo_model.workgroup import WorkGroupDB

GROUP_DATAS = list()  # 记录所有班组的中间表信息


def get_equipment_iter(factory_id):
    """
    遍历设备表获取包含该工厂的设备特定字段信息的列表
    :param factory_id: 工厂id
    :return: 成功返回该车间下的所有的设备id和出厂编号字典组成的列表
    """
    equipment_obj = EquipmentDB(factory_id=factory_id)
    equipment_iter = equipment_obj.get_id_and_number()
    return list(equipment_iter)


def get_schedule_list(factory_id):
    """
    根据该工厂中的work_schedule获取班组的安排信息
    :param factory_id: 工厂id
    :return: 成功返回班组的安排信息，包含班组，班次，时间段的迭代器
    """
    result = []
    schedule_obj = WorkScheduleDB(factory_id=factory_id)
    schedule_iter = schedule_obj.get_group_and_schedule()
    workgroup_obj = WorkGroupDB(factory_id=factory_id)
    for schedule in schedule_iter:
        schedule['group_name'] = workgroup_obj.find(schedule['group_id'])["name"]
        result.append(schedule)
    return result


def report_insert(factory_id):
    """
    回调函数实现数据的插入
    :param factory_id: 工厂id
    :return: 插入班组报表和每日报表
             班组报表格式: str(equipment_id) + '_group_report'
             每日报表格式: str(equipment_id) + '_daily_report'
    """

    # 实现班组的报表的插入
    equipment_id_set = set()
    global GROUP_DATAS
    for data in GROUP_DATAS:
        equipment_id = data[0]['equipment_id']
        equipment_id_set.add(equipment_id)
        group_report_obj = GroupReportDB(factory_id=factory_id,
                                         equipment_id=equipment_id)
        group_report_obj.insert(data[0])
        group_report_obj.close()
    # 删除临时保存数据库的字典
    del GROUP_DATAS
    # 实现每日报表数据的插入
    for equipment_id in equipment_id_set:
        # 取前一天的时间凌晨时间
        after_days = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=1),
                                               datetime.time.min)
        group_report_obj = GroupReportDB(factory_id=factory_id,
                                         equipment_id=equipment_id)
        daily_report_list = group_report_obj.get_daily_report(equipment_id=equipment_id,
                                                              date=after_days)
        if daily_report_list:
            daily_report_obj = DailyReportDB(factory_id=factory_id, equipment_id=equipment_id)
            daily_report_list[0]['date'] = after_days
            daily_report_obj.insert(daily_report_list[0])
            daily_report_obj.close()
        group_report_obj.close()


@shared_task
def report(factory_id, equipment, schedule):
    """
    生成报表celery任务
    根据设备id 以及时间段在product_data表中获取所有的记录(插入时根据设备出厂编号和时间进行查询)
    :param factory_id: 工厂id
    :param equipment: 包含设备id和出厂编号的设备字典
    :param schedule:  包含班组，班次，时间段的班次字典
    :return:
    """

    factory_number = equipment['factory_number']
    product_obj = ProductData(factory_number=factory_number, factory_id=factory_id)
    # 取前一天的时间凌晨时间
    after_days = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=1),
                                           datetime.time.min)
    # 对时间间隔进行处理
    start_time = map(int, schedule['start_time'].split(":"))
    end_time = map(int, schedule['end_time'].split(":"))
    date_start = after_days + datetime.timedelta(hours=start_time[0],
                                                 minutes=start_time[1], microseconds=1)
    end_start = after_days + datetime.timedelta(hours=end_time[0],
                                                minutes=end_time[1], microseconds=1)
    # 这里记得将结果从列表中解析出来
    group_data = product_obj.get_group_report(start_time=date_start,
                                              end_time=end_start)
    if group_data:
        group_data[0]['work_group'] = schedule['group_name']
        group_data[0]['work_group_id'] = schedule['group_id']
        group_data[0]['work_schedule'] = schedule['name']
        group_data[0]['work_schedule_id'] = schedule['_id']
        group_data[0]['start_time'] = schedule['start_time']
        group_data[0]['end_time'] = schedule['end_time']
        group_data[0]['equipment_id'] = equipment['_id']
        group_data[0]['date'] = after_days
        GROUP_DATAS.append(group_data)  # 将结果保存起来
    product_obj.close()


@shared_task
def main():
    """中间表生成的入口函数"""
    factory_id = parser.factoryid
    equipment_iter = get_equipment_iter(factory_id)
    schedule_iter = get_schedule_list(factory_id=factory_id)
    # 执行完所有队列任务后设置一个回调函数，执行中间表的插入
    # 利用列表推到计算出说有任务对象
    report_task = [(equipment, schedule) for equipment in equipment_iter for schedule in
                   schedule_iter]
    res = chord(
        (report.s(factory_id, task) for task in report_task), report_insert(factory_id))()
    # for task in report_task:
    #     report(factory_id, *task)
    # report_insert(factory_id=factory_id)


