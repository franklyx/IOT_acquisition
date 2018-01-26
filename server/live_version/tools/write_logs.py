#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
tools.write_logs
~~~~~~~~~~~~~~~~

实现对日志文件写入方法的封装
目的: 让代码看上去更加的整简，减少大量冗余代码
"""

import logging

spider_api = logging.getLogger('spider_api')
spider_flow = logging.getLogger('spider_flow')


class SpiderApi(object):
    """api日志的写入封装"""

    @classmethod
    def request(cls, who, ip, method, uri):
        """
        当有请求访问时，讲访问的细节记录到日志文件中
        :param who: 访问者用户id
        :param ip: 访问者ip地址
        :param method: 访问使用的请求方法
        :param uri: 访问的具体地址
        :return:
        """
        original_str = "Request access： {0} by {1} send {2} request access {3}"
        spider_api.info(original_str.format(who, ip, method, uri))

    @classmethod
    def response(cls, data):
        """
        当完成请求的响应后，将响应信息记录到日志文件中
        :param data: 记录响应的结果
        :return:
        """
        original_str = "Return the content: {}"
        spider_api.info(original_str.format(data))


class SpiderFlow(object):
    """flow(数据库)日志的写入封装"""

    @classmethod
    def operate(cls, who, ip, requirement, old_data):
        """
        当对数据库进行操作时，将数据的改动进行记录
        :param who: 操作者id
        :param ip: 操作者ip
        :param requirement: 操作的方法和条件
        :param old_data: 删除修改的原数据
        :return:
        """
        original_str = "Operation starts： {0} by {1} performing operation:{2}, old_data: {3}"
        logging.info(original_str)
        spider_flow.info(original_str.format(who, ip, requirement, old_data))

    @classmethod
    def result(cls, data):
        """
        数据库操作完成后，将结果记录日志
        :param data: 数据库返回结果
        :return:
        """
        original_str = "End of operation：{}"
        spider_flow.info(original_str.format(data))
