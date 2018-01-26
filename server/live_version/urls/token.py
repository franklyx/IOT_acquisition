#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
urls.token
~~~~~~~~~~~~

token api接口的handler
"""
from handler.token import Token, RfToken

token_handler = [

    ('/api/v1/token', Token),
    ('/api/v1/rf-token', RfToken)

]
