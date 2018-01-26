#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
handler.basic
~~~~~~~~~~~~~

继承tornado的BasicCtrl类
功能：
    主要重载了请求的get,post,put,delete,option的请求基本类型和编写write_error
    和write_json来实现api接口的错误请求和正确请求的返回
    实现两个装饰器来判断现场是否初始化和api请求是否都携带了token值
"""

import functools
import json
import traceback

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from httplib import responses
except ImportError:
    from httpclient import responses

from tornado.web import RequestHandler, HTTPError

from handler import errors
from tools.cfgparser import parser
from model.convert import time2json
from tools.jwt_serializer import tokenAuth
from model.mongo_model.factory import FactoryDB


class BasicCtrl(RequestHandler):
    """这里定义的方法能够在前端模板中调用,实现前后端的数据交互"""

    def data_received(self, chunk):
        pass

    def initialize(self):
        self._caches = {'model': {}, 'datum': {}}

    def set_default_headers(self):
        self.set_header('server', self.settings['servs'])
        self.set_header('x-frame-options', 'SAMEORIGIN')
        self.set_header('x-xss-protection', '1; mode=block')
        self.set_header('cache-control', 'no-transform')
        # 设置允许跨域
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, "
                        "X-Requested-With, X-Requested-By, If-Modified-Since, "
                        "X-File-Name, Cache-Control, Token")
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def post(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def put(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def delete(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def options(self, *args, **kwargs):
        self.write("")

    def write_error(self, status_code, **kwargs):
        self._status_code = 200
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # 在调试模式下，返回错误的详细信息
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.write_json(dict(traceback=''.join(lines)), status_code, self._reason)

        else:
            self.write_json(None, status_code, self._reason)

    def write_json(self, data, status_code=200, msg='success'):
        """
        格式化输出结果
        :param data: 返回的数据
        :param status_code: 错误码
        :param msg: 详细的错误信息
        :return: 格式化后的json字符串
        """
        self.finish(json.dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        }, default=time2json))


class APINotFoundHandler(BasicCtrl):
    """
    定义为定义页面的基础类
    """

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.redirect('/')
        # raise HTTPError(**errors.status_1)

    def post(self, *args, **kwargs):
        self.redirect('/')
        # raise HTTPError(**errors.status_1)

    def put(self, *args, **kwargs):
        self.redirect('/')
        # raise HTTPError(**errors.status_1)

    def delete(self, *args, **kwargs):
        self.redirect('/')
        # raise HTTPError(**errors.status_1)

    def options(self, *args, **kwargs):
        self.write("")


def login(method):
    """定义装饰器login"""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_current_user():
            if self.find_accept('json'):
                self.flash(0, {'sta': 403, 'url': self.get_login_url()})
                return
            if self.request.method in ('GET', 'HEAD'):
                url = self.get_login_url()
                if '?' not in url:
                    if urlparse.urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += '?' + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            self.flash(0, {'sta': 403})
            return
        return method(self, *args, **kwargs)

    return wrapper


def alive(method):
    """检查用户是否已经登录用的装饰器"""

    @login
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.model('admin').chk_user_is_live(self.current_user):
            return method(self, *args, **kwargs)
        else:
            self.flash(0, {'sta': 403, 'url': self.get_login_url()})
            return

    return wrapper


def check_token(method):
    """定义装饰器检测token值"""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        token = self.request.headers.get('Token')
        if token:
            result = tokenAuth(token)
            if result[0] and result[1] is not None:
                return method(self, c_user_id=result[0], c_role=result[1], *args, **kwargs)
            else:
                raise HTTPError(**errors.status_25)
        else:
            raise HTTPError(**errors.status_21)

    return wrapper


def check_token_and_type(method):
    """定义装饰器检测token值和传递的参数类型"""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        token = self.request.headers.get('Token')
        content_type = self.request.headers.get('Content-Type')
        if content_type == 'application/json':
            try:
                request_data = json.loads(self.request.body)
            except:
                raise HTTPError(**errors.status_35)
            if token:
                result = tokenAuth(token)
                if result[0] and result[1] is not None:
                    return method(self, request_data=request_data, c_user_id=result[0],
                                  c_role=result[1], *args, **kwargs)
                else:
                    raise HTTPError(**errors.status_25)
            else:
                raise HTTPError(**errors.status_21)
        else:
            raise HTTPError(**errors.status_34)

    return wrapper


def check_role_one(method):
    """
    单机版 用户权限分为0类，1类
    定义权限装饰器，对api进行访问限制
    进入后台接口需要判断是不是1类账户
    进行增删改的操作时候需要判断是不是1类账户
    允许用户修改自身账户信息
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        role = kwargs['c_role']
        if int(role) == 1:
            return method(self, *args, **kwargs)
        else:
            raise HTTPError(**errors.status_29)

    return wrapper


def check_role_many(method):
    """
    多机版 用户权限分为0类，2类
    定义权限装饰器，对api进行访问限制
    进入后台接口需要判断是不是2类账户
    不允许用户进行增删改操作
    允许用户修改自身账户信息
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        role = kwargs['c_role']
        if int(role) == 2:
            return method(self, *args, **kwargs)
        else:
            raise HTTPError(**errors.status_29)

    return wrapper


def check_sys_init(method):
    """
    检测系统是否初始化，通过对比配置文件中的ID和数据库的ID得到结果
    已经初始化，返回True
    还没有初始化返回False
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        content_type = self.request.headers.get('Content-Type')
        if content_type == 'application/json':
            init_factory_id = parser.factoryid
            result = FactoryDB().find(id=init_factory_id)
            try:
                request_data = json.loads(self.request.body)
            except:
                raise HTTPError(**errors.status_35)
            if not result:
                return method(self, request_data=request_data, c_factory_id=init_factory_id, *args,
                              **kwargs)
            else:
                raise HTTPError(**errors.status_1)
        else:
            raise HTTPError(**errors.status_34)

    return wrapper
