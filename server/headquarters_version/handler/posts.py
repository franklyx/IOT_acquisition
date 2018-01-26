#!/usr/bin/env python
# -*- coding:utf-8 -*-

from basic import BasicCtrl


class PostsCtrl(BasicCtrl):
    """渲染首页"""

    def get(self):
        self.render('index.html')
