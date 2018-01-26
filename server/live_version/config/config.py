#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
config
~~~~~~

包含系统所有的配置文件
"""

import os
import sys
import time

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Tornado Config
etc = dict()
etc.setdefault('debug', False)
etc.setdefault('error', False)
etc.setdefault('xheaders', True)  # 获取用户ip地址
etc.setdefault('servs', 'AL/1.0.%s' % int(time.time()))
etc.setdefault('root_path', sys.path[0])
etc.setdefault('xsrf_cookies', False)
etc.setdefault('cookie_secret', 'keda-china')
etc.setdefault('template_path', os.path.join(etc['root_path'], 'template'))
etc.setdefault('static_path', os.path.join(etc['root_path'], 'static'))
