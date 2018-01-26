#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
tools.report_filter
~~~~~~~~~~~~~~~~~~~

中间表处理过程中需要用到的常见运算
"""

# 定义中间表处理的项
FILTER_RULES = (
    'Avg_State', 'Avg_PhaseVoltageInput', 'Avg_LineVin', 'Avg_LineIin', 'Avg_PhaseVinAB',
    'Avg_PhaseVinBC', 'Avg_PhaseVinCA', 'Avg_PhaseIinAB', 'Avg_PhaseIinBC', 'Avg_PhaseIinCA',
    'Avg_InputPower', 'Avg_DCVout', 'Avg_DCIout', 'Avg_EfficiencyRatio', 'Avg_GasFlow',
    'Avg_Temperature1', 'Avg_Temperature2', 'Avg_OCAlarm', 'Avg_OVAlarm')


def dict_multi(datas):
    """
    将列表中字典的指定项乘以指定的因子
    :param datas: 需要处理的字典列表
    :return: 成功返回处理后的字典列表
    """
    for data in datas:
        for k, v in data.items():
            if k in FILTER_RULES:
                data[k] = v * data['num']
    return datas


def dict_add_merge(datas):
    """
    将列表中的指定字典进行相加合并，生成一个字典
    :param datas: 需要处理的字典列表
    :return: 成功返回处理后的字典
    """
    dict_first = datas[0:1]  # 取字典列表中的第一个字典
    if datas[1:]:
        for data in datas[1:]:
            for k, v in data.items():
                if k in FILTER_RULES:
                    dict_first[0][k] += v
        return dict_first[0]
    else:
        return dict_first[0]


def dict_division(data, num):
    """
    将字典中的特定项除以指定值
    :param data: 字典
    :param num: 被除数
    :return: 成功返回处理后的字典
    """
    for k, v in data.items():
        if k in FILTER_RULES:
            data[k] = v / num
    return data
