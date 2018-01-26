#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
handler.websocket
~~~~~~~~~~~~~~~~~

通过websocket,向前端信息实时显示设备的报错信息
send_message方法实现向前端发送信息
"""
import logging

from tornado import gen
import tornado.websocket

from basic import BasicCtrl
from tools.jwt_serializer import tokenAuth


def send_message(message):
    """
    向前端定义发送接口
    :param message: 发送的信息
    :return:
    """
    for handler in NewsSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)


class NewsSocketHandler(tornado.websocket.WebSocketHandler):
    """websocket初始化操作"""

    socket_handlers = set()

    # 跨域修正
    def check_origin(self, origin):
        return True

    # 链接成功时触发
    def open(self):
        NewsSocketHandler.socket_handlers.add(self)

    # 链接端关闭时触发
    def on_close(self):
        NewsSocketHandler.socket_handlers.remove(self)

    # 发送数据时触发
    def on_message(self, token):
        if token:
            result = tokenAuth(token)
            if not (result[0] and result[1] is not None):
                self.close()
        else:
            self.close()


# TODO 报警信息推送的格式定义，只传递需要传递的信息

class WebSocket(BasicCtrl):
    """报警信息推送接口"""

    # @check_token_and_type
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        post请求，通过websocket向前端发送报警信息
        :param args:
                alarm_data: 警告设备的具体信息
        :param kwargs:
        :return:
        """
        # request_data = kwargs['request_data']
        # print self.request.body
        # request_data = json.loads(self.request.body)
        alarm_data = self.get_argument('alarm_data', None)
        print alarm_data
        send_message(alarm_data)
