#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
urls.sys_init
~~~~~~~~~~~~~

系统初始化接口
实现方法
    1. 判断系统是否已经初始化
    2. 提供一个初始化添加用户的接口
"""
from handler.sys_init import SysInit
from handler.sys_init import InitAdmin

init_handler = [

    ('/api/v1/sys_init', SysInit),
    ('/api/v1/init_admin', InitAdmin)

]
